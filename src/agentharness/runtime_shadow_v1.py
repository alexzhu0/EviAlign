"""Pure, bounded verifier for a non-executing runtime shadow observation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import re
from typing import Mapping


RUNTIME_ID = "deepseek-harness"
MODEL_ID = "deepseek-v4-flash"
TOOL_NAME = "inspect_policy_summary"
NOT_EXECUTED = "not_executed"
MAX_REQUEST_BYTES = 4096
MAX_OBSERVATION_BYTES = 8192
REQUEST_TTL_SECONDS = 300
MAX_STRUCTURE_DEPTH = 16
POLICY_SCOPE = "agentharness-shadow-poc"

TOOL_SCHEMA: dict[str, object] = {
    "additionalProperties": False,
    "properties": {
        "challenge": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        "policy_scope": {"const": POLICY_SCOPE, "type": "string"},
    },
    "required": ["challenge", "policy_scope"],
    "type": "object",
}

_REQUEST_KEYS = frozenset({
    "kind", "request_id", "challenge", "runtime_id", "runtime_revision",
    "model", "tool_name", "tool_schema_digest", "policy_scope", "issued_at",
    "expires_at", "result_status",
})
_OBSERVATION_KEYS = frozenset({
    "kind", "request_id", "challenge", "runtime_id", "runtime_revision",
    "model", "tool_schema_digest", "correlation_id", "tool_calls",
    "execution_attempted", "result_status",
})
_TOOL_CALL_KEYS = frozenset({"tool_name", "arguments", "arguments_digest"})
_ARGUMENT_KEYS = frozenset({"challenge", "policy_scope"})
_FORBIDDEN_KEYS = frozenset({
    "api_key", "authorization", "token", "secret", "prompt", "response",
    "path", "cwd", "workspace",
})
_HEX_64_RE = re.compile(r"[0-9a-f]{64}\Z")
_HEX_40_RE = re.compile(r"[0-9a-f]{40}\Z")
_REQUEST_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")


class RuntimeShadowValidationError(ValueError):
    """A public, bounded parse failure with no untrusted detail."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _canonical_json(value: object) -> bytes:
    _validate_json_value(value, 0)
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


TOOL_SCHEMA_DIGEST = hashlib.sha256(
    json.dumps(
        TOOL_SCHEMA, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
).hexdigest()


def issue_shadow_request_v1(
    *, request_id: str, now: datetime, challenge: str, runtime_revision: str
) -> dict[str, object]:
    """Issue one deterministic, evidence-only shadow request."""

    instant = _as_utc(now)
    request = {
        "kind": "shadow-request-v1",
        "request_id": request_id,
        "challenge": challenge,
        "runtime_id": RUNTIME_ID,
        "runtime_revision": runtime_revision,
        "model": MODEL_ID,
        "tool_name": TOOL_NAME,
        "tool_schema_digest": TOOL_SCHEMA_DIGEST,
        "policy_scope": POLICY_SCOPE,
        "issued_at": _utc_rfc3339(instant),
        "expires_at": _utc_rfc3339(instant + timedelta(seconds=REQUEST_TTL_SECONDS)),
        "result_status": NOT_EXECUTED,
    }
    _validate_request(request)
    if len(_canonical_json(request)) > MAX_REQUEST_BYTES:
        raise RuntimeShadowValidationError("shadow.request_too_large")
    return request


def parse_shadow_json_v1(
    raw: bytes, *, maximum_bytes: int, document_kind: str
) -> dict[str, object]:
    """Parse one bounded UTF-8 JSON object and reject ambiguous duplicate keys."""

    prefix = _document_prefix(document_kind)
    if type(raw) is not bytes or type(maximum_bytes) is not int or maximum_bytes < 1:
        raise RuntimeShadowValidationError(f"{prefix}_malformed")
    if not raw or len(raw) > maximum_bytes:
        raise RuntimeShadowValidationError(f"{prefix}_too_large")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
        _validate_json_value(value, 0)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, RecursionError):
        raise RuntimeShadowValidationError(f"{prefix}_malformed") from None
    if type(value) is not dict:
        raise RuntimeShadowValidationError(f"{prefix}_malformed")
    return value


