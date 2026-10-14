# Optional Jev Sandbox Shadow Scoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in, observation-only Jev intent scorer to the independent
synthetic business sandbox without changing runtime authorization or effects.

**Architecture:** A standard-library OpenRouter adapter scores narrow typed
questions. `Conversation` observes eligible proposals before `runtime.act`,
records separate bounded assessments and rechecks context after the extra wait.
CLI and HTTP setup construct the adapter only when explicitly enabled.

**Tech Stack:** Python 3.10+, standard-library HTTPS/JSON, existing unittest
framework; no new package dependencies.

**Spec:** [Approved design](../specs/2026-10-14-jev-sandbox-shadow-design.md).

## Global Constraints

- Requested model: `typesafe/jev-1.13`; returned model:
  `typesafe/jev-1.13-20260917`; reject other versions.
- Endpoint: `https://openrouter.ai/api/alpha/decisions`; HTTPS only, official
  host only, no redirects, no retries or alternate-model fallback.
- Timeout: 10 seconds; outbound envelope: 16 KiB; response: 64 KiB.
- Labels: `fits`, `overreach`, `unclear`; confidence floor: 0.8.
- Maximum four assessments per turn; preserve the existing twelve-turn limit.
- Default-off mode does not read OpenRouter credentials, call Jev or change
  existing output shapes. `world`, `act`, `test`, `compare` never call Jev.
- A `human_review` assessment is a recommendation, not a pause or a completed
  human review. All assessments remain `result_status: not_executed`.
- Original authorization, runtime action logs, evidence receipts, transactions,
  idempotency, answers and replay do not consume model judgments.
- Implementation and commits belong to `agentharness-business-sandbox`;
  AgentHarness source and evidence contracts are not modified by this plan.
- Reuse the already authorized ignored `.env`; never copy, source or print keys,
  raw provider errors, absolute host paths or untrusted identifiers in summaries.
- Historical model reports and the twenty-four seen spike cases are not new
  blind acceptance evidence. No paid suite is required for offline integration
  acceptance. A later live acceptance run needs its own pre-call freeze.

## Review Focus

1. Permission revocation during Jev's network wait must prevent the stale
   proposal from executing (Task 2 context-change regression).
2. The scorer must not mutate proposal/history objects or leak observations
   back into planner context (Task 2 copy-isolation regression).
3. A follow-up with missing context must retain uncertainty; actor names must
   not be guessed into customer IDs (Task 1 state-projection regression).
4. Bool/NaN probabilities, wrong versions, duplicate JSON keys and oversize
   responses must be unavailable assessments, not a plausible success (Task 1).
5. CLI setup with the flag absent must never inspect OpenRouter configuration;
   explicit flag/configuration errors must be bounded and redacted (Task 3).

## Repository checkpoints and files

AgentHarness design checkpoint: `c1437ad`. External sandbox baseline:
`a22e39dbc4ed27a5459459cbb7372c2c48f74ea4`, clean `main` at planning time.
All code paths below are relative to the external sandbox checkout.

| File | Responsibility |
| --- | --- |
| `sandbox/jev_shadow.py` (new) | Credential/config validation, minimal state, versioned rubric, bounded API adapter, validated assessments |
| `sandbox/agent.py` | Optional scoring hook and post-score context check |
| `sandbox/__main__.py` | Explicit `--jev-shadow` construction and CLI disclosure |
| `sandbox/web.py` | Optional judge injection into sessions and HTTP configuration disclosure |
| `sandbox/model_eval.py` | Optional judge injection; separate Jev accounting |
| `tests/test_jev_shadow.py` (new) | Real adapter boundary behavior with transport-only doubles |
| `tests/test_agent.py` | Observation-only, context revocation, history/copy regressions |
| `tests/test_cli.py`, `tests/test_web.py`, `tests/test_model_eval.py` | Disabled and opt-in plumbing compatibility |
| `README.md`, `AGENTS.md`, `docs/jev-shadow.md` (new) | Operator instructions and approved provider boundary |

Do not restructure unrelated modules or change business rules. Do not require a
new dashboard, asynchronous worker, provider router or dependency.

## Task 1: Bounded Jev adapter

**Files:** Create `sandbox/jev_shadow.py`, `tests/test_jev_shadow.py`.

**Interfaces:**

