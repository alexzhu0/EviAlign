# AgentHarness

AgentHarness is a pre-execution evidence control-plane for agent actions.

Current prerelease: **v0.2.0-alpha.1**. This GitHub source prerelease does not
publish a PyPI or npm package.

Latest source milestone (2026-09-09): the bounded shadow request/verifier CLI
is implemented, and the separate DeepSeek runtime completed one live synthetic
evidence round trip. Offline acceptance passed 515 AgentHarness tests and 158
external shadow tests. This source milestone is newer than the tagged prerelease;
it does not add business-tool execution. Start with the
[current handoff](docs/30-deepseek-shadow-handoff.md) and
[milestone record](release/2026.09.09.md).

AgentHarness validates, binds, and exports evidence. Its finite methodology
pilot emits one exact `permit_once` evidence decision; that value has no
in-repo execution effect and is not runtime approval. In the accepted
cross-repository pilot, a trusted, version-pinned, admission-controlled Pi/Win9
extension separately consumed that evidence for one local read-only action.
That external runtime behavior is not general runtime authorization. It adds no
extension sandbox and does not prevent Pi extensions from using their existing
process or network capabilities. Pi companion code is not included in this
repository release.

The goal is **not** to copy leaked or reverse-engineered prompts. The goal is to extract reusable engineering patterns and turn them into policy-driven, testable, auditable agent control-plane and runtime-boundary assets.

## Core Idea

Modern agents are not just models plus prompts. They are operating systems around models:

```text
User Task
  ↓
Instruction Hierarchy Resolver
  ↓
Planner / State Machine
  ↓
Tool Router
  ↓
Approval Gate
  ↓
[external runtime] Tool Execution / Sandbox
  ↓
Verifier / Eval Hooks
  ↓
Audited User-facing Response
```

AgentHarness treats pre-execution evidence controls as **policy-as-code**:

```text
agent_policy.yaml
  → prompt compiler
  → evidence policy
  → tool eligibility
  → safety evals
  → audit evidence
```

## Four Core Assets

### 1. Agent Design Pattern Library

Entry point: [`docs/01-agent-design-pattern-library.md`](docs/01-agent-design-pattern-library.md)

Machine-readable seed: [`patterns/agent_design_patterns.yaml`](patterns/agent_design_patterns.yaml)

This asset extracts reusable agent OS patterns:

- layered agent architecture
- instruction hierarchy resolver
- search-before-edit
- tool preference hierarchy
- approval gate for side effects
- verification loop
- planner / execution mode split
- event stream as source of truth
- memory write boundary
- untrusted corpus neutralization
- policy as code

### 2. Tool Governance Policy

Entry point: [`docs/02-tool-governance-policy.md`](docs/02-tool-governance-policy.md)

Machine-readable seed: [`policies/tool_governance.yaml`](policies/tool_governance.yaml)

This asset defines how tools should be classified, routed, approved and audited.

It covers:

- search tools
- file read/write/delete tools
- shell tools
- database tools
- git tools
- browser tools
- deployment tools
- secret tools
- memory tools
- external communication tools

### 3. Agent Safety Eval Suite

Entry point: [`docs/03-agent-safety-eval-suite.md`](docs/03-agent-safety-eval-suite.md)

Machine-readable seed: [`evals/agent_safety_eval_suite.yaml`](evals/agent_safety_eval_suite.yaml)

This asset turns safety and governance principles into regression tests.

It covers:

- prompt injection
- hidden instruction disclosure
- destructive operations
- database mutation
- secret handling
- unverified code edits
- dependency hallucination
- external communication
- memory pollution
- fake tool-call injection
- source freshness and citation
- CI repair limits

### 4. Prompt / Policy Compiler

Entry point: [`docs/04-prompt-policy-compiler.md`](docs/04-prompt-policy-compiler.md)

Conceptual schema: [`schemas/agent_policy.schema.yaml`](schemas/agent_policy.schema.yaml)

Example policy: [`examples/agent_policy.example.yaml`](examples/agent_policy.example.yaml)

This asset describes how to compile structured policy into:

