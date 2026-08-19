from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentharness.runtime_shadow_v1 import (
    MAX_OBSERVATION_BYTES,
    RuntimeShadowValidationError,
    TOOL_SCHEMA_DIGEST,
    issue_shadow_request_v1,
    parse_shadow_json_v1,
    verify_shadow_observation_v1,
)


NOW = datetime(2026, 8, 19, 12, 0, tzinfo=timezone.utc)
CHALLENGE = "a" * 64
REVISION = "b" * 40


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def valid_observation(request: dict[str, object]) -> dict[str, object]:
    arguments = {
        "challenge": request["challenge"],
        "policy_scope": "agentharness-shadow-poc",
    }
    return {
        "kind": "runtime-shadow-observation-v1",
        "request_id": request["request_id"],
        "challenge": request["challenge"],
        "runtime_id": request["runtime_id"],
        "runtime_revision": request["runtime_revision"],
        "model": request["model"],
        "tool_schema_digest": request["tool_schema_digest"],
        "correlation_id": canonical_digest(request),
        "tool_calls": [
            {
                "tool_name": "inspect_policy_summary",
                "arguments": arguments,
                "arguments_digest": canonical_digest(arguments),
            }
        ],
        "execution_attempted": False,
        "result_status": "not_executed",
    }


class RuntimeShadowV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = issue_shadow_request_v1(
            request_id="shadow-001",
            now=NOW,
            challenge=CHALLENGE,
            runtime_revision=REVISION,
        )

    def assert_rejected_without_echo(self, observation: dict[str, object], secret: str, code: str) -> None:
        report = verify_shadow_observation_v1(self.request, observation, now=NOW)
        self.assertEqual(False, report["ok"])
        self.assertEqual(code, report["code"])
        self.assertNotIn(secret, json.dumps(report, sort_keys=True))

    def test_valid_observation_binds_exact_request_without_execution(self) -> None:
        report = verify_shadow_observation_v1(self.request, valid_observation(self.request), now=NOW)

        self.assertEqual(True, report["ok"])
        self.assertEqual("shadow.ok", report["code"])
        self.assertEqual("not_executed", report["result_status"])
        self.assertEqual("shadow-001", report["request_id"])
        self.assertNotIn("allow_candidate", report)

    def test_changed_challenge_is_rejected_without_echoing_it(self) -> None:
        observation = valid_observation(self.request)
        observation["challenge"] = "c" * 64
        observation["tool_calls"][0]["arguments"]["challenge"] = "c" * 64
        observation["tool_calls"][0]["arguments_digest"] = canonical_digest(observation["tool_calls"][0]["arguments"])

        self.assert_rejected_without_echo(observation, "c" * 64, "shadow.binding_invalid")

    def test_expired_request_is_rejected(self) -> None:
        report = verify_shadow_observation_v1(
            self.request,
            valid_observation(self.request),
            now=NOW + timedelta(seconds=301),
        )

        self.assertEqual(False, report["ok"])
        self.assertEqual("shadow.request_expired", report["code"])

    def test_future_issued_and_shortened_ttl_requests_are_rejected(self) -> None:
        future_request = issue_shadow_request_v1(
            request_id="shadow-future",
            now=NOW + timedelta(hours=1),
            challenge=CHALLENGE,
            runtime_revision=REVISION,
        )
        shortened_request = deepcopy(self.request)
        shortened_request["expires_at"] = "2026-08-19T12:04:59Z"
        for request in (future_request, shortened_request):
            with self.subTest(request=request["request_id"]):
                report = verify_shadow_observation_v1(request, valid_observation(request), now=NOW)
                self.assertEqual(False, report["ok"])
                self.assertEqual("shadow.request_invalid", report["code"])

    def test_current_request_binding_fields_reject_changes(self) -> None:
        cases = (
            ("request_id", "shadow-002"),
            ("runtime_revision", "c" * 40),
            ("model", "other-model"),
            ("tool_schema_digest", "d" * 64),
            ("correlation_id", "e" * 64),
        )
        for field, value in cases:
            with self.subTest(field=field):
                observation = valid_observation(self.request)
                observation[field] = value
                self.assert_rejected_without_echo(observation, value, "shadow.binding_invalid")

        observation = valid_observation(self.request)
        observation["tool_calls"][0]["tool_name"] = "other_tool"
        self.assert_rejected_without_echo(observation, "other_tool", "shadow.binding_invalid")

    def test_tool_calls_must_contain_exactly_one_canonical_call(self) -> None:
        for calls in ([], valid_observation(self.request)["tool_calls"] * 2):
            with self.subTest(calls=calls):
                observation = valid_observation(self.request)
                observation["tool_calls"] = calls
                report = verify_shadow_observation_v1(self.request, observation, now=NOW)
                self.assertEqual(False, report["ok"])
                self.assertEqual("shadow.observation_invalid", report["code"])

    def test_missing_and_extra_observation_or_call_fields_are_rejected(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = []
        missing = valid_observation(self.request)
        del missing["model"]
        cases.append(("missing top-level field", missing))
        extra = valid_observation(self.request)
        extra["extra"] = "do-not-echo"
        cases.append(("extra top-level field", extra))
        missing_call = valid_observation(self.request)
        del missing_call["tool_calls"][0]["arguments_digest"]
        cases.append(("missing call field", missing_call))
        extra_call = valid_observation(self.request)
        extra_call["tool_calls"][0]["extra"] = "do-not-echo"
        cases.append(("extra call field", extra_call))
        for name, observation in cases:
            with self.subTest(name=name):
                report = verify_shadow_observation_v1(self.request, observation, now=NOW)
                self.assertEqual(False, report["ok"])
                self.assertEqual("shadow.observation_invalid", report["code"])

    def test_argument_extra_key_is_rejected_without_echo(self) -> None:
        observation = valid_observation(self.request)
        arguments = observation["tool_calls"][0]["arguments"]
        arguments["unexpected"] = "do-not-echo"
        observation["tool_calls"][0]["arguments_digest"] = canonical_digest(arguments)

        self.assert_rejected_without_echo(observation, "do-not-echo", "shadow.observation_invalid")

    def test_execution_statuses_cannot_claim_execution(self) -> None:
        cases = (
            ("execution_attempted", True),
            ("execution_attempted", 0),
            ("result_status", "executed"),
        )
        for field, value in cases:
            with self.subTest(field=field):
                observation = valid_observation(self.request)
                observation[field] = value
                report = verify_shadow_observation_v1(self.request, observation, now=NOW)
                self.assertEqual(False, report["ok"])
                self.assertEqual("shadow.observation_invalid", report["code"])

    def test_absolute_path_forbidden_keys_and_credential_prefix_are_rejected_without_echo(self) -> None:
        probes = [("path", "/private/host/path")]
        probes.extend((key, "not-for-report") for key in (
            "api_key", "authorization", "token", "secret", "prompt", "response", "path", "cwd", "workspace"
        ))
        probes.append(("harmless", "sk-private-value"))
        for key, value in probes:
            with self.subTest(key=key):
                observation = valid_observation(self.request)
                observation["tool_calls"][0]["arguments"][key] = value
                self.assert_rejected_without_echo(observation, value, "shadow.observation_invalid")

    def test_parse_rejects_oversized_bytes_and_duplicate_json_keys(self) -> None:
        with self.assertRaises(RuntimeShadowValidationError) as oversized:
            parse_shadow_json_v1(
                b"{" + b"x" * MAX_OBSERVATION_BYTES + b"}",
                maximum_bytes=MAX_OBSERVATION_BYTES,
                document_kind="observation",
            )
        self.assertEqual("shadow.observation_too_large", oversized.exception.code)

        with self.assertRaises(RuntimeShadowValidationError) as duplicate:
            parse_shadow_json_v1(
                b'{"kind":"one","kind":"two"}',
                maximum_bytes=MAX_OBSERVATION_BYTES,
                document_kind="observation",
            )
        self.assertEqual("shadow.observation_malformed", duplicate.exception.code)

    def test_issued_request_has_bounded_canonical_constants(self) -> None:
        self.assertEqual("shadow-request-v1", self.request["kind"])
        self.assertEqual("not_executed", self.request["result_status"])
        self.assertEqual(TOOL_SCHEMA_DIGEST, self.request["tool_schema_digest"])
        self.assertEqual("2026-08-19T12:05:00Z", self.request["expires_at"])

    def test_mutated_input_mappings_and_depth_exceeding_values_fail_closed(self) -> None:
        observation = valid_observation(self.request)
        nested: dict[str, object] = {"value": "safe"}
        for _ in range(17):
            nested = {"next": nested}
        observation["unexpected"] = nested

        report = verify_shadow_observation_v1(self.request, observation, now=NOW)
        self.assertEqual(False, report["ok"])
        self.assertEqual("shadow.observation_invalid", report["code"])


if __name__ == "__main__":
    unittest.main()
