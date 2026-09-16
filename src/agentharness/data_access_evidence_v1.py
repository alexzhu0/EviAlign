"""Bounded correlation of caller-owned data-access requests and receipts.

Digest agreement is neither authentication nor runtime authorization. The caller
must independently own the original request, authorize access, and gate any
execution. Every report from this module is evidence only and not_executed.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time


MAX_INPUT_BYTES = 16 * 1024
MAX_DEPTH = 12
_NAME = re.compile(r"[a-z][a-z0-9_]{0,31}", re.ASCII)
_HEX32 = re.compile(r"[0-9a-f]{32}", re.ASCII)
_HEX64 = re.compile(r"[0-9a-f]{64}", re.ASCII)
_REQUEST_KEYS = {"kind", "request_id", "challenge", "issued_at", "expires_at",
                 "context", "query", "authorization", "result_status"}
_CONTEXT_KEYS = {"user_id", "tenant_id", "role", "auth_version", "policy_version", "data_version"}
_SCOPE_KEYS = {"tenant_id", "customer_id", "fields", "limit"}
_DIGEST_KEYS = ("request_digest", "context_digest", "query_digest", "authorization_digest")
_EVIDENCE_KEYS = {"kind", "request_id", "challenge", "result_status", *_DIGEST_KEYS}


def _json_text(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def canonical_digest(value) -> str:
    """SHA-256 of sorted, compact ASCII JSON; nonfinite numbers are invalid."""
    return hashlib.sha256(_json_text(value).encode("ascii")).hexdigest()


def _bounded(value) -> bool:
    """Reject non-JSON objects and limit work before recursive serialization."""
    pending = [(value, 0)]
    nodes = 0
    while pending:
        item, depth = pending.pop()
        nodes += 1
        if depth > MAX_DEPTH or nodes > 2048:
            return False
        if type(item) is dict:
            if len(item) > 64 or any(type(key) is not str or len(key) > 64 for key in item):
                return False
            pending.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            if len(item) > 64:
                return False
            pending.extend((child, depth + 1) for child in item)
        elif type(item) is str:
            if len(item) > MAX_INPUT_BYTES:
                return False
        elif type(item) is int:
            if item.bit_length() > 63:
                return False
        elif type(item) is float:
            if not math.isfinite(item):
                return False
        elif item is not None and type(item) is not bool:
            return False
    return len(_json_text(value)) <= MAX_INPUT_BYTES


def _keys(value, expected) -> bool:
    return type(value) is dict and value.keys() == expected


def _matches(value, pattern) -> bool:
    return type(value) is str and pattern.fullmatch(value) is not None


def _integer(value, low, high) -> bool:
    return type(value) is int and low <= value <= high


def _scope(value) -> bool:
    if not _keys(value, _SCOPE_KEYS):
        return False
    fields = value["fields"]
    return (
        _matches(value["tenant_id"], _NAME)
        and (value["customer_id"] is None or _matches(value["customer_id"], _NAME))
        and type(fields) is list and 1 <= len(fields) <= 16
        and all(_matches(field, _NAME) for field in fields)
        and len(set(fields)) == len(fields)
        and _integer(value["limit"], 1, 50)
    )


def _request_valid(value) -> bool:
    if not _bounded(value) or not _keys(value, _REQUEST_KEYS):
        return False
    if (value["kind"] != "data-access-request-v1"
            or value["result_status"] != "not_executed"
            or not _matches(value["request_id"], _HEX32)
            or not _matches(value["challenge"], _HEX64)
            or not _integer(value["issued_at"], 0, 2**63 - 1)
            or not _integer(value["expires_at"], 0, 2**63 - 1)
            or value["expires_at"] - value["issued_at"] != 300):
        return False
    context, query, authorization = value["context"], value["query"], value["authorization"]
    if (not _keys(context, _CONTEXT_KEYS)
            or not all(_matches(context[key], _NAME) for key in
                       ("user_id", "tenant_id", "role", "policy_version", "data_version"))
            or context["role"] not in ("customer", "support", "analyst")
            or not _integer(context["auth_version"], 1, 1_000_000_000)):
        return False
    if (not _keys(query, _SCOPE_KEYS | {"tool"})
            or not _matches(query["tool"], _NAME)
            or not _scope({key: query[key] for key in _SCOPE_KEYS})):
        return False
    if (not _keys(authorization, {"decision", "reason", "scope"})
            or not _matches(authorization["reason"], _NAME)):
        return False
    if authorization["decision"] == "deny":
        return type(authorization["scope"]) is dict and not authorization["scope"]
    return authorization["decision"] == "permit" and _scope(authorization["scope"])


def _evidence_valid(value) -> bool:
    return (
        _bounded(value) and _keys(value, _EVIDENCE_KEYS)
        and value["kind"] == "data-access-evidence-v1"
        and value["result_status"] == "not_executed"
        and _matches(value["request_id"], _HEX32)
        and _matches(value["challenge"], _HEX64)
        and all(_matches(value[key], _HEX64) for key in _DIGEST_KEYS)
    )


def _report(code) -> dict:
    return {"kind": "data-access-verification-v1", "ok": code == "ok",
            "code": "data_access." + code, "result_status": "not_executed"}


def verify_data_access_evidence_v1(request, evidence, *, now: int) -> dict:
    """Correlate evidence only; freshness uses issued_at <= now < expires_at."""
    try:
        if not _integer(now, 0, 2**63 - 1) or not _request_valid(request):
            return _report("request_invalid")
        if not request["issued_at"] <= now < request["expires_at"]:
            return _report("request_expired")
        if not _evidence_valid(evidence):
            return _report("evidence_invalid")
        expected = {"request_id": request["request_id"], "challenge": request["challenge"],
                    "request_digest": canonical_digest(request),
                    "context_digest": canonical_digest(request["context"]),
                    "query_digest": canonical_digest(request["query"]),
                    "authorization_digest": canonical_digest(request["authorization"])}
        if any(evidence[key] != value for key, value in expected.items()):
            return _report("binding_invalid")
        return _report("ok" if request["authorization"]["decision"] == "permit" else "policy_denied")
    except Exception:
        return _report("internal_error")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError


def main() -> int:
    """Read one bounded JSON envelope; emit one fixed report with no raw input."""
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                              parse_constant=_reject_constant)
        if not _bounded(document) or not _keys(document, {"request", "evidence"}):
            raise ValueError
    except (ValueError, UnicodeError, RecursionError):
        report = _report("request_invalid")
    except Exception:
        report = _report("internal_error")
    else:
        try:
            report = verify_data_access_evidence_v1(document["request"], document["evidence"],
                                                   now=int(time.time()))
        except Exception:
            report = _report("internal_error")
    sys.stdout.write(_json_text(report) + "\n")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