- provider-specific system prompts
- runtime tool policies
- approval gates
- sandbox policies
- eval suites
- audit schemas

## Asset Map

Start here: [`docs/00-asset-map.md`](docs/00-asset-map.md)

Runtime architecture: [`docs/06-runtime-architecture.md`](docs/06-runtime-architecture.md)

Enterprise positioning and boundary audit: [`docs/07-enterprise-positioning-and-boundary-audit.md`](docs/07-enterprise-positioning-and-boundary-audit.md)

Glossary and product contract: [`docs/08-glossary-and-product-contract.md`](docs/08-glossary-and-product-contract.md)

Source-backed integration strategy: [`docs/09-source-backed-integration-strategy.md`](docs/09-source-backed-integration-strategy.md)

Enterprise audit report and buyer demo: [`docs/10-enterprise-audit-report-and-buyer-demo.md`](docs/10-enterprise-audit-report-and-buyer-demo.md)

Reproducible enterprise demo: [`docs/11-reproducible-enterprise-demo.md`](docs/11-reproducible-enterprise-demo.md)

Buyer/reviewer decision guide: [`docs/12-buyer-reviewer-decision-guide.md`](docs/12-buyer-reviewer-decision-guide.md)

External reviewer checklist: [`docs/13-external-reviewer-checklist.md`](docs/13-external-reviewer-checklist.md)

Reviewer dry-run and reproducibility: [`docs/14-reviewer-dry-run-and-reproducibility.md`](docs/14-reviewer-dry-run-and-reproducibility.md)

Development loop operating model: [`docs/15-agentharness-development-loop-operating-model.md`](docs/15-agentharness-development-loop-operating-model.md)

Phase E release readiness and packaging audit: [`docs/16-phase-e-release-readiness-and-packaging-audit.md`](docs/16-phase-e-release-readiness-and-packaging-audit.md)

Pi integration boundary and contract planning doc only, not live Pi integration: [`docs/17-pi-integration-boundary-and-contract.md`](docs/17-pi-integration-boundary-and-contract.md)

Pi tool-call mapping static fixture doc only, not live Pi integration: [`docs/18-pi-tool-call-mapping-fixture.md`](docs/18-pi-tool-call-mapping-fixture.md)

Pi contract-check CLI doc for static fixture validation only, not live Pi integration: [`docs/19-pi-contract-check-cli.md`](docs/19-pi-contract-check-cli.md)

Pi dual-repo dry-run E2E doc for opt-in local wiring only, not runtime allow: [`docs/20-pi-dual-repo-dry-run-e2e.md`](docs/20-pi-dual-repo-dry-run-e2e.md)

Historical T040 controlled fake-read PoC evidence records one positive fake
read execution. Accepted T056 evidence-integrity review supersedes that behavior
with a block-only baseline: all tested cases block and fake-tool execution stays
at zero:
[`docs/21`](docs/21-pi-controlled-read-only-poc.md)

Pi integration readiness pause review, not real execution approval:
[`docs/22`](docs/22-pi-integration-readiness-pause-review.md)

Pi milestone packaging audit, not a commit or release:
[`docs/23`](docs/23-pi-milestone-packaging-audit.md)

Pi observation/evidence contract v1, evidence-only and not runtime allow:
[`docs/24`](docs/24-pi-observation-evidence-contract-v1.md)

Pi runtime-authorization readiness ADR, currently NO-GO and NOT IMPLEMENTED:
[`docs/25`](docs/25-pi-runtime-authorization-readiness-adr.md)

Historical T061 no-commit milestone packaging handoff:
[`docs/26`](docs/26-agentharness-pi-shadow-milestone-packaging.md)

T062 runtime-authorization Phase-0 preflight, derivative and still NO-GO:
[`docs/27`](docs/27-pi-runtime-authorization-phase0-preflight.md)

Official `v0.2.0-alpha.1` GitHub source prerelease notes:
[`release/2026.07.20.md`](release/2026.07.20.md)

Pi V4 trusted-publication continuity record, deployment-integrity planning only
and not runtime authorization:
[`docs/28`](docs/28-pi-v4-publication-continuity.md)

