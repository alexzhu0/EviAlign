# Synthetic Data Access Lab Implementation Plan

> **For agentic workers:** Use Superpowers TDD and independent code review.

**Goal:** Deliver a runnable synthetic multi-user data-access test environment.

**Architecture:** Pure AgentHarness evidence correlation plus an independent
Python/SQLite lab that owns sessions, authorization, and local fixture reads.

**Tech Stack:** Python 3.10+, SQLite, unittest, local HTML/JS; no added dependencies.

**Spec:** `docs/superpowers/specs/2026-09-14-data-access-lab-design.md`.

## Global constraints

- Preserve existing contracts, previous cleanup changes, and external repos.
- Keep AgentHarness outputs `result_status: not_executed`.
- Never treat evidence validity as external runtime authorization.
- Use only generated in-memory fixtures; no credentials or live provider calls.
- Runtime reads require current authorization and explicit fixture-read mode.
- Run tests with `PYTHONDONTWRITEBYTECODE=1`.

## Task 1: Pure evidence contract

Files: `src/agentharness/data_access_evidence_v1.py`,
`tests/test_data_access_evidence_v1.py`.

Interfaces: `canonical_digest(value) -> str`,
`verify_data_access_evidence_v1(request, evidence, *, now: int) -> dict`.
The module CLI accepts one bounded `{request, evidence}` JSON document on stdin.

- [x] Write tests first for a literal valid request/receipt, each binding
  mutation, time boundaries, policy deny, malformed shapes, unknown fields,
  duplicate JSON keys, oversized/deep input and non-disclosing error output.
- [x] Run `python3 -m unittest -q tests.test_data_access_evidence_v1` and observe
  failure before adding implementation.
- [x] Implement the finite contract and stable output described in the spec.
  Serialize with `json.dumps(value, sort_keys=True, separators=(",", ":"),
  ensure_ascii=True, allow_nan=False)`; compare all receipt fields exactly.
- [x] Run the targeted tests until green and review the new pure module.

## Task 2: External fixture runtime and cases

Files in standalone lab: `lab/runtime.py`, `lab/planner.py`, `lab/cases.py`,
`tests/test_runtime.py`, `tests/test_planner.py`, `pyproject.toml`, `lab/__init__.py`.

Interfaces: `LabRuntime(enable_fixture_reads=False)`;
`new_session(actor) -> str`; `prepare(session, proposal) -> str`;
`execute(session, ticket) -> dict`; `ask(session, question) -> dict`;
`run_cases() -> dict` with literal expected outcomes and real SQL counts.

- [x] Write failing own-row, cross-user, tenant, field, summary, masking,
  revocation, replay, tamper, mode-off, and query-count tests.
- [x] Implement fixed fixture seed, finite authorization and parameterized SQL.
- [x] Implement bounded rule-based proposal generation and ambiguity rejection.
- [x] Run external unittests and matrix; verify errors never return data.

## Task 3: Manual test interface

Files in standalone lab: `lab/web.py`, `lab/__main__.py`, `static/index.html`,
`tests/test_web.py`, `README.md`, `run-lab`.

- [x] Write HTTP tests for sessions, ask, unknown input, body limits and origin.
- [x] Implement loopback server and CLI with the spec's explicit read-mode flag.
- [x] Add a compact Chinese interface with identity selection, questions,
  separate proposal/evidence/runtime/result views and acceptance-case table.
- [x] Exercise customer success, customer denial, support masking, analyst
  totals, identity switching and case runner in a browser if available.

## Task 4: Review, install and handoff

- [x] Run AgentHarness required six commands and evidence six-module suite.
- [x] Run lab unittests and acceptance matrix; verify frontend session flows.
- [x] Obtain independent review of the evidence contract and external runtime;
  fix material findings before enabling the local synthetic read demo.
- [x] Install the standalone lab as a sibling project if permitted, then start
  its loopback-only server and verify the final URL and launch command.
- [x] Record test evidence and provide a short reproducible user guide.

## Rulings

- The user approved the preceding roles/scenario and requested implementation;
  continue within that scope without a repeated design-approval question.
- Default to the browser entry point plus CLI while the optional UI preference
  is unanswered. The first Agent is visibly offline and rule-based.
- Existing Git metadata writes are restricted; keep reviewable working-tree
  changes and separate lab source, without committing or publishing.

## Verification record — 2026-09-14

- AgentHarness policy validation, PI-001/PD-001/SEC-001 evaluation, and both
  example loop checks passed. Full unittest discovery: **529 passed**.
- Existing evidence-contract six-module regression suite: **150 passed**.
- External lab unittest discovery: **33 passed**, including real loopback HTTP
  tests. Acceptance matrix: **28/28 passed** with exact expected rows and
  observed SQLite SELECT counts.
- Independent review found a parser that could broaden an unknown-customer
  request. Failing regressions preceded a finite anchored grammar fix; unknown
  customers and mixed intents now fail closed, and Chinese tenant names retain
  their explicit scope. Review also caught misleading execution-failure UI text;
  the UI now preserves the runtime's actual execution status and query count.
- A disconnected-request regression failed before fixed-code server logging
  was added. The final independent review reported no remaining actionable
  findings in the reviewed files.
- Installed and initialized the standalone runtime repository at
  `../agentharness-data-access-lab`; no commit, push or publication was made.
- Headless Chrome exercised the installed server on `127.0.0.1:8765`: own rows,
  cross-user denial, masked contact, cross-tenant denial, analyst total, session
  switching/cleared output, and the 28-case button all passed. An injected
  execution-failure result rendered honestly. Desktop and 390px mobile views
  were inspected; no page-level horizontal overflow was observed.
- The browser acceptance script and screenshots are local `/tmp` verification
  artifacts, not repository source or production evidence. The test Chrome was
  closed; the loopback lab server was left running for the user.
- `git diff --check` passed. Prior cleanup changes remain separate in the
  working tree; unrelated files were not staged.

This verifies a synthetic-only, offline rule-Agent laboratory. It does not
verify a real LLM, production authentication, or real-data execution authority.
