# Runtime Shadow Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, generic AgentHarness request/observation verifier for a local DeepSeek Harness shadow PoC without creating runtime authorization or execution.

**Architecture:** A pure `runtime_shadow_v1` module issues a per-request challenge and verifies one external observation against it. A `shadow` CLI group reads bounded UTF-8 JSON and produces one deterministic redacted verification document; it has no network, adapter, filesystem execution, or policy-allow behavior.

**Tech Stack:** Python 3.10+, standard-library `json`, `hashlib`, `secrets`, `datetime`, `argparse`, `unittest`.

## Global Constraints

- This repository remains a pre-execution evidence control-plane: every shadow output has `result_status: "not_executed"`; `allow_candidate` is never emitted or treated as permission.
- Contract v1 accepts only `runtime_id: "deepseek-harness"`, `model: "deepseek-v4-flash"`, and `tool_name: "inspect_policy_summary"`.
- Request JSON is at most 4096 UTF-8 bytes; observation JSON is at most 8192 UTF-8 bytes; duplicate JSON keys, non-object roots, invalid UTF-8, and excess bytes fail closed.
- A request uses a 1–64 ASCII `request_id`, 64 lowercase-hex challenge, 40 lowercase-hex runtime revision, and a 64 lowercase-hex tool-schema digest. An observation carries that schema digest, the 64 lowercase-hex canonical-argument digest, and issue/expiry times no more than 300 seconds apart.
- Observation arguments contain exactly `challenge` and `policy_scope: "agentharness-shadow-poc"`; observations include no prompt, response, API key, absolute path, or sensitive key name/value. Its opaque `correlation_id` is exactly the lowercase SHA-256 digest of the canonical request document, so it can be bound without storing replay state or echoing untrusted content.
- Cross-request replay is rejected by exact request/challenge binding. Byte-identical same-request replay detection is explicitly outside v1 because no durable replay store is introduced.
- CLI output is a single bounded JSON document with stable reason codes and never exposes host paths, exception text, credentials, raw arguments, prompts, or responses.
- Do not change Pi contracts, adapter registry behavior, policy semantics, CI API calls, or any external runtime repository in this plan.

---

## File Structure

- Create `src/agentharness/runtime_shadow_v1.py`: pure request issue/parse/verify functions and public bounded reason codes.
- Modify `src/agentharness/cli.py`: `shadow issue` and `shadow verify` subcommands with safe stream/path handling.
- Create `tests/test_runtime_shadow_v1.py`: contract construction and adversarial verifier coverage.
- Create `tests/test_runtime_shadow_cli.py`: CLI stream, exit-code, redaction, and command-grammar coverage.
- Modify `README.md`: one short evidence-only shadow-contract section, not a runtime setup guide.

### Task 1: Pure shadow contract and adversarial tests

**Files:**
- Create: `src/agentharness/runtime_shadow_v1.py`
- Create: `tests/test_runtime_shadow_v1.py`

**Interfaces:**
- Produces `issue_shadow_request_v1(*, request_id: str, now: datetime, challenge: str, runtime_revision: str) -> dict[str, object]`.
- Produces `verify_shadow_observation_v1(request: Mapping[str, object], observation: Mapping[str, object], *, now: datetime) -> dict[str, object]`.
- Produces `parse_shadow_json_v1(raw: bytes, *, maximum_bytes: int, document_kind: str) -> dict[str, object]` and `RuntimeShadowValidationError(code: str)`.

- [ ] **Step 1: Write focused failing contract tests**

```python
def test_valid_observation_binds_exact_request_without_execution(self):
    request = issue_shadow_request_v1(
        request_id="shadow-001",
        now=NOW,
        challenge="a" * 64,
        runtime_revision="b" * 40,
    )
    observation = valid_observation(request)
    report = verify_shadow_observation_v1(request, observation, now=NOW)
    self.assertEqual(True, report["ok"])
    self.assertEqual("not_executed", report["result_status"])
    self.assertNotIn("allow_candidate", report)

def test_changed_challenge_is_rejected_without_echoing_it(self):
    report = verify_shadow_observation_v1(REQUEST, changed_challenge(), now=NOW)
    self.assertEqual(False, report["ok"])
    self.assertEqual("shadow.binding_invalid", report["code"])
    self.assertNotIn("a" * 64, json.dumps(report))
```

Add table-driven cases for expired request, different request ID, different
runtime revision/model/tool, duplicate/extra calls, argument extra key,
oversized bytes, duplicate JSON keys, `execution_attempted: true`, status
`executed`, absolute path, each forbidden key name, and a string beginning
`sk-`.

- [ ] **Step 2: Verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_runtime_shadow_v1.py' -v`

Expected: FAIL because `agentharness.runtime_shadow_v1` does not exist.

- [ ] **Step 3: Implement the pure contract**