Current AgentHarness-only local maintenance closure:
[`docs/29`](docs/29-agentharness-maintenance-closure.md)

Current business-sandbox maintenance handoff and real-data pilot boundary:
[`docs/32`](docs/32-business-sandbox-maintenance-handoff.md)

Latest local release record, dated 2026-08-13:
[`release/2026.08.13.md`](release/2026.08.13.md)

Historical 2026-07-13 documentation/package handoff note:
[`release/2026.07.13.md`](release/2026.07.13.md)

Complete local release-record index, newest first:
[`release/README.md`](release/README.md)

Repository maintenance and verification rules:
[`AGENTS.md`](AGENTS.md)

Development workflow: new work uses Superpowers only. See
[`AGENTS.md`](AGENTS.md) and the
[WSL migration design](docs/superpowers/specs/2026-08-13-omx-to-superpowers-migration-design.md).
Historical OMX references document earlier work and are not active workflow
instructions.

Enterprise audit report schema: [`schemas/enterprise_audit_report.schema.yaml`](schemas/enterprise_audit_report.schema.yaml)

Enterprise audit checklist schema: [`schemas/enterprise_audit_checklist.schema.yaml`](schemas/enterprise_audit_checklist.schema.yaml)

End-to-end evidence-chain regression harness: [`tests/test_end_to_end_evidence_chain.py`](tests/test_end_to_end_evidence_chain.py)

## Minimal Executable Loop

AgentHarness includes a small local CLI for keeping the YAML assets honest:

```bash
./agentharness validate examples/agent_policy.example.yaml
./agentharness eval --cases PI-001,PD-001,SEC-001
./agentharness loop check examples/agent_bus
./agentharness loop check examples/agent_bus_tool_gate
./agentharness loop check examples/agent_bus_approval
./agentharness loop check examples/agent_bus_preflight
./agentharness loop check examples/agent_bus_handoff
./agentharness loop check examples/agent_bus_adapter_registry
./agentharness handoff inspect examples/agent_bus_handoff
./agentharness handoff inspect examples/agent_bus_adapter_registry
./agentharness handoff inspect examples/agent_bus_handoff --json
./agentharness handoff inspect examples/agent_bus_adapter_registry --json
./agentharness handoff export examples/agent_bus_adapter_registry
./agentharness handoff manifest examples/agent_bus_adapter_registry
./agentharness handoff manifest examples/agent_bus_adapter_registry > /tmp/agentharness-manifest.json
./agentharness handoff verify-manifest examples/agent_bus_adapter_registry /tmp/agentharness-manifest.json
./agentharness audit report examples/agent_bus_adapter_registry
./agentharness audit checklist examples/agent_bus_adapter_registry
./agentharness audit report examples/agent_bus_adapter_registry > /tmp/agentharness-audit-report.json
./agentharness audit verify-report examples/agent_bus_adapter_registry /tmp/agentharness-audit-report.json
./agentharness pi contract-check examples/pi_tool_call_mapping/pi_tool_call_observations.json examples/pi_tool_call_mapping/expected_mapping.json examples/agent_bus_adapter_registry
./agentharness pi evidence-evaluate-v1 examples/agent_bus_adapter_registry < request.json
./agentharness pi methodology-permit-v1 < request.json
```

### Offline Runtime Shadow Contract

The offline-only runtime shadow contract issues a bounded request and verifies
one bounded observation. It is evidence-only and preserves
`result_status: not_executed`:

```bash
./agentharness shadow issue --request-id shadow-001 --runtime-revision <40-hex-sha> > request.json
./agentharness shadow verify request.json < observation.json
```

This feature does not launch DeepSeek Harness, load credentials, call a model,
or authorize a tool. It has no external runtime invocation or policy-allow
decision surface.

The separately maintained DeepSeek Harness shadow pilot completed one live
model request and AgentHarness verification on 2026-09-09. This validates the
fixed `inspect_policy_summary` evidence path only. For the current checkpoints,
credential-update procedure, failure interpretation, and next development step,
see the [shadow handoff and runbook](docs/30-deepseek-shadow-handoff.md) and
[local milestone record](release/2026.09.09.md).

