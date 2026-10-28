# EviAlign Enterprise Audit Report and Buyer Demo

> 项目品牌：EviAlign。现有命令与包名保留 `agentharness`；[文档导航](README.md)与[能力范围](actlumen-brand-and-scope.md)提供当前入口。

Guidance consolidated: 2026-09-14. Historical T017–T025 references are retained below.

EviAlign is a pre-execution evidence control-plane for agent actions.

This document uses [`docs/08-glossary-and-product-contract.md`](./08-glossary-and-product-contract.md) as the normative glossary and product contract. It also follows the source-backed external-consumer boundaries in [`docs/09-source-backed-integration-strategy.md`](./09-source-backed-integration-strategy.md).

Current scope invariant: EviAlign validates and exports evidence only. Runtime, governance, auth, identity, sandbox, signing, trust-root, and execution-plane systems are external consumers, not EviAlign in-repo responsibilities. All handoff, export, manifest, and verification outputs remain `result_status: not_executed`.

## Audience

This narrative is for enterprise reviewers who need to understand an agent action before any downstream runtime owns execution:

- **Security reviewers** decide whether the proposed action has enough policy, approval, and digest evidence to be considered by a downstream owner.
- **Platform reviewers** decide whether the file-bus, handoff, export, and manifest surfaces are deterministic enough for platform intake.
- **Compliance reviewers** decide whether the evidence is replayable, reviewable, and bounded before operational systems act.
- **Runtime/governance/auth owners** decide, outside EviAlign, whether their own runtime, governance, identity, authorization, sandbox, and operational controls will consume the evidence.

## One-page buyer-demo narrative

An agent wants to perform a tool action. In a normal runtime-first story, the buyer has to ask after the fact: what was requested, which policy applied, who approved it, whether the target runtime supported it, and whether the record can be replayed.

EviAlign moves that discussion before execution. It reads a file-bus ledger, validates tool-gate reports, checks approval records, recomputes preflight eligibility, reads handoff reports, validates adapter registry bindings, exports only ready evidence, builds a digest manifest, and verifies manifest readback. The reviewer can see which requests are ready, blocked, or unsupported without any tool being executed.

For the current registry-backed fixture, the reviewer sees five proposed handoffs. Two are ready and exported, two are blocked, and one is unsupported. The exported items are the read-only request `TR-read` and the approval-backed delete request `TR-approve-delete`. The blocked and unsupported requests do not enter the export package.

The downstream runtime, governance, or auth owner remains external. EviAlign does not replace LangGraph, OpenAI Agents SDK, CrewAI, Microsoft Agent Framework, Microsoft Agent Governance Toolkit, Open Agent Auth, MCP Authorization, or a future execution-plane system. It supplies deterministic pre-execution evidence that those owners may review under their own controls.

No execution has occurred. The current package, manifest, and verification report all keep `result_status: not_executed`.

## Reviewer workflow

