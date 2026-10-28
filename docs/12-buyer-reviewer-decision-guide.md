# EviAlign Buyer/Reviewer Decision Guide

> 项目品牌：EviAlign。现有命令与包名保留 `agentharness`；[文档导航](README.md)与[能力范围](actlumen-brand-and-scope.md)提供当前入口。

EviAlign is a pre-execution evidence control-plane for agent actions.

## Audience and decision frame

This guide is for:

- security reviewers deciding whether evidence is complete enough for downstream review;
- platform reviewers checking whether the file-bus, handoff, export, manifest, audit report, and checklist are coherent;
- compliance reviewers checking reproducible evidence before a downstream owner acts;
- runtime, governance, auth, sandbox, or signing owners acting as external consumers of EviAlign evidence.

The decision in this guide is evidence acceptance for downstream review, not execution approval. A reviewer may accept an evidence package for an external owner to review, reject the evidence package, or escalate externally. EviAlign does not approve runtime action.

## One-sentence product value

EviAlign produces deterministic pre-execution evidence so reviewers can accept for downstream review, reject, or escalate proposed agent actions before a runtime acts.

## Reviewer questions to evidence map

| Reviewer question | Evidence artifact or command | What it proves | What it does not prove |
| --- | --- | --- | --- |
| What was requested? | `./agentharness handoff inspect examples/agent_bus_adapter_registry`, audit report handoff rows | Request IDs, tool names, categories, intents, and target scopes are present in reviewable evidence. | It does not prove the action ran or should run. |
| Which policy/gate applied? | Tool gate, preflight, handoff inspection, audit report | The request was classified as ready, blocked, or unsupported under current evidence. | It does not grant runtime permission. |
| Was approval required and present? | Approval record references, preflight decision, handoff status, audit report rows | Approval-backed readiness can be distinguished from missing-approval blocking. | It does not create broad standing approval or external authorization. |
| Was preflight eligibility recomputed? | `src/agentharness/execution_preflight.py` evidence surfaced through handoff and audit report | Eligibility evidence is recomputed before export/reporting. | It does not execute the proposed action. |
| Is adapter/spec support bound and digest-checked? | Registry-backed handoff export, digest manifest, adapter registry validation | Adapter reference and spec digest evidence are pinned for review. | It does not load or invoke a runtime adapter. |
| Which items are ready, blocked, or unsupported? | Handoff inspection summary, export package summary, audit report summary | Ready/exported `2`, blocked `2`, unsupported `1` are separated. | It does not make blocked or unsupported items ready. |
| Can export, manifest, and report be regenerated and compared? | `handoff verify-manifest`, `audit verify-report`, T025 harness | Saved evidence can be compared with regenerated current evidence. | It does not provide signing, timestamping, attestation, or trust-root proof. |
| What remains manual? | `./agentharness audit checklist examples/agent_bus_adapter_registry` | Saved manifest readback and saved audit report readback require reviewer-provided paths. | Manual does not mean EviAlign approves or performs runtime action. |
| Who owns actual execution? | Product contract in `docs/08-glossary-and-product-contract.md` | External runtime/governance/auth/sandbox/signing owners keep operational responsibility. | EviAlign does not become that owner. |

## Decision outcomes

### Accept evidence for downstream review

Use this outcome when the evidence package is complete, deterministic, and consistent enough to hand to an external runtime or governance owner for their own review. The reviewer can point to validated policy, bus integrity, handoff inspection, registry-backed export, digest manifest, readback verification, audit report, audit report readback, checklist status, and the T025 harness.

Accepting evidence for downstream review does not approve or perform the action. It only says the EviAlign evidence package is coherent enough for external-owner review.

### Reject evidence package

Use this outcome when the evidence package is not acceptable for downstream review. Reasons include missing or invalid evidence, failed readback, stale manifest/report content, unsupported or blocked items appearing in export, schema/contract violation, path leak, or non-deterministic output.

Rejecting the evidence package is not a runtime failure; it is a control-plane evidence decision.

### Escalate externally

Use this outcome when the question is outside EviAlign ownership. Escalate questions about identity, authorization, sandbox policy, signing, timestamping, attestation, trust-root material, deployment policy, production operations, or actual runtime execution to the responsible external owner.

Escalation is external-owner routing. It is not an EviAlign lifecycle state.

## Case walkthrough

Apply these decisions to the [five demo requests](./11-reproducible-enterprise-demo.md#ready-blocked-and-unsupported-case-interpretation).
The ready items may enter the evidence package; blocked and unsupported items
are excluded. An unsupported intent may require an external adapter owner to
review coverage. Accepting evidence never grants execution permission.

## Manual checks and limits

The enterprise audit checklist includes two manual checks:

- saved manifest readback;
- saved audit report readback.

Manual means the reviewer must provide or inspect saved paths and any needed external context. It does not mean EviAlign executes, approves, schedules, dispatches, submits, or mutates anything.

EviAlign can validate, inspect, export, digest, and verify evidence. It cannot answer external-owner questions about production identity, authorization, sandbox controls, signing material, timestamping, attestation, trust roots, deployment policy, or operational approval.

## Boundary red lines

All current handoff, export, manifest, verification, audit, checklist, and demo
outputs remain `result_status: not_executed`. The T028 decision guide introduced
no execution or enforcement capability. See the normative
[product contract](./08-glossary-and-product-contract.md#product-contract).

## Traceability links

- Product contract and vocabulary: [`docs/08-glossary-and-product-contract.md`](./08-glossary-and-product-contract.md)
- Audit report and buyer-demo narrative: [`docs/10-enterprise-audit-report-and-buyer-demo.md`](./10-enterprise-audit-report-and-buyer-demo.md)
- Reproducible command demo: [`docs/11-reproducible-enterprise-demo.md`](./11-reproducible-enterprise-demo.md)
- External reviewer checklist: [`docs/13-external-reviewer-checklist.md`](./13-external-reviewer-checklist.md)
- End-to-end regression harness: [`tests/test_end_to_end_evidence_chain.py`](../tests/test_end_to_end_evidence_chain.py)
- Golden fixture: [`examples/agent_bus_adapter_registry/`](../examples/agent_bus_adapter_registry/)
- Existing commands: `handoff inspect`, `handoff export`, `handoff manifest`, `handoff verify-manifest`, `audit report`, `audit verify-report`, and `audit checklist`

## Anti-claims / wording guardrail

Use the three [decision outcomes](#decision-outcomes): accept evidence for
downstream review, reject evidence package, or escalate externally. “Ready”
means evidence eligibility, never execution, runtime approval, or a safety
guarantee. External owners retain enforcement and operational responsibility.
