"""Independent receipt fixtures and adversarial evidence boundary tests."""

from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib
from io import BytesIO, StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def request_fixture(now=1000):
    return {
        "kind": "data-access-request-v1", "request_id": "a" * 32,
        "challenge": "b" * 64, "issued_at": now, "expires_at": now + 300,
        "context": {"user_id": "alice", "tenant_id": "acme", "role": "customer",
                    "auth_version": 1, "policy_version": "policy_v1",
                    "data_version": "data_v1"},
        "query": {"tool": "list_orders", "tenant_id": "acme", "customer_id": "alice",
                  "fields": ["order_id", "amount_cents"], "limit": 10},
        "authorization": {"decision": "permit", "reason": "allowed", "scope": {
            "tenant_id": "acme", "customer_id": "alice",
            "fields": ["order_id", "amount_cents"], "limit": 10}},
        "result_status": "not_executed",
    }


def receipt(request):
    return {
        "kind": "data-access-evidence-v1", "request_id": request["request_id"],
        "challenge": request["challenge"], "request_digest": digest(request),
        "context_digest": digest(request["context"]),
        "query_digest": digest(request["query"]),
        "authorization_digest": digest(request["authorization"]),
        "result_status": "not_executed",
    }


class DataAccessEvidenceV1Tests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = importlib.import_module("agentharness.data_access_evidence_v1")
        except ModuleNotFoundError:
            self.fail("data access evidence verifier has not been implemented")
        self.request = request_fixture()
        self.evidence = receipt(self.request)

    def check(self, code, request=None, evidence=None, now=1000):
        actual = self.module.verify_data_access_evidence_v1(
            self.request if request is None else request,
            self.evidence if evidence is None else evidence, now=now)
        self.assertEqual({"kind": "data-access-verification-v1", "ok": code == "ok",
                          "code": "data_access." + code,
                          "result_status": "not_executed"}, actual)

    def test_valid_receipt_and_canonical_ascii_digest(self):
        self.check("ok")
        self.assertEqual(digest({"z": "中文", "a": [1, None]}),
                         self.module.canonical_digest({"a": [1, None], "z": "中文"}))

    def test_every_receipt_binding_is_required(self):
        for key in ("request_id", "challenge", "request_digest", "context_digest",
                    "query_digest", "authorization_digest"):
            with self.subTest(key=key):
                evidence = deepcopy(self.evidence)
                evidence[key] = "0" * len(evidence[key])
                self.check("binding_invalid", evidence=evidence)

    def test_each_expected_request_value_is_bound(self):
        mutations = [
            (("request_id",), "c" * 32), (("challenge",), "d" * 64),
            (("context", "user_id"), "bob"), (("context", "tenant_id"), "nova"),
            (("context", "role"), "support"), (("context", "auth_version"), 2),
            (("context", "policy_version"), "policy_v2"),
            (("context", "data_version"), "data_v2"),
            (("query", "tool"), "customer_contact"), (("query", "tenant_id"), "nova"),
            (("query", "customer_id"), "bob"), (("query", "fields"), ["order_id"]),
            (("query", "limit"), 1), (("authorization", "reason"), "another_reason"),
            (("authorization", "scope", "tenant_id"), "nova"),
            (("authorization", "scope", "customer_id"), None),
            (("authorization", "scope", "fields"), ["order_id"]),
            (("authorization", "scope", "limit"), 1),
        ]
        for path, value in mutations:
            with self.subTest(path=path):
                changed = deepcopy(self.request)
                parent = changed
                for part in path[:-1]:
                    parent = parent[part]
                parent[path[-1]] = value
                self.check("binding_invalid", request=changed)
        changed = deepcopy(self.request)
        changed.update(issued_at=999, expires_at=1299)
        self.check("binding_invalid", request=changed)
        changed["authorization"].update(decision="deny", scope={})
        self.check("binding_invalid", request=changed)

    def test_freshness_exact_lifetime_and_integer_types(self):
        self.check("ok", now=1299)
        for now in (999, 1300, 1301):
            self.check("request_expired", now=now)
        for now in (True, 1000.0, -1, "1000"):
            self.check("request_invalid", now=now)
        for key, value in (("issued_at", True), ("issued_at", -1),
                           ("expires_at", 1301), ("expires_at", 1300.0)):
            changed = deepcopy(self.request)
            changed[key] = value
            self.check("request_invalid", request=changed)

    def test_denial_remains_denial_and_requires_empty_scope(self):
        changed = deepcopy(self.request)
        changed["authorization"].update(decision="deny", scope={})
        self.check("policy_denied", request=changed, evidence=receipt(changed))
        changed["authorization"]["scope"] = self.request["authorization"]["scope"]
        self.check("request_invalid", request=changed)

    def test_unknown_or_missing_keys_are_invalid_at_every_level(self):
        for path in ((), ("context",), ("query",), ("authorization",),
                     ("authorization", "scope")):
            for extra in (False, True):
                with self.subTest(path=path, extra=extra):
                    changed = deepcopy(self.request)
                    parent = changed
                    for key in path:
                        parent = parent[key]
                    if extra:
                        parent["untrusted"] = "secret"
                    else:
                        parent.pop(next(iter(parent)))
                    self.check("request_invalid", request=changed)
        for key in self.evidence:
            changed = deepcopy(self.evidence)
            changed.pop(key)
            self.check("evidence_invalid", evidence=changed)
        self.check("evidence_invalid", evidence={**self.evidence, "rows": []})

    def test_malformed_identifiers_fields_limits_and_statuses_fail_closed(self):
        cases = [("tenant_id", v) for v in ("ACME", "a/b", "á", "a" * 33, "", 1)]
        cases += [("fields", v) for v in ([], ["a"] * 2, ["a"] * 17, "order_id", [1])]
        cases += [("limit", v) for v in (0, 51, True, 1.0, "1")]
        cases += [("customer_id", v) for v in (False, "Alice", "../alice")]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                changed = deepcopy(self.request)
                changed["query"][key] = value
                self.check("request_invalid", request=changed)
        for key, value in (("kind", "other"), ("result_status", "executed"),
                           ("request_id", "A" * 32), ("challenge", "b" * 63)):
            self.check("request_invalid", request={**self.request, key: value})
        for key, value in (("kind", "other"), ("result_status", "executed"),
                           ("context_digest", "A" * 64)):
            self.check("evidence_invalid", evidence={**self.evidence, key: value})
        changed = deepcopy(self.request)
        changed["context"]["role"] = "admin"
        self.check("request_invalid", request=changed)

    def test_nullable_customer_id_and_structural_scope_are_allowed(self):
        changed = deepcopy(self.request)
        changed["query"]["customer_id"] = None
        changed["authorization"]["scope"]["customer_id"] = None
        self.check("ok", request=changed, evidence=receipt(changed))

    def test_api_rejects_non_json_values_and_internal_error_never_leaks(self):
        for value in ([], "secret", 1, True, object()):
            self.check("request_invalid", request=value)
            self.check("evidence_invalid", evidence=value)
        with patch.object(self.module, "canonical_digest", side_effect=RuntimeError("/secret/token")):
            self.check("internal_error")

    def test_auth_version_bounds_and_finite_canonicalization(self):
        for value in (0, True, 1.0, "auth_v1", 1_000_000_001):
            changed = deepcopy(self.request)
            changed["context"]["auth_version"] = value
            self.check("request_invalid", request=changed)
        changed = deepcopy(self.request)
        changed["context"]["auth_version"] = 1_000_000_000
        self.check("ok", request=changed, evidence=receipt(changed))
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                self.module.canonical_digest(value)

    def test_list_bounds_and_cycles_are_rejected(self):
        changed = deepcopy(self.request)
        changed["query"]["fields"] = ["field_" + chr(97 + i) for i in range(16)]
        self.check("ok", request=changed, evidence=receipt(changed))
        changed["query"]["fields"].append("field_q")
        self.check("request_invalid", request=changed)
        changed = deepcopy(self.request)
        changed["query"]["fields"] = changed
        self.check("request_invalid", request=changed)
        changed = deepcopy(self.evidence)
        changed["query_digest"] = "a" * 16385
        self.check("evidence_invalid", evidence=changed)

    def test_cli_internal_clock_failure_is_one_fixed_report(self):
        raw = json.dumps({"request": self.request, "evidence": self.evidence}).encode()
        stdout, stderr = StringIO(), StringIO()
        with patch.object(sys, "stdin", SimpleNamespace(buffer=BytesIO(raw))), \
                patch.object(self.module.time, "time", side_effect=RuntimeError("/secret/token")), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                status = self.module.main()
            except Exception:
                self.fail("CLI exposed an internal failure instead of a fixed report")
        self.assertEqual(2, status)
        self.assertEqual("", stderr.getvalue())
        self.assertEqual({"kind": "data-access-verification-v1", "ok": False,
                          "code": "data_access.internal_error", "result_status": "not_executed"},
                         json.loads(stdout.getvalue()))

    def cli(self, raw):
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
        run = subprocess.run([sys.executable, "-m", "agentharness.data_access_evidence_v1"],
                             input=raw, capture_output=True, env=env, cwd=ROOT, timeout=5)
        self.assertEqual(b"", run.stderr)
        self.assertLess(len(run.stdout), 256)
        self.assertEqual(1, len(run.stdout.splitlines()))
        report = json.loads(run.stdout)
        self.assertEqual("not_executed", report["result_status"])
        self.assertEqual({"kind", "ok", "code", "result_status"}, set(report))
        return run.returncode, report

    def test_cli_valid_and_expired_documents(self):
        request = request_fixture(int(time.time()))
        raw = json.dumps({"request": request, "evidence": receipt(request)}).encode()
        self.assertEqual((0, {"kind": "data-access-verification-v1", "ok": True,
                            "code": "data_access.ok", "result_status": "not_executed"}), self.cli(raw))
        request = request_fixture(1)
        status, report = self.cli(json.dumps({"request": request, "evidence": receipt(request)}).encode())
        self.assertEqual(2, status)
        self.assertEqual("data_access.request_expired", report["code"])

    def test_cli_duplicate_oversized_deep_and_invalid_inputs_are_fixed_reports(self):
        invalid = [b"", b"{", b"\xff", b"{} {}", b"[]", b'{"request":{},"request":{}}',
                   b'{"request":{"context":{"role":"customer","role":"support"}},"evidence":{}}',
                   b" " * 16385, b"[" * 1000 + b"0" + b"]" * 1000,
                   b'{"request":NaN,"evidence":{}}', b'{"request":1e999,"evidence":{}}',
                   b'{"request":{},"evidence":{},"extra":"/secret/token"}']
        for raw in invalid:
            with self.subTest(size=len(raw)):
                status, report = self.cli(raw)
                self.assertEqual(2, status)
                self.assertEqual("data_access.request_invalid", report["code"])


if __name__ == "__main__":
    unittest.main()