- `load_shadow_judge(env_file=None) -> JevShadowJudge`: resolve the existing
  AgentHarness source-directory convention and ignored `.env`. Read only the
  two target entries, as literal values. Reject symlink/nonregular or >16 KiB
  files, duplicate/missing/empty entries and URL credentials/query/fragment.
  Accept official root, `/api`, `/api/v1` and the exact Decisions endpoint;
  normalize to the endpoint in Global Constraints.
- `JevShadowJudge(key: str, base_url: str)` validates configuration without
  network activity. Use existing `sandbox.agent.open_request` only if its
  redirect/timeout semantics cover this adapter unchanged; otherwise use one
  private no-redirect standard-library transport helper in this module.
- `assess(self, question: str, context: dict, proposal: dict,
  history: list) -> dict` returns a bounded assessment and never a permission.
  Its inputs must be independent copies. It performs at most one request.
- `validate_assessment(value: dict) -> dict` returns a fresh allowlisted
  assessment or raises a fixed `ValueError`; Task 2 uses it to contain faulty
  judge implementations at the observation boundary.

The assessment has `kind: jev-shadow-assessment-v1`, `result_status:
not_executed`, `status: ok|unavailable|skipped`, a fixed `jev_shadow.*` code,
`request_digest`, `proposal_digest`, `rubric_digest`, `request_attempted`,
and finite bounded `elapsed_ms`. Successful assessments additionally have
`choice`, `confidence`, `probabilities`, `triage`, pinned `model`, and validated
available `usage` fields (`cost`, `inputTokens`, `outputTokens`). Missing usage
stays missing; never invent zero billing. Only local fixed codes/labels and
validated numbers/digests appear in returned summaries.

- [x] **Step 1: Write boundary regressions.** Test a complete documented
  response and controlled invalid variants. Pin independent assertions:

  ```python
  self.assertEqual(result['choice'], 'overreach')
  self.assertEqual(result['triage'], 'flag_overreach')
  self.assertEqual(result['result_status'], 'not_executed')
  self.assertFalse(failed['request_attempted'])  # invalid state, no transport
  self.assertEqual(failed['status'], 'skipped')
  self.assertNotIn('expected', captured_payload['state'])
  self.assertNotIn('rows', captured_payload['state'])
  ```

  Cover all three labels, the exact 0.8 boundary, no-request invalid/oversized
  input, wrong model/question/label, nonfinite/bool numbers, probability sums
  and winning label, redirects, duplicate JSON, 64 KiB response bounds, HTTP
  errors and one-attempt timeout. Response failure is `unavailable`, not a
  successful overreach judgment; raw exceptions and provider bodies never
  appear in output. Verify credential parser behavior using temporary dummy
  files, including quotes, duplicates, symlinks and literal expansion text.

  Capture actual outgoing request bytes through the transport boundary. State
  contains only current user request, the most recent three previous user
  requests (max 1000 characters each), proposal, explicit meanings for all
  thirteen existing tools and trusted `actor`, `tenant`, `role` facts. No
  grants, session token, rows, operator data or full history. Do not infer
  customer IDs from actor names. Add an explicit instruction that unresolved
  references or missing mappings require `unclear`. Hash canonical JSON of
  the submitted model/state/questions envelope and original proposal. Include
  the projection version, instructions, criteria and tool meanings in the
  rubric digest. Unsupported tools yield a skipped assessment without a call.