Use the [reproducible command flow](./11-reproducible-enterprise-demo.md#copy-paste-command-flow)
to generate and verify the evidence, then apply the
[decision guide](./12-buyer-reviewer-decision-guide.md#decision-outcomes) and
[reviewer rubric](./13-external-reviewer-checklist.md#reviewer-checklist-table).
EviAlign reports evidence; the external runtime owns execution and authorization.

## Evidence-chain walkthrough

| Evidence step | What the reviewer learns | Current boundary |
| --- | --- | --- |
| file-bus | The ledger-backed request and report references exist in a deterministic bus layout. | Validation source of truth, not a scheduler or live queue. |
| tool gate | The requested tool action is classified as allowed, approval-required, or denied by policy. | Side-effect-free report, not permission to execute. |
| approval record | Approval-required requests are bound to a same-attempt approval decision and digest context. | Evidence binding, not broad standing authorization. |
| preflight | Tool-gate and approval facts are recomputed into ready or blocked eligibility. | Pre-execution readiness, not runtime execution. |
| handoff | Preflight output is bound to adapter support checks and `result_status: not_executed`. | Read-only boundary report, not adapter invocation. |
| adapter registry | Adapter refs are selected by exact id/version and checked against registry/spec digests. | Versioned evidence binding, not package discovery or runtime loading. |
| export package | Only registry-backed, handoff-ready items are emitted to deterministic stdout JSON. | Ready-only evidence, not task submission. |
| digest manifest | The export package and each item are named by canonical SHA-256 digest. | Digest readback material, not signing, timestamping, attestation, or trust-root proof. |
| manifest verification | A saved manifest is regenerated from current bus state and compared deterministically. | Readback check, not external trust verification or execution. |

## Embedded audit report examples

The [demo summaries](./11-reproducible-enterprise-demo.md#expected-summary-counts)
and [five request cases](./11-reproducible-enterprise-demo.md#ready-blocked-and-unsupported-case-interpretation)
are maintained in the reproducible demo. Exact tool, intent, scope, preflight,
and gate fields are in the committed
[handoff fixture](../examples/agent_bus_adapter_registry/handoffs/T008-handoff-report.yaml).
These examples describe evidence; they are not a separate report schema.

The original registry-backed example recorded this canonical package digest:

```text
sha256:63806cd94fb4a5b012a2b79e7bbef1c5068009a972a73ae26dc72ef04a010965
```

Its ready item order is `TR-read`, then `TR-approve-delete`. A matching saved
manifest verifies with `ok: true`, an empty errors list, and
`result_status: not_executed`. Regenerate evidence for a current review rather
than treating this recorded digest as fresh verification.

## T018/T020 machine-readable enterprise audit report

T018 adds a read-only command for this narrative:

```bash
./agentharness audit report examples/agent_bus_adapter_registry
```

The command emits deterministic JSON to stdout with `kind: enterprise_audit_report`. It composes existing handoff inspection, registry-backed export package, and digest manifest evidence. It does not call `handoff verify-manifest`, because saved-manifest readback requires a separate manifest path. Instead, the report includes `manifest_verification` as a boundary note with `performed: false`, `reason: requires_saved_manifest_path`, and `result_status: not_executed`.

Failure output uses `kind: enterprise_audit_report_error`, exits 1, and keeps sanitized errors/warnings free of absolute host paths. The command has no `--out`, `--write`, `--save`, `--execute`, `--dispatch`, `--submit`, `--run`, `--mutate`, `--sign`, or `--timestamp` flags.

T020 adds the repo-native enterprise audit report schema at
[`schemas/enterprise_audit_report.schema.yaml`](../schemas/enterprise_audit_report.schema.yaml)
and a pure in-memory payload validator. The schema is a contract/check for the
pre-execution evidence report; it is not runtime integration, not execution,
not signing, not timestamping, not attestation, not a trust-root system, and not
file-output behavior. Successful audit payloads continue to omit top-level
`ok`, and both success/error payloads continue to require
`result_status: not_executed`.

T021 adds saved-report readback verification:

```bash
./agentharness audit report examples/agent_bus_adapter_registry > /tmp/agentharness-audit-report.json
./agentharness audit verify-report examples/agent_bus_adapter_registry /tmp/agentharness-audit-report.json
```

The verifier reads the saved `enterprise_audit_report` JSON, validates it with
the T020 payload validator, regenerates the current report from the file bus,
and compares canonical JSON/digests. It emits
`enterprise_audit_report_verification_report` JSON to stdout on pass and fail.
This is readback verification only: it is not runtime execution, not runtime
adapter invocation, not file-output behavior, not signing/timestamping,
attestation, certificate, notarization, or trust-root proof, not auth/identity/
sandbox/governance enforcement, and not dispatch, submit, run, execute, or task
mutation.

T022 adds a read-only reviewer checklist:

```bash
./agentharness audit checklist examples/agent_bus_adapter_registry
```

The checklist emits `enterprise_audit_checklist_report` JSON to stdout only.
It orders the reviewer goals as file-bus validation, handoff inspection,
registry-backed export, digest manifest, enterprise audit report self-check,
and two manual saved-artifact readback checks. Manual means the readback needs a
reviewer-provided saved manifest or audit report path; EviAlign does not
create that file through a product output flag. Checklist statuses are limited
to `pass`, `fail`, `blocked`, and `manual`, and every check keeps
`result_status: not_executed`. T024 adds the repo-native checklist schema at
[`schemas/enterprise_audit_checklist.schema.yaml`](../schemas/enterprise_audit_checklist.schema.yaml)
and a pure in-memory validator; this is payload drift protection, not runtime
authorization, signing, trust-root, governance enforcement, or file output.

For a copy-paste reviewer demo using the existing commands and fixture, see [`docs/11-reproducible-enterprise-demo.md`](./11-reproducible-enterprise-demo.md).
For reviewer decision outcomes, see [`docs/12-buyer-reviewer-decision-guide.md`](./12-buyer-reviewer-decision-guide.md).
For an operational third-party acceptance rubric, see [`docs/13-external-reviewer-checklist.md`](./13-external-reviewer-checklist.md).

## Buyer-demo talk track

Explain the need for evidence before high-impact agent actions, run the
[demo](./11-reproducible-enterprise-demo.md), and show why some requests are
exported while others are blocked or unsupported. Demonstrate saved-artifact
readback, then identify the external owner responsible for any execution decision.

## Objections and answers

| Objection | Answer |
| --- | --- |
| Is this a runtime? | No. EviAlign validates and exports pre-execution evidence only. |
| Does it replace LangGraph/OpenAI Agents SDK/CrewAI/MAF? | No. Those are external runtime/orchestration consumers; EviAlign can supply evidence before their owners act. |
| Does it enforce auth/governance/sandboxing? | No. It supplies evidence to external governance, auth, identity, sandbox, and runtime owners. |
| Can it execute tools? | No. Current handoff/export/manifest/verification output remains `result_status: not_executed`. |
| Why is it valuable? | It gives deterministic pre-execution evidence, ready-only exclusion, approval binding, and replayable manifests that reviewers can inspect before downstream systems decide anything. |

## Red-line boundaries

T017 provided the narrative; T018/T020 added report generation and payload
validation; T021 added report readback; T022/T024 added checklist generation and
validation; T025 added evidence-chain regression coverage. These milestones
remain evidence-only, with `result_status: not_executed`.

The [product contract](./08-glossary-and-product-contract.md#product-contract)
is the normative boundary for runtime ownership, authorization, adapters,
file output, scheduling, signing, and trust roots.

## Future follow-ups

Add further interchange contracts only when an external consumer has a concrete
need. Any runtime work follows the separate approval and ownership boundaries in
the [product contract](./08-glossary-and-product-contract.md#product-contract).
Use the [end-to-end regression harness](../tests/test_end_to_end_evidence_chain.py)
when reviewing later evidence-contract changes.