```python
RUNTIME_ID = "deepseek-harness"
MODEL_ID = "deepseek-v4-flash"
TOOL_NAME = "inspect_policy_summary"
NOT_EXECUTED = "not_executed"
MAX_REQUEST_BYTES = 4096
MAX_OBSERVATION_BYTES = 8192
REQUEST_TTL_SECONDS = 300

def issue_shadow_request_v1(*, request_id, now, challenge, runtime_revision):
    expires_at = now + timedelta(seconds=REQUEST_TTL_SECONDS)
    return {
        "kind": "shadow-request-v1",
        "request_id": request_id,
        "challenge": challenge,
        "runtime_id": RUNTIME_ID,
        "runtime_revision": runtime_revision,
        "model": MODEL_ID,
        "tool_name": TOOL_NAME,
        "tool_schema_digest": TOOL_SCHEMA_DIGEST,
        "policy_scope": "agentharness-shadow-poc",
        "issued_at": _utc_rfc3339(now),
        "expires_at": _utc_rfc3339(expires_at),
        "result_status": NOT_EXECUTED,
    }
```

Define `TOOL_SCHEMA` as the exact canonical JSON Schema for two required
arguments: a 64-character lowercase-hex `challenge` and literal
`policy_scope: "agentharness-shadow-poc"`, with `additionalProperties:false`.
Compute `TOOL_SCHEMA_DIGEST` and every argument/correlation digest from sorted,
compact UTF-8 JSON. Use `object_pairs_hook` to reject duplicate keys, exact
built-in `dict`/`list` types only, a depth limit of 16, and exact key sets.
The verifier recomputes the opaque expected correlation ID as SHA-256 of the
canonical request document. Return only an allow-free verification report with
`ok`, `code`, `request_id`, `runtime_id`, `model`, `tool_name`, and
`result_status`; do not copy observation values into the report.

- [ ] **Step 4: Verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_runtime_shadow_v1.py' -v`

Expected: all contract tests pass; no test writes a bytecode file.

- [ ] **Step 5: Commit the contract unit**

```bash
git add src/agentharness/runtime_shadow_v1.py tests/test_runtime_shadow_v1.py
git diff --cached --check
git commit -m "feat: verify bounded runtime shadow observations"
```

### Task 2: Safe CLI and contributor documentation

**Files:**
- Modify: `src/agentharness/cli.py`
- Create: `tests/test_runtime_shadow_cli.py`
- Modify: `README.md`

**Interfaces:**
- Consumes Task 1's pure functions.
- Produces `./agentharness shadow issue --request-id ID --runtime-revision SHA` and `./agentharness shadow verify REQUEST_PATH` with observation JSON only on stdin.

- [ ] **Step 1: Write failing CLI tests**

```python
def test_shadow_verify_emits_one_redacted_json_report(self):
    with patched_stdin(valid_observation_bytes()):
        code, stdout, stderr = invoke_cli(
            ["shadow", "verify", str(REQUEST_PATH)]
        )
    self.assertEqual(0, code)
    self.assertEqual("", stderr)
    payload = json.loads(stdout)
    self.assertEqual("shadow.verification.v1", payload["kind"])
    self.assertEqual("not_executed", payload["result_status"])

def test_shadow_verify_bad_path_never_leaks_path_or_exception(self):
    code, stdout, stderr = invoke_cli(["shadow", "verify", "/tmp/private.json"])
    self.assertEqual(2, code)
    self.assertEqual("", stderr)
    self.assertEqual("shadow.request_unreadable", json.loads(stdout)["code"])
    self.assertNotIn("/tmp/private.json", stdout)
```

Also cover oversized stdin, malformed JSON, no `--request-id`, malformed
revision, issue output's TTL, and no `--format`/external execution flags.

- [ ] **Step 2: Verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_runtime_shadow_cli.py' -v`

Expected: FAIL because the `shadow` command group is absent.

- [ ] **Step 3: Implement the minimal CLI surface and README section**

Add an exact `shadow` parser with `issue` and `verify` children. `issue` writes
one compact JSON request to stdout; `verify` reads its request with a 4097-byte
bounded file reader, reads observation from stdin with an 8193-byte bounded
reader, maps all path/JSON/internal errors to a public `shadow.*` code, and
writes one compact JSON report plus newline to stdout. `shadow verify` returns
0 only for `ok:true`; rejection returns 2 and internal failure returns 1.
**Adjudication (2026-08-19):** `shadow issue` returns 0 with the exact raw
`shadow-request-v1` document, which intentionally has no `ok` wrapper so the
external runtime can consume its strict schema unchanged.

Document only this offline contract use:

```bash
./agentharness shadow issue --request-id shadow-001 --runtime-revision <40-hex-sha> > request.json
./agentharness shadow verify request.json < observation.json
```

State that it does not launch DeepSeek Harness, load credentials, call a model,
or authorize a tool.

- [ ] **Step 4: Verify GREEN and repository compatibility**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_runtime_shadow_cli.py' -v
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
git diff --check
```

Expected: shadow-focused tests and all existing checks pass.

- [ ] **Step 5: Commit CLI and documentation**

```bash
git add src/agentharness/cli.py tests/test_runtime_shadow_cli.py README.md
git diff --cached --check
git commit -m "feat: add runtime shadow verification CLI"
```

- [ ] **Step 6: Review and final verification**

Invoke `superpowers:requesting-code-review` for both AgentHarness commits.
Resolve Critical/Important findings, then invoke
`superpowers:verification-before-completion` and rerun Task 2 Step 4 before
claiming this repository unit is ready. Do not run a paid model request from
this repository plan.