### Synthetic Data Access Lab

A separate local lab exercises synthetic customer/order queries across customer,
support, and analyst identities. AgentHarness verifies bounded pre-execution
evidence; the external lab independently authorizes and performs fixture reads.
The default Agent is a rule-based offline simulator, not a live model. See the
[lab guide](docs/31-synthetic-data-access-lab.md) for launch and test instructions.

### Business Sandbox

The separate `agentharness-business-sandbox` runtime expands the synthetic lab
to correlated orders, payments, refunds, shipments, tickets, documents, events,
role changes, approvals and reversible simulated writes. AgentHarness supplies
the bounded `business-action-evidence-v1` correlation check; the external
runtime retains identity, authorization, transaction and execution ownership.
See the [contract](docs/business-action-evidence-v1.md) and the
[current handoff](docs/32-business-sandbox-maintenance-handoff.md).

The accepted synthetic result is a development checkpoint. It does not validate
real SSO, production databases, real payments, production authorization or
internal adoption. The next recommended experiment is one low-risk, read-only
shadow pilot against a single internal data source.

### Declarative Safety Evaluations

The local evaluator has a compatibility default for the original smoke cases,
plus explicit selectors and deterministic machine-readable reports:

```bash
./agentharness eval
./agentharness eval --all
./agentharness eval --tags secret-handling
./agentharness eval --all --format json
./agentharness eval --tags secret-handling --format junit
```

Evaluators and assertion operations are finite Python registries. Suite YAML is
data only and cannot execute code. The command involves no model, network,
tool, or runtime authorization; it evaluates policy controls against bounded
local fixtures. Only cases that carry the complete declarative contract
(`title`, `tags`, `evaluator`, `input`, `assertions`, and `pass_message`) are
executable. Narrative-only suite cases remain documentation rather than eval
workloads.

## Continuous Integration