def verify_shadow_observation_v1(
    request: Mapping[str, object], observation: Mapping[str, object], *, now: datetime
) -> dict[str, object]:
    """Verify a single observation without authorizing or executing anything."""

    try:
        validated_request = _validate_request(request)
        current_time = _as_utc(now)
        issued_at = _parse_rfc3339(validated_request["issued_at"])
        if current_time < issued_at:
            return _report(False, "shadow.request_invalid", validated_request)
        if current_time >= _parse_rfc3339(validated_request["expires_at"]):
            return _report(False, "shadow.request_expired", validated_request)
    except RuntimeShadowValidationError:
        return _report(False, "shadow.request_invalid", None)

    try:
        validated_observation = _validate_observation(observation)
    except RuntimeShadowValidationError:
        return _report(False, "shadow.observation_invalid", validated_request)

    if not _observation_binds_request(validated_request, validated_observation):
        return _report(False, "shadow.binding_invalid", validated_request)
    return _report(True, "shadow.ok", validated_request)


def _validate_request(value: object) -> dict[str, object]:
    _validate_json_value(value, 0)
    if type(value) is not dict or set(value) != _REQUEST_KEYS:
        raise RuntimeShadowValidationError("shadow.request_invalid")
    if (
        value["kind"] != "shadow-request-v1"
        or value["runtime_id"] != RUNTIME_ID
        or value["model"] != MODEL_ID
        or value["tool_name"] != TOOL_NAME
        or value["tool_schema_digest"] != TOOL_SCHEMA_DIGEST
        or value["policy_scope"] != POLICY_SCOPE
        or value["result_status"] != NOT_EXECUTED
        or not _valid_request_id(value["request_id"])
        or not _valid_hex(value["challenge"], _HEX_64_RE)
        or not _valid_hex(value["runtime_revision"], _HEX_40_RE)
    ):
        raise RuntimeShadowValidationError("shadow.request_invalid")
    issued_at = _parse_rfc3339(value["issued_at"])
    expires_at = _parse_rfc3339(value["expires_at"])
    if expires_at - issued_at != timedelta(seconds=REQUEST_TTL_SECONDS):
        raise RuntimeShadowValidationError("shadow.request_invalid")
    return value


def _validate_observation(value: object) -> dict[str, object]:
    _validate_json_value(value, 0)
    if type(value) is not dict or set(value) != _OBSERVATION_KEYS or _contains_sensitive_content(value):
        raise RuntimeShadowValidationError("shadow.observation_invalid")
    fixed_fields = (
        ("kind", "runtime-shadow-observation-v1"),
        ("execution_attempted", False),
        ("result_status", NOT_EXECUTED),
    )
    if (
        type(value["execution_attempted"]) is not bool
        or any(value[field] != expected for field, expected in fixed_fields)
    ):
        raise RuntimeShadowValidationError("shadow.observation_invalid")
    if not (
        _valid_request_id(value["request_id"])
        and _valid_hex(value["challenge"], _HEX_64_RE)
        and _valid_hex(value["runtime_revision"], _HEX_40_RE)
        and _valid_hex(value["tool_schema_digest"], _HEX_64_RE)
        and _valid_hex(value["correlation_id"], _HEX_64_RE)
        and _valid_identifier(value["runtime_id"])
        and _valid_identifier(value["model"])
        and type(value["tool_calls"]) is list
        and len(value["tool_calls"]) == 1
    ):
        raise RuntimeShadowValidationError("shadow.observation_invalid")
    call = value["tool_calls"][0]
    if type(call) is not dict or set(call) != _TOOL_CALL_KEYS:
        raise RuntimeShadowValidationError("shadow.observation_invalid")
    arguments = call["arguments"]
    if (
        not _valid_identifier(call["tool_name"])
        or type(arguments) is not dict
        or set(arguments) != _ARGUMENT_KEYS
        or not _valid_hex(call["arguments_digest"], _HEX_64_RE)
        or not _valid_hex(arguments["challenge"], _HEX_64_RE)
        or arguments["policy_scope"] != POLICY_SCOPE
    ):
        raise RuntimeShadowValidationError("shadow.observation_invalid")
    return value


