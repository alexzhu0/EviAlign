from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import hashlib
from io import BytesIO, StringIO
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentharness import cli as cli_module
from agentharness.cli import main
from agentharness.runtime_shadow_v1 import (
    MAX_OBSERVATION_BYTES,
    NOT_EXECUTED,
    issue_shadow_request_v1,
)


REVISION = "b" * 40


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _valid_observation(request: dict[str, object]) -> dict[str, object]:
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
        "correlation_id": _canonical_digest(request),
        "tool_calls": [{
            "tool_name": "inspect_policy_summary",
            "arguments": arguments,
            "arguments_digest": _canonical_digest(arguments),
        }],
        "execution_attempted": False,
        "result_status": NOT_EXECUTED,
    }


class _BinaryStdin:
    def __init__(self, value: bytes) -> None:
        self.buffer = BytesIO(value)


class RuntimeShadowCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = issue_shadow_request_v1(
            request_id="shadow-001",
            now=datetime.now(timezone.utc),
            challenge="a" * 64,
            runtime_revision=REVISION,
        )

    def test_shadow_verify_emits_one_redacted_json_report(self) -> None:
        with self._request_path() as request_path:
            code, stdout, stderr = _invoke_cli(
                ["shadow", "verify", str(request_path)],
                json.dumps(_valid_observation(self.request), separators=(",", ":")).encode("utf-8"),
            )

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        payload = _one_bounded_json_document(stdout)
        self.assertEqual("shadow.verification.v1", payload["kind"])
        self.assertEqual(True, payload["ok"])
        self.assertEqual(NOT_EXECUTED, payload["result_status"])
        self.assertNotIn("allow_candidate", payload)
        self.assertNotIn(str(ROOT), stdout)

    def test_shadow_verify_bad_path_never_leaks_path_or_exception(self) -> None:
        private_path = "/tmp/private.json"
        code, stdout, stderr = _invoke_cli(["shadow", "verify", private_path], b"{}")

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_unreadable", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(private_path, stdout)

    def test_shadow_verify_rejects_malformed_request_without_path_leak(self) -> None:
        with self._file_path(b"{") as request_path:
            code, stdout, stderr = _invoke_cli(["shadow", "verify", str(request_path)], b"{}")

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_malformed", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(str(request_path), stdout)

    def test_shadow_verify_rejects_linked_request_without_path_leak(self) -> None:
        with self._request_path() as request_path:
            linked_path = request_path.parent / "linked-request.json"
            linked_path.symlink_to(request_path)
            code, stdout, stderr = _invoke_cli(
                ["shadow", "verify", str(linked_path)],
                json.dumps(_valid_observation(self.request), separators=(",", ":")).encode("utf-8"),
            )

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_unreadable", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(str(linked_path), stdout)

    def test_shadow_verify_rejects_request_through_linked_parent_without_path_leak(self) -> None:
        with self._request_path() as request_path:
            linked_parent = request_path.parent / "linked-request-parent"
            linked_parent.symlink_to(request_path.parent, target_is_directory=True)
            linked_request = linked_parent / request_path.name
            code, stdout, stderr = _invoke_cli(
                ["shadow", "verify", str(linked_request)],
                json.dumps(_valid_observation(self.request), separators=(",", ":")).encode("utf-8"),
            )

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_unreadable", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(str(linked_request), stdout)

    def test_shadow_verify_rejects_hard_linked_request_without_path_or_content_leak(self) -> None:
        with self._request_path() as request_path:
            linked_path = request_path.parent / "hard-linked-request.json"
            os.link(request_path, linked_path)
            code, stdout, stderr = _invoke_cli(
                ["shadow", "verify", str(linked_path)],
                json.dumps(_valid_observation(self.request), separators=(",", ":")).encode("utf-8"),
            )

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_unreadable", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(str(linked_path), stdout)
        self.assertNotIn("a" * 64, stdout)

    @unittest.skipUnless(
        os.path.exists("/dev/null") and stat.S_ISCHR(os.stat("/dev/null").st_mode),
        "requires a POSIX character device",
    )
    def test_shadow_verify_rejects_non_regular_request_without_path_leak(self) -> None:
        request_path = "/dev/null"
        code, stdout, stderr = _invoke_cli(["shadow", "verify", request_path], b"{}")

        self.assertEqual(2, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.request_unreadable", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(request_path, stdout)

    def test_shadow_verify_rejects_oversized_or_malformed_observation_stdin(self) -> None:
        with self._request_path() as request_path:
            for raw, expected_code in (
                (b"{" + b"x" * (MAX_OBSERVATION_BYTES + 1), "shadow.observation_too_large"),
                (b"{", "shadow.observation_malformed"),
            ):
                with self.subTest(expected_code=expected_code):
                    code, stdout, stderr = _invoke_cli(["shadow", "verify", str(request_path)], raw)
                    self.assertEqual(2, code)
                    self.assertEqual("", stderr)
                    self.assertEqual(expected_code, _one_bounded_json_document(stdout)["code"])

    def test_shadow_issue_emits_a_request_with_exact_ttl(self) -> None:
        code, stdout, stderr = _invoke_cli(
            ["shadow", "issue", "--request-id", "shadow-cli-001", "--runtime-revision", REVISION]
        )

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        request = _one_bounded_json_document(stdout)
        issued_at = datetime.strptime(request["issued_at"], "%Y-%m-%dT%H:%M:%SZ")
        expires_at = datetime.strptime(request["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
        self.assertEqual(300, int((expires_at - issued_at).total_seconds()))
        self.assertEqual(NOT_EXECUTED, request["result_status"])
        self.assertNotIn("allow_candidate", request)

    def test_shadow_issue_rejects_missing_request_id_and_malformed_revision_as_json(self) -> None:
        cases = (
            (["shadow", "issue", "--runtime-revision", REVISION], "shadow.argument_invalid"),
            (["shadow", "issue", "--request-id", "shadow-001", "--runtime-revision", "not-a-sha"], "shadow.request_invalid"),
            (["shadow", "issue", "--request-id", "sk-private-request", "--runtime-revision", REVISION], "shadow.request_invalid"),
        )
        for argv, expected_code in cases:
            with self.subTest(argv=argv):
                code, stdout, stderr = _invoke_cli(argv)
                self.assertEqual(2, code)
                self.assertEqual("", stderr)
                self.assertEqual(expected_code, _one_bounded_json_document(stdout)["code"])
                self.assertNotIn("sk-private-request", stdout)

    def test_shadow_rejects_format_and_external_execution_flags_as_json(self) -> None:
        with self._request_path() as request_path:
            for flag in ("--format", "--out", "--write", "--execute", "--run", "--allow"):
                with self.subTest(flag=flag):
                    code, stdout, stderr = _invoke_cli(["shadow", "verify", str(request_path), flag])
                    self.assertEqual(2, code)
                    self.assertEqual("", stderr)
                    self.assertEqual("shadow.argument_invalid", _one_bounded_json_document(stdout)["code"])

    def test_shadow_verify_internal_failure_is_redacted_and_returns_one(self) -> None:
        secret = "secret /private/runtime sk-secret-value"
        with self._request_path() as request_path:
            with patch("agentharness.cli.verify_shadow_observation_v1", side_effect=RuntimeError(secret)):
                code, stdout, stderr = _invoke_cli(
                    ["shadow", "verify", str(request_path)],
                    json.dumps(_valid_observation(self.request), separators=(",", ":")).encode("utf-8"),
                )

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.internal_error", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(secret, stdout)
        self.assertNotIn("/private/runtime", stdout)

    def test_shadow_value_error_is_redacted_json_internal_failure(self) -> None:
        secret = "secret /private/issue sk-secret-value"
        with patch("agentharness.cli._cmd_shadow_issue", side_effect=ValueError(secret)):
            code, stdout, stderr = _invoke_cli(
                ["shadow", "issue", "--request-id", "shadow-001", "--runtime-revision", REVISION]
            )

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertEqual("shadow.internal_error", _one_bounded_json_document(stdout)["code"])
        self.assertNotIn(secret, stdout)
        self.assertNotIn("/private/issue", stdout)

    def test_shadow_reader_rejects_file_changed_during_read(self) -> None:
        with self._request_path() as request_path:
            original_fdopen = cli_module.os.fdopen

            def replace_contents_before_read(descriptor: int, *args, **kwargs):
                request_path.write_bytes(b"changed")
                return original_fdopen(descriptor, *args, **kwargs)

            with patch.object(cli_module.os, "fdopen", side_effect=replace_contents_before_read):
                with self.assertRaises(OSError):
                    cli_module._read_shadow_file(str(request_path))

    def test_shadow_reader_closes_duplicate_when_fdopen_fails(self) -> None:
        with self._request_path() as request_path:
            original_dup = cli_module.os.dup
            duplicates: list[int] = []

            def track_duplicate(descriptor: int) -> int:
                duplicate = original_dup(descriptor)
                duplicates.append(duplicate)
                return duplicate

            with patch.object(cli_module.os, "dup", side_effect=track_duplicate), patch.object(
                cli_module.os, "fdopen", side_effect=OSError("fdopen failed")
            ):
                with self.assertRaises(OSError):
                    cli_module._read_shadow_file(str(request_path))

        self.assertEqual(1, len(duplicates))
        with self.assertRaises(OSError):
            os.fstat(duplicates[0])

    def _request_path(self):
        return self._file_path(json.dumps(self.request, separators=(",", ":")).encode("utf-8"))

    def _file_path(self, contents: bytes):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        request_path = Path(temporary_directory.name) / "request.json"
        request_path.write_bytes(contents)
        return _RequestPathContext(request_path)


class _RequestPathContext:
    def __init__(self, request_path: Path) -> None:
        self.request_path = request_path

    def __enter__(self) -> Path:
        return self.request_path

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False


def _invoke_cli(argv: list[str], stdin: bytes = b"") -> tuple[int, str, str]:
    stdout = StringIO()
    stderr = StringIO()
    with patch("sys.stdin", _BinaryStdin(stdin)), redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            code = main(argv)
        except SystemExit as exc:
            code = exc.code
    return code, stdout.getvalue(), stderr.getvalue()


def _one_bounded_json_document(stdout: str) -> dict[str, object]:
    encoded = stdout.encode("utf-8")
    if len(encoded) > 4096:
        raise AssertionError(f"stdout is unbounded: {len(encoded)}")
    document, end = json.JSONDecoder().raw_decode(stdout)
    if stdout[end:].strip():
        raise AssertionError("stdout contains more than one JSON document")
    if type(document) is not dict:
        raise AssertionError("stdout JSON document is not an object")
    return document


if __name__ == "__main__":
    unittest.main()