[![CI](https://github.com/alexzhu0/AgentHarness/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alexzhu0/AgentHarness/actions/workflows/ci.yml)

The CI workflow runs on pull requests and pushes to `main`, using a Python 3.10,
Python 3.11, and Python 3.12 matrix. Reproduce its local verification sequence
with:

```bash
python -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
mkdir -p artifacts
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --all --format junit > artifacts/eval-results.xml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --all --format json > artifacts/eval-results.json
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -q
git fetch origin main
git diff --check origin/main...HEAD
```

Failure-only 14-day report artifacts are retained when both reports were
generated. If either report is missing, CI fails a missing-evidence check before
upload.

CI is not runtime authorization and does not execute Agent Runtime tools.

The loop check command validates an existing file-bus directory against the
loop protocol. It does not create, mutate, schedule, or execute tasks.

The handoff inspect command validates the file bus first, then reads
`execution_handoff_report_path` references from `designer_review` events and
prints handoff readiness summaries. It is read-only: it does not call runtime
adapters, mutate task state, or execute tools.

The handoff export command validates the file bus first, then emits a
deterministic JSON package for registry-backed, handoff-ready entries only. It
writes JSON to stdout only; direct legacy `adapter_spec_path` handoff fixtures
still validate but do not export.

The handoff manifest command builds on that export package and emits a
digest-addressed JSON manifest to stdout only. It names the full package and
each exported ready item by canonical SHA-256 digest while preserving
`result_status: not_executed`.

The handoff verify-manifest command reads a saved T012 manifest JSON file,
regenerates the expected manifest from the current bus, and emits a
deterministic verification report to stdout on both pass and fail. It is a
readback check, not a trust or runtime execution surface.

The audit report command composes handoff inspection, registry-backed export,
and digest manifest evidence into one deterministic enterprise audit JSON
report. It writes JSON to stdout only, does not call manifest readback without a
saved manifest path, self-checks the payload against the repo-native enterprise
audit report schema, and keeps `result_status: not_executed`.

The audit checklist command emits a deterministic goal/check status report
for reviewer convenience. It summarizes file-bus validation, handoff inspection,
registry-backed export, digest manifest, enterprise audit report self-check,
and manual saved-artifact readback steps. It self-checks the payload against
the repo-native enterprise audit checklist schema, writes JSON to stdout only,
and keeps every checklist item `result_status: not_executed`.

The audit verify-report command reads a saved enterprise audit report JSON,
validates it with the repo-native audit report payload validator, regenerates
the current report from the file bus, and emits deterministic readback
verification JSON to stdout. It is not runtime execution, adapter invocation,
signing, timestamping, trust-root behavior, task dispatch, or file-output mode.

The pi contract-check command runs the T036 static Pi-like mapping validator
over observation and expectation fixtures plus the registry-backed bus. It
emits `pi_tool_call_mapping_validation_report` JSON to stdout only, returns 0
only when `ok:true`, and keeps `allow_candidate` as candidate evidence rather
than runtime allow or safe-to-execute approval.

The pi evidence-evaluate-v1 command reads one bounded observation request from
stdin, binds it to one captured AgentHarness evidence snapshot, and emits one
deterministic JSON response. It never executes the observed tool and preserves
`result_status: not_executed`.

The pi methodology-permit-v1 command evaluates the exact finite methodology
pilot request from bounded stdin. A matching request emits `permit_once` as
evidence for external runtime verification; it does not read the pinned
artifact, consume the permit, or execute a tool in this repository.

## File-Bus Loop MVP

AgentHarness now includes a protocol-first file-bus loop MVP for two Codex terminals coordinating through repository files.

- Protocol: [`docs/05-loop-file-bus.md`](docs/05-loop-file-bus.md)
- Runtime architecture: [`docs/06-runtime-architecture.md`](docs/06-runtime-architecture.md)
- Conceptual task schema: [`schemas/loop_task.schema.yaml`](schemas/loop_task.schema.yaml)
- Versioned fixtures: [`examples/agent_bus/`](examples/agent_bus/)
- Tool gate fixture: [`examples/agent_bus_tool_gate/`](examples/agent_bus_tool_gate/)
- Approval record fixture: [`examples/agent_bus_approval/`](examples/agent_bus_approval/)
- Execution preflight fixture: [`examples/agent_bus_preflight/`](examples/agent_bus_preflight/)
- Execution handoff fixture: [`examples/agent_bus_handoff/`](examples/agent_bus_handoff/)
- Adapter registry fixture: [`examples/agent_bus_adapter_registry/`](examples/agent_bus_adapter_registry/)
- Validation helpers: [`src/agentharness/loop_bus.py`](src/agentharness/loop_bus.py)
- Tool gate reports: [`src/agentharness/tool_gate.py`](src/agentharness/tool_gate.py)
- Approval records: [`src/agentharness/approval_record.py`](src/agentharness/approval_record.py)
- Execution preflight: [`src/agentharness/execution_preflight.py`](src/agentharness/execution_preflight.py)
- Execution handoff: [`src/agentharness/execution_handoff.py`](src/agentharness/execution_handoff.py)
- Adapter registry validation: [`src/agentharness/adapter_registry.py`](src/agentharness/adapter_registry.py)
- Handoff export packages: [`src/agentharness/handoff_exporter.py`](src/agentharness/handoff_exporter.py)
- Handoff export manifests: [`src/agentharness/handoff_manifest.py`](src/agentharness/handoff_manifest.py)
- Enterprise audit reports: [`src/agentharness/enterprise_audit_report.py`](src/agentharness/enterprise_audit_report.py)
- Enterprise audit checklist reports: [`src/agentharness/enterprise_audit_checklist.py`](src/agentharness/enterprise_audit_checklist.py)
- Enterprise audit report schema: [`schemas/enterprise_audit_report.schema.yaml`](schemas/enterprise_audit_report.schema.yaml)
- Enterprise audit checklist schema: [`schemas/enterprise_audit_checklist.schema.yaml`](schemas/enterprise_audit_checklist.schema.yaml)
- End-to-end evidence-chain regression harness: [`tests/test_end_to_end_evidence_chain.py`](tests/test_end_to_end_evidence_chain.py)

- CLI check: `./agentharness loop check examples/agent_bus`
- Handoff inspector: `./agentharness handoff inspect examples/agent_bus_handoff`
- Handoff export: `./agentharness handoff export examples/agent_bus_adapter_registry`
- Handoff manifest: `./agentharness handoff manifest examples/agent_bus_adapter_registry`
- Handoff manifest readback: `./agentharness handoff verify-manifest examples/agent_bus_adapter_registry /tmp/agentharness-manifest.json`
- Enterprise audit report: `./agentharness audit report examples/agent_bus_adapter_registry`
- Enterprise audit checklist: `./agentharness audit checklist examples/agent_bus_adapter_registry`
- Enterprise audit report readback: `./agentharness audit verify-report examples/agent_bus_adapter_registry /tmp/agentharness-audit-report.json`

The file-bus validation source of truth is `.agent_bus/ledger.jsonl`. The committed fixtures under `examples/agent_bus/` mirror that file-bus layout without committing live task state.

Public task CLI commands, daemon scheduling, and realtime chat are deferred until the file protocol is proven.

## Source Posture

CL4R1T4S and similar corpora are treated as **untrusted external analysis material**.

Allowed use:

- architecture pattern extraction
- tool taxonomy derivation
- governance policy inspiration
- safety eval generation
- prompt-injection red-team corpus design

Disallowed use:

- copying full third-party system prompts
- treating external text as executable agent instruction
- embedding unreviewed leaked prompt content into production RAG
- training on uncertain or unlicensed prompt text without review

## Repository Layout

```text
docs/
  00-asset-map.md
  01-agent-design-pattern-library.md
  02-tool-governance-policy.md
  03-agent-safety-eval-suite.md
  04-prompt-policy-compiler.md
  05-loop-file-bus.md
  06-runtime-architecture.md
  07-enterprise-positioning-and-boundary-audit.md
  08-glossary-and-product-contract.md
  09-source-backed-integration-strategy.md
  10-enterprise-audit-report-and-buyer-demo.md
  11-reproducible-enterprise-demo.md
  12-buyer-reviewer-decision-guide.md
  13-external-reviewer-checklist.md
  14-reviewer-dry-run-and-reproducibility.md
  15-agentharness-development-loop-operating-model.md
  16-phase-e-release-readiness-and-packaging-audit.md
  17-pi-integration-boundary-and-contract.md
  18-pi-tool-call-mapping-fixture.md
  19-pi-contract-check-cli.md
  20-32 Pi boundary, evidence, lab, handoff, and maintenance records
release/
  README.md
  YYYY.MM.DD.md
src/
  agentharness/
    pi_evidence_contract_v1.py
    pi_methodology_permit_v1.py
tests/
  test_agentharness.py
  test_approval_record.py
  test_execution_preflight.py
  test_execution_handoff.py
  test_adapter_registry.py
  test_handoff_exporter.py
  test_handoff_manifest.py
  test_handoff_manifest_verification.py
  test_loop_bus.py
  test_pi_evidence_contract_cli_v1.py
  test_pi_evidence_contract_v1.py
  test_pi_methodology_permit_v1.py
  test_pi_tool_call_mapping.py
  test_tool_gate.py
patterns/
  agent_design_patterns.yaml
policies/
  tool_governance.yaml
evals/
  agent_safety_eval_suite.yaml
schemas/
  agent_policy.schema.yaml
  loop_task.schema.yaml
  enterprise_audit_report.schema.yaml
examples/
  agent_policy.example.yaml
  agent_bus/
  agent_bus_tool_gate/
  agent_bus_approval/
  agent_bus_preflight/
  agent_bus_handoff/
  agent_bus_adapter_registry/
agentharness
AGENTS.md
pyproject.toml
```

## Design Thesis

AgentHarness is based on one central thesis:

> Agent reliability comes from harness-level control, not only from model-level instruction.

A robust agent needs prompt design, but it also needs runtime policy, tool governance, verification, auditability and safety evals.
