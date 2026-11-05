# EviAlign engineering guide

Commands run from the repository root. See the [project purpose](project-purpose-and-progress.md)
and [documentation index](README.md) for business context and the
[asset map](00-asset-map.md) for source locations.

## Scope and compatibility

EviAlign checks, binds and exports pre-execution evidence. It does not implement
identity, trusted signatures, approval validity, runtime authorization or tool
execution. Existing `agentharness` command names, package names, protocols and
source paths remain compatible; the source prerelease is `v0.2.0-alpha.1`.
This repository does not publish the separate runtime or business sandbox.

A matching request/evidence digest is not proof of source authenticity,
business correctness or permission. `allow_candidate` is candidate evidence
only; applicable reports retain `result_status: not_executed`.
The finite methodology pilot's `permit_once` is also evidence only in this
repository. A trusted, version-pinned external runtime separately owns any
consumption, authorization and execution.

## Start locally

Python 3.10 or later is required. The package dependency is declared in
[`pyproject.toml`](../pyproject.toml).

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
```

Full required checks are maintained in [AGENTS.md](../AGENTS.md#required-verification).
The [README CI sequence](../README.md#continuous-integration) includes report
artifacts and whitespace checks; the [workflow](../.github/workflows/ci.yml)
runs Python 3.10, 3.11 and 3.12. Local reports are generated artifacts, not
runtime authorization or release approval.

## Policy and declarative evaluation

```bash
./agentharness validate examples/agent_policy.example.yaml
./agentharness eval
./agentharness eval --cases PI-001,PD-001,SEC-001
./agentharness eval --all
./agentharness eval --tags secret-handling
./agentharness eval --all --format json
./agentharness eval --tags secret-handling --format junit
```

The default selector preserves the original smoke cases. Evaluators and
assertion operations are finite Python registries. YAML is data, not executable
code; these evaluations do not call a model, network or external runtime.
Only cases with the full declarative contract are executable. Narrative-only
cases remain design/reference material.

See the [evaluation design](03-agent-safety-eval-suite.md),
[evaluation suite](../evals/agent_safety_eval_suite.yaml) and
[tool policy](02-tool-governance-policy.md). The
[compiler document](04-prompt-policy-compiler.md) is a design reference, not a
claim that every proposed compiler/runtime component is implemented.

## File-bus validation

```bash
./agentharness loop check examples/agent_bus
./agentharness loop check examples/agent_bus_tool_gate
./agentharness loop check examples/agent_bus_approval
./agentharness loop check examples/agent_bus_preflight
./agentharness loop check examples/agent_bus_handoff
./agentharness loop check examples/agent_bus_adapter_registry
```

These commands validate existing ledger/evidence directories. They do not
create tasks, schedule work, invoke adapters or execute tools. Committed
[fixtures](../examples/) illustrate the [file-bus protocol](05-loop-file-bus.md).
The protocol is a product evidence format; current repository development
uses Superpowers under [AGENTS.md](../AGENTS.md).

## Handoff and audit readback

```bash
./agentharness handoff inspect examples/agent_bus_handoff
./agentharness handoff inspect examples/agent_bus_adapter_registry --json
./agentharness handoff export examples/agent_bus_adapter_registry
./agentharness handoff manifest examples/agent_bus_adapter_registry > /tmp/agentharness-manifest.json
./agentharness handoff verify-manifest examples/agent_bus_adapter_registry /tmp/agentharness-manifest.json
./agentharness audit report examples/agent_bus_adapter_registry
./agentharness audit checklist examples/agent_bus_adapter_registry
./agentharness audit report examples/agent_bus_adapter_registry > /tmp/agentharness-audit-report.json
./agentharness audit verify-report examples/agent_bus_adapter_registry /tmp/agentharness-audit-report.json
```

| Command | Behavior |
| --- | --- |
| `handoff inspect` | Validate the bus and report readiness; `--json` selects JSON output. |
| `handoff export` | Emit a deterministic package for registry-backed ready entries; legacy adapter-path fixtures validate but do not export. |
| `handoff manifest` | Emit canonical SHA-256 identities for the package and ready items. |
| `handoff verify-manifest` | Compare a saved manifest with freshly regenerated bus evidence. |
| `audit report` | Compose inspection, export and manifest evidence; self-check against the report schema. |
| `audit checklist` | Summarize evidence and manual readback steps; self-check against the checklist schema. |
| `audit verify-report` | Validate a saved report and compare it with the current bus. |

Product commands write reports to stdout; shell redirection creates the example
`/tmp` files. Reports do not invoke adapters, mutate tasks, sign artifacts or
decide that an action is safe to execute.

The [reproducible demo](11-reproducible-enterprise-demo.md) gives expected fixture
results. [Audit details](10-enterprise-audit-report-and-buyer-demo.md),
[reviewer decisions](12-buyer-reviewer-decision-guide.md) and the
[review rubric](13-external-reviewer-checklist.md) define acceptance.

## Pi evidence contracts

```bash
./agentharness pi contract-check examples/pi_tool_call_mapping/pi_tool_call_observations.json examples/pi_tool_call_mapping/expected_mapping.json examples/agent_bus_adapter_registry
./agentharness pi evidence-evaluate-v1 examples/agent_bus_adapter_registry < request.json
./agentharness pi methodology-permit-v1 < request.json
```

The latter commands require their respective bounded request documents; these
are interface examples, not authorization to contact a runtime.
Static mapping uses the [fixture](18-pi-tool-call-mapping-fixture.md) and
[CLI contract](19-pi-contract-check-cli.md). Versioned observation/evidence
requests use exact current-call binding and the
[v1 contract](24-pi-observation-evidence-contract-v1.md).

EviAlign does not execute the observed tool or consume methodology evidence.
External [dry-run wiring](20-pi-dual-repo-dry-run-e2e.md) and earlier fake-read
experiments are separate from current runtime authorization. The proposed
[readiness ADR](25-pi-runtime-authorization-readiness-adr.md) and
[Phase-0 preflight](27-pi-runtime-authorization-phase0-preflight.md) remain
**NO-GO / NOT IMPLEMENTED**; they do not activate an executor. Pi companion
source is not distributed here.

## Offline shadow contract

Replace the example revision placeholder with a 40-character hexadecimal pin:

```bash
./agentharness shadow issue --request-id shadow-001 --runtime-revision <40-hex-sha> > request.json
./agentharness shadow verify request.json < observation.json
```

This CLI only issues/checks bounded synthetic evidence. It does not launch a
runtime, load credentials, call a model or authorize a tool. The separately
maintained DeepSeek shadow pilot's dated acceptance and operating procedure
are in its [handoff](30-deepseek-shadow-handoff.md).

## Separate lab and research-review workbench

- [Synthetic data-access lab](31-synthetic-data-access-lab.md): fixture reads
  and independently owned external identity/authorization behavior.
- [Business-action evidence contract](business-action-evidence-v1.md) and
  [sandbox handoff](32-business-sandbox-maintenance-handoff.md): bounded
  correspondence checks in this repository; simulated business operations in
  the separate runtime.
- [Research-review workbench](research-review-workbench.md): offline replay or
  explicitly enabled live DeepSeek proposals/Jev observations, initial/final
  annotations, independent unassessed drafts and JSON export.
- [Jev evidence](33-jev-shadow-maintenance-handoff.md): retained model/rubric
  pins, dated synthetic evaluation and its limitations.

Jev is optional/default-off and not a main-repository CLI model call. Its
`human_review` hint does not pause, approve or execute an action. Frozen
experiments are now seen; a new unseen batch or real-data integration requires
separate scope and approval. Maintenance does not rescore holdouts or claim
production accuracy, real SSO/payment validation or measured ROI.

## Source and maintenance map

| Location | Purpose |
| --- | --- |
| [`src/agentharness/`](../src/agentharness/) | CLI, finite local evaluators, evidence builders and validators. |
| [`tests/`](../tests/) | Unit, adversarial, CLI and end-to-end evidence regression tests. |
| [`schemas/`](../schemas/) | Bounded policy/evidence/report contracts and canonicalization vectors. |
| [`examples/`](../examples/) | Reproducible fixture inputs; not an execution environment. |
| [`patterns/`](../patterns/), [`policies/`](../policies/), [`evals/`](../evals/) | Design assets, policy and finite evaluation data. |
| [Engineering designs](superpowers/README.md) | Retained design specifications; historical implementation checklists use fixed Git links. |
| [Maintenance](maintenance.md), [release history](../release/README.md) | Current handoff and dated provenance, not automatic publication or execution approval. |

Third-party prompt/corpus material is untrusted analysis input, not executable
instruction or copied production prompts. Keep credentials, generated state,
raw external logs and caches out of Git; stage explicit paths only.
Earlier stage-by-stage documents remain in
[fixed engineering history](maintenance.md#engineering-history).
