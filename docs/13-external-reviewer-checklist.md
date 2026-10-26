# ActLumen External Reviewer Checklist

> 项目品牌：ActLumen · 明行。现有命令与包名保留 `agentharness`；[文档导航](README.md)与[能力范围](actlumen-brand-and-scope.md)提供当前入口。

ActLumen remains a pre-execution evidence control-plane.

This checklist is for security, platform, and compliance reviewers evaluating ActLumen evidence before any downstream owner acts. It turns the current evidence chain into an operational rubric for deciding whether an evidence package should be accepted for downstream review, rejected, or escalated externally.

This is evidence acceptance, not runtime approval. ActLumen does not approve runtime action, does not execute tools, and does not make safety guarantees for downstream execution.

Ready does not mean executed. Ready does not mean safe to execute. All current result_status outputs remain not_executed.

## Scope and audience

Use this checklist when reviewing the evidence generated from an ActLumen file-bus fixture, especially the `examples/agent_bus_adapter_registry` demo flow.
For a concrete reviewer dry-run that applies this checklist to the golden fixture, see [`docs/14-reviewer-dry-run-and-reproducibility.md`](./14-reviewer-dry-run-and-reproducibility.md).

The reviewer is checking whether the evidence package is complete, deterministic, internally consistent, traceable, and boundary-safe enough for an external owner to review. The checklist is not a runtime authorization process, not a governance decision engine, not an auth or identity system, not a sandbox policy, and not a signing, timestamp, attestation, certificate, or trust-root flow.

## Reviewer outcome definitions