- [x] **Step 2: Run the new tests and record expected missing-implementation
  failures.** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
  -p test_jev_shadow.py -q`. Resolve fixture/import mistakes before the red run.
- [x] **Step 3: Implement the module interfaces.** Start with the spike's
  documented wire format, not its permissive version-prefix matching or
  machine-specific paths. Reuse existing duplicate-key/depth parsing where
  appropriate. Output only sanitized local codes. Freeze a versioned rubric
  before any future live call; no live call occurs in this task.
- [x] **Step 4: Run the new tests and the sandbox complete suite.** All tests
  pass; no external model requests are made. Review focused changes and run
  `git diff --check`.
- [x] **Step 5: Commit the task in the sandbox only.** Stage exactly the two
  owned files, inspect `git diff --cached --name-only`, run
  `git diff --cached --check`, then commit
  `feat: add bounded optional Jev shadow adapter`.

## Task 2: Observation-only conversation hook

**Files:** Modify `sandbox/agent.py`, `tests/test_agent.py`.

**Interfaces:** Consume Task 1's `assess` and `validate_assessment`.
Extend `Conversation.__init__(self, planner, shadow_judge=None)`; existing
`ask(runtime, session, question)` callers stay compatible. With a judge,
return a separate `jev_shadow: list[dict]` of at most four assessments,
each with a local `proposal_index` (zero-based eligible proposal position).
Without a judge, preserve the original result keys exactly.

- [x] **Step 1: Write regressions against the real conversation loop.** Use
  the existing scripted planner and recording runtime; vary judge outputs
  between `no_flag`, `flag_overreach`, `human_review`, raised exceptions and
  invalid dictionaries. Assert these produce the same permitted action,
  runtime read/write counters and original conversation status as disabled
  mode. A runtime denial must remain a denial even when the judge says `fits`.
  Do not compare volatile timing or generated IDs as proof of equivalence.

  ```python
  self.assertEqual(result['status'], baseline['status'])
  self.assertEqual(runtime.executed_proposals, baseline_proposals)
  self.assertNotIn('jev_shadow', conversation.history[-1])
  self.assertNotIn('jev_shadow', planner.calls[-1][3][0])
  self.assertEqual(result['jev_shadow'][0]['proposal_index'], 0)
  ```

  Add a judge that changes runtime context mid-call; assert
  `context_changed`, zero executed proposals and cleared history. Add one
  that mutates its input copies; assert the original runtime proposal and
  planner history remain intact. Assert no assessment for finish, invalid
  proposals or a stalled repeated read, and at most four in a turn. Assert a
  state-projection/scoring failure records only a bounded unavailable/skipped
  assessment and does not expose exception text.
- [x] **Step 2: Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s
  tests -p test_agent.py -q`; confirm new tests fail because the hook is absent.**
- [x] **Step 3: Add the optional hook.** After current validation/stall checks,
  call the judge with copied inputs; validate and record its output outside
  `steps`/history. Recheck trusted binding after every scoring attempt before
  `runtime.act`. Keep judge construction/configuration out of `Conversation`.
  Contain unexpected observer exceptions as fixed unavailable codes; do not
  reinterpret them as policy denials or successful judgments.
- [x] **Step 4: Run agent tests, adapter tests and the complete sandbox suite.**
  Confirm all existing context-change and stalled-read regressions still pass.
- [x] **Step 5: Review and commit only `sandbox/agent.py` and
  `tests/test_agent.py`**, after exact staged-list and whitespace checks, with
  `feat: observe sandbox proposals with optional Jev scoring`.

## Task 3: Explicit CLI/HTTP plumbing and operator documentation

**Files:** Modify `sandbox/__main__.py`, `sandbox/web.py`,
`sandbox/model_eval.py`, `tests/test_cli.py`, `tests/test_web.py`,
`tests/test_model_eval.py`, `README.md`, `AGENTS.md`; create
`docs/jev-shadow.md`.

**Interfaces:** Consume `load_shadow_judge` and
`Conversation(planner, shadow_judge=None)`. Extend
`make_server(port=0, enable_writes=False, planner=None, evidence=True,
shadow_judge=None)` and
`run_model_suite(planner, split='development', evidence=True,
shadow_judge=None)` with compatible optional parameters.

- [x] **Step 1: Write opt-in plumbing regressions.** Exercise CLI parsing and
  setup with loader/transport doubles only, without starting real paid suites.
  With the flag absent, a loader that raises must never run. With the flag
  present, assert it loads once and reaches `Conversation`, `make_server` or
  `run_model_suite`. Explicit invalid configuration produces existing bounded
  `cli.failed`, never secret values or paths. Reject `serve --agent offline
  --jev-shadow` before credential loading because it cannot generate proposals.

  Exercise a real loopback server with scripted planner/judge. `/api/config`
  gains `jev_shadow_enabled` and a fixed synthetic-data/credits disclosure only
  when enabled. `/api/ask` returns assessments; `/api/act`, `/api/replay`,
  `/api/eval`, `/api/compare` never invoke the judge. Login/control resets still
  clear conversation state. Default HTTP result/configuration shapes remain
  unchanged.

  In model-evaluation tests, assert Jev assessments are reported separately
  from planner `model_calls` and token usage and do not affect `_check` or
  original pass/fail results. Derive optional Jev request count and available
  usage totals only from validated assessments, retaining missing-usage count.
  Historical suite versions and oracles remain untouched.
- [x] **Step 2: Run the CLI, HTTP and evaluator test modules; record new
  missing-option/plumbing failures.** Use unittest discovery patterns for
  `test_cli.py`, `test_web.py`, `test_model_eval.py` independently.