def _observation_binds_request(request: dict[str, object], observation: dict[str, object]) -> bool:
    for field in (
        "request_id", "challenge", "runtime_id", "runtime_revision", "model",
        "tool_schema_digest",
    ):
        if observation[field] != request[field]:
            return False
    call = observation["tool_calls"][0]
    arguments = call["arguments"]
    return (
        call["tool_name"] == request["tool_name"]
        and arguments["challenge"] == request["challenge"]
        and arguments["policy_scope"] == request["policy_scope"]
        and call["arguments_digest"] == _digest(arguments)
        and observation["correlation_id"] == _digest(request)
    )


def _report(ok: bool, code: str, request: dict[str, object] | None) -> dict[str, object]:
    if request is None:
        return {
            "ok": ok,
            "code": code,
            "request_id": None,
            "runtime_id": RUNTIME_ID,
            "model": MODEL_ID,
            "tool_name": TOOL_NAME,
            "result_status": NOT_EXECUTED,
        }
    return {
        "ok": ok,
        "code": code,
        "request_id": request["request_id"],
        "runtime_id": request["runtime_id"],
        "model": request["model"],
        "tool_name": request["tool_name"],
        "result_status": NOT_EXECUTED,
    }


def _validate_json_value(value: object, depth: int) -> None:
    if depth > MAX_STRUCTURE_DEPTH:
        raise RuntimeShadowValidationError("shadow.structure_too_deep")
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise RuntimeShadowValidationError("shadow.structure_invalid")
            _validate_json_value(item, depth + 1)
        return
    if type(value) is list:
        for item in value:
            _validate_json_value(item, depth + 1)
        return
    if type(value) is float and not math.isfinite(value):
        raise RuntimeShadowValidationError("shadow.structure_invalid")
    if type(value) not in (str, int, float, bool, type(None)):
        raise RuntimeShadowValidationError("shadow.structure_invalid")


def _contains_sensitive_content(value: object) -> bool:
    if type(value) is dict:
        return any(key in _FORBIDDEN_KEYS or _contains_sensitive_content(item) for key, item in value.items())
    if type(value) is list:
        return any(_contains_sensitive_content(item) for item in value)
    return type(value) is str and (value.startswith("sk-") or value.startswith("/"))


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _valid_hex(value: object, pattern: re.Pattern[str]) -> bool:
    return type(value) is str and pattern.fullmatch(value) is not None


def _valid_request_id(value: object) -> bool:
    return (
        type(value) is str
        and not value.startswith("sk-")
        and _REQUEST_ID_RE.fullmatch(value) is not None
    )


def _valid_identifier(value: object) -> bool:
    return type(value) is str and 1 <= len(value) <= 128 and _REQUEST_ID_RE.fullmatch(value) is not None


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _as_utc(value: datetime) -> datetime:
    if type(value) is not datetime or value.tzinfo is None or value.utcoffset() is None:
        raise RuntimeShadowValidationError("shadow.time_invalid")
    return value.astimezone(timezone.utc)


def _utc_rfc3339(value: datetime) -> str:
    return _as_utc(value).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_rfc3339(value: object) -> datetime:
    if type(value) is not str:
        raise RuntimeShadowValidationError("shadow.time_invalid")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise RuntimeShadowValidationError("shadow.time_invalid") from None


def _document_prefix(document_kind: str) -> str:
    if document_kind == "request":
        return "shadow.request"
    if document_kind == "observation":
        return "shadow.observation"
    return "shadow.document"