Use the [decision guide](./12-buyer-reviewer-decision-guide.md#decision-outcomes)
for the meanings of accept evidence for downstream review, reject evidence
package, and escalate externally. Apply those outcomes using the rubric below.

## Reviewer checklist table

| Check ID | Reviewer question | Evidence source / command | Accept condition | Reject condition | Escalate condition |
| --- | --- | --- | --- | --- | --- |
| `R1_artifact_completeness` | Are all expected evidence artifacts present? | Demo flow in [`docs/11-reproducible-enterprise-demo.md`](./11-reproducible-enterprise-demo.md), saved reviewer artifacts, and this checklist. | Required artifacts are present: validation/eval output, loop check, handoff inspection, export package, digest manifest, manifest readback, audit report, audit report readback, audit checklist, and T025 harness result when available. | Any required artifact is missing, unreadable, malformed, or from the wrong fixture/run. | Escalate if an external owner requires additional production records outside ActLumen evidence. |
| `R2_policy_and_bus_validation` | Did policy validation, smoke evals, and file-bus validation pass? | `./agentharness validate`, `./agentharness eval --cases PI-001,PD-001,SEC-001`, `./agentharness loop check examples/agent_bus_adapter_registry`. | Policy validation passes, smoke evals are 3/3, and loop check passes for the reviewed bus. | Any validation fails, reports malformed input, or cannot be reproduced. | Escalate if policy acceptance itself belongs to a governance owner. |
| `R3_handoff_readiness_split` | Are ready, blocked, and unsupported handoffs separated? | `./agentharness handoff inspect examples/agent_bus_adapter_registry`, audit report handoff rows. | Ready/exported, blocked, and unsupported items are distinguishable and match the expected reviewed evidence. | Blocked or unsupported items are unclear, missing, or misclassified as ready. | Escalate if adapter coverage or production intent classification is owned externally. |
| `R4_approval_binding` | Is approval-required evidence present where needed? | Handoff inspection, preflight evidence, approval records, enterprise audit report rows. | Approval-backed readiness is present for approval-required ready items, and missing approval blocks the relevant item. | Approval-required item is ready/exported without required approval evidence, or approval evidence is malformed/stale. | Escalate if approval authority or approval policy belongs to an external governance owner. |
| `R5_adapter_registry_binding` | Is adapter/spec evidence registry-backed and digest-bound? | Registry-backed export package, adapter registry validation, digest manifest, audit report manifest section. | Adapter ref selects an active exact version, registry digest matches the canonical adapter spec, and paths remain within bus scope. | Registry entry is missing, disabled, deprecated for selection, digest-mismatched, path-traversing, or otherwise invalid. | Escalate if the runtime adapter coverage question exceeds current registry evidence. |
| `R6_export_exclusion_safety` | Did export include only ready handoffs? | `./agentharness handoff export examples/agent_bus_adapter_registry`, audit report export section. | Exported request IDs are only handoff-ready items; blocked and unsupported items are excluded. | Any blocked or unsupported request appears in the export package. | Escalate if an external owner asks whether an excluded item should be supported in a future adapter. |
| `R7_manifest_readback` | Does the saved digest manifest match regenerated evidence? | `agentharness handoff verify-manifest <bus_root> <manifest_path>`. | Verification report returns `ok: true`, matching item order and digests, with `result_status: not_executed`. | Saved manifest is stale, missing items, has extra/reordered/tampered items, malformed JSON, wrong digest, or wrong `result_status`. | Escalate if reviewer requires signing, timestamp, attestation, or trust-root material. |
| `R8_audit_report_contract` | Does the enterprise audit report match the accepted contract? | `./agentharness audit report examples/agent_bus_adapter_registry`, [`schemas/enterprise_audit_report.schema.yaml`](../schemas/enterprise_audit_report.schema.yaml). | Report is deterministic, schema-valid, path-sanitized, and preserves expected summary/export/manifest evidence. | Report is malformed, schema-drifted, contains unexpected writer/runtime fields, leaks raw local paths, or claims execution. | Escalate if a production audit system requires additional external fields or controls. |
| `R9_audit_report_readback` | Does the saved audit report match regenerated current evidence? | `agentharness audit verify-report <bus_root> <audit_report_path>`. | Verification report returns `ok: true`, matching canonical report digest and handoff rows. | Saved report is stale, tampered, missing/extra/reordered, schema-invalid, path-leaking, or has mismatched digest. | Escalate if long-term retention, signing, timestamp, or evidence custody is an external compliance concern. |
| `R10_checklist_goal_status` | Does the enterprise audit checklist summarize pass/fail/blocked/manual status correctly? | `./agentharness audit checklist examples/agent_bus_adapter_registry`, [`schemas/enterprise_audit_checklist.schema.yaml`](../schemas/enterprise_audit_checklist.schema.yaml). | Checklist has `ok: true`, goal status is pass, expected check IDs are ordered, passed/manual counts are coherent. | Checklist has failed/blocked checks, schema drift, unordered/missing IDs, malformed status, or unsanitized errors. | Escalate if manual reviewer context cannot be supplied inside ActLumen evidence. |
| `R11_result_status_invariant` | Do all current outputs remain pre-execution evidence? | Handoff inspection, export, manifest, verification, audit report, audit verification, audit checklist, T025 harness. | Every current handoff/export/manifest/verification/audit/checklist output uses `result_status: not_executed`. | Any output contains executed/completed/runtime execution status or implies a side effect occurred. | Escalate if downstream runtime status is required; ActLumen does not own it. |
| `R12_path_sanitization` | Do reviewer-facing outputs avoid raw local host paths? | `handoff inspect`, `handoff inspect --json`, audit report errors/warnings, verification reports. | Reviewer-facing artifacts contain no raw `/home`, `/tmp`, Windows drive, UNC, or host-specific path leaks except reviewer-owned shell paths outside the payload. | Any text/JSON payload leaks raw local paths, temp paths, or host-specific workspace paths. | Escalate if external evidence custody requires a separate redaction or DLP process. |
| `R13_manual_checks_recorded` | Are manual checks explicit and reviewer-owned? | Audit checklist manual rows and saved readback commands. | Manual items clearly list saved manifest and saved audit report readback commands, and the reviewer supplies paths. | Manual checks are hidden, skipped, or described as ActLumen execution/approval. | Escalate if external context is required to interpret manual evidence. |
| `R14_boundary_non_claims` | Does the evidence avoid runtime, safety, and enforcement claims? | Product contract, docs/12, this checklist, audit report boundary fields. | Wording says accept evidence for downstream review, reject evidence package, or escalate externally; it does not claim execution approval or safety. | Output or docs claim ActLumen executes, dispatches, submits, approves runtime action, guarantees safety, or enforces governance/auth/sandbox/signing/trust-root controls. | Escalate all execution, authorization, sandbox, signing, deployment, and operations decisions to external owners. |

## Evidence package completeness

Check row `R1_artifact_completeness` against the artifacts generated by the
[demo command flow](./11-reproducible-enterprise-demo.md#copy-paste-command-flow).
Record each missing, malformed, or mismatched artifact in the review.

## Accepted fixture counts

The [demo summary table](./11-reproducible-enterprise-demo.md#expected-summary-counts)
is the maintained source of expected counts for
`examples/agent_bus_adapter_registry`. These are fixture expectations, not
universal requirements for other evidence packages. The
[recorded dry-run](./14-reviewer-dry-run-and-reproducibility.md#expected-vs-observed)
retains the historical observed results.

## Reject triggers

Use the reject condition in each `R1`–`R14` row. A missing artifact, failed
binding or readback, invalid schema, path leak, wrong execution status, or
unsupported item exported as ready prevents evidence acceptance. See the
[rejection outcome](./12-buyer-reviewer-decision-guide.md#reject-evidence-package).

## External escalation triggers

Use the escalation condition in each rubric row and the
[external escalation outcome](./12-buyer-reviewer-decision-guide.md#escalate-externally).
Identity, runtime authorization, sandboxing, signing, deployment, and operational
decisions belong to their external owners; escalation creates no task lifecycle
state in ActLumen.

## Manual checks

Manual means reviewer-supplied saved artifacts or external context, not ActLumen execution or approval.

Current manual readback commands are:

```bash
agentharness handoff verify-manifest <bus_root> <manifest_path>
agentharness audit verify-report <bus_root> <audit_report_path>
```

A manual check can still be required even when all generated evidence is deterministic. The reviewer supplies the saved manifest or audit report path and compares it with regenerated current evidence.

## Copy-paste reviewer mini-loop

Run the [single maintained demo command flow](./11-reproducible-enterprise-demo.md#copy-paste-command-flow)
from the repository root. Its `/tmp/agentharness-demo-*.json` files are created
by reviewer shell redirection for readback, not by a product output-writer flag.
Apply the rubric above to those artifacts.

## Anti-claims / wording guardrail

Follow the [decision wording](./12-buyer-reviewer-decision-guide.md#anti-claims--wording-guardrail)
and [product contract](./08-glossary-and-product-contract.md#product-contract).
Evidence acceptance is not execution approval; every current result remains
`result_status: not_executed`.