- [x] **Step 3: Wire `--jev-shadow` only on `ask`, `serve`, `test-model`.**
  Construct the adapter lazily in the explicit branch and pass it through the
  interfaces above. Enabled CLI results/server startup disclose that synthetic
  requests and proposals go to OpenRouter and consume credits. Update sandbox
  guidance to allow this approved pinned observation provider alongside the
  existing DeepSeek planner. Document defaults, endpoint normalization, model
  pin, usage, review-hint meaning, unavailable assessments and independent
  authorization. Add examples with the flag without printing credentials.
- [x] **Step 4: Run final verification and request independent code review.**
  Apply only reviewed fixes using TDD, then rerun affected checks. No live API
  request is necessary to claim offline integration acceptance.
- [x] **Step 5: Commit exactly the Task 3 owned paths after staged-list and
  whitespace checks**, with `feat: expose opt-in Jev sandbox shadow mode`.
  Keep AgentHarness document commits separate. Do not push, tag or publish.

## Execution setup and final verification

After the user reviews this plan and selects execution, load the selected
execution skill and `using-git-worktrees`. Honor the user's isolation choice;
if none was supplied, resolve it before creating a worktree. A worktree/temporary
checkout of the external runtime must explicitly point `AGENTHARNESS_SOURCE`
at the existing AgentHarness checkout so sibling-directory assumptions remain
correct. Do not copy `.env` into an isolated checkout. Establish a fresh sandbox
baseline before editing, and preserve any newly discovered concurrent changes.

Run in the external sandbox checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
./run-sandbox test
./run-sandbox compare
git diff --check
```

Acceptance: all unit/HTTP tests pass; offline suite 60/60; baseline and evidence
comparison arms each 60/60 with zero unauthorized successes and zero model calls.
Record the fresh actual test count; do not assume it remains 63 after additions.
Loopback test binding may require execution approval in this environment; a
sandbox permission failure is not evidence that the HTTP tests passed.

Run in AgentHarness:

```bash
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
git diff --check
```

Acceptance: policy validation, 3/3 smoke cases, both loop fixtures and the entire
test suite pass. AgentHarness evidence-contract code is unchanged, so the extra
six-module suite is required only if review discovers a justified contract change
that is separately designed and authorized.

Finish with independent review of the sandbox implementation and a separate
check of AgentHarness document accuracy. Verify actual commits, exact file lists
and worktree status. Hand off commands and validated limits; distinguish offline
integration evidence from the prior live spike. Integration into `main` follows
the finishing-branch workflow and existing user authority; no remote action is
inferred from local completion.

## Plan self-review

The three tasks cover the approved spec's runtime flow, observation contract,
configuration, bounds, model pin and compatibility requirements. Review Focus
items each have a named owning test step. Interfaces and optional parameters
match across tasks. No retained experiment runner, blind-accuracy claim, extra
provider, real-data path or execution gate is introduced. User plan review and
execution-method selection were completed on 2026-10-14; native execution in
the existing sandbox checkout was selected.

## Execution record — 2026-10-14

All three tasks completed using failed-then-passing offline regressions. Source
commits in the independent sandbox are `d6c4247` (adapter), `59a8402` (observer)
and `a670abe` (opt-in wiring and operator documentation). Implementation ended
on sandbox `main` as explicitly selected by the user; no worktree, merge or
remote action was needed. AgentHarness contains documentation only.

Final verification at sandbox `a670abe992ca8cc69f5105c48c04e27d6f1156a5`:

- Complete sandbox suite: 91/91 passed, including real loopback HTTP tests.
- Deterministic scenarios: 60/60; comparison arms each 60/60, both with zero
  unauthorized successes and zero model calls.
- AgentHarness: 538/538 tests, policy validation, 3/3 smoke cases and both
  required loop checks passed; whitespace and local document links passed.
- Existing OpenRouter configuration loaded successfully without network calls.
- Independent read-only review: no Critical or Important finding. It also ran
  adapter, conversation and CLI suites and real-runtime revocation/probability
  probes. No implementation source changed after that review.

These are session-captured offline results. The prior twenty-four live spike
cases remain historical feasibility evidence. No new live accuracy, provider
availability, cost, calibration or production authorization result is claimed.

Deferred minor: Task 1 requested every tool description in submitted state;
implementation sends only the proposed tool's meaning. All thirteen meanings
are maintained and included in the rubric digest. The reviewer found the narrow
payload adequate for this observation-only scope. The broader catalog payload
is not implemented and this discrepancy must remain visible to future readers.

The review's stale-workflow-status note is reconciled by this normal execution
record and the design checkpoint update. It required no source-code change.
