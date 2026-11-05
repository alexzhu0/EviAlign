# EviAlign asset map / 资产地图

Current purpose and stage: [English](project-purpose-and-progress.md) ·
[中文版](project-purpose-and-progress.zh-CN.md). EviAlign supplies pre-execution
request/evidence checks; identity, approval validity and execution remain with
external systems.

## Current assets

| Asset | Source of truth | Guide |
| --- | --- | --- |
| Agent design patterns | [`patterns/agent_design_patterns.yaml`](../patterns/agent_design_patterns.yaml) | [Pattern library](01-agent-design-pattern-library.md) |
| Tool-policy definitions | [`policies/tool_governance.yaml`](../policies/tool_governance.yaml) | [Policy design](02-tool-governance-policy.md) |
| Local safety evaluations | [`evals/agent_safety_eval_suite.yaml`](../evals/agent_safety_eval_suite.yaml) | [Evaluation contract](03-agent-safety-eval-suite.md) |
| Structured policy | [`schemas/agent_policy.schema.yaml`](../schemas/agent_policy.schema.yaml), [example](../examples/agent_policy.example.yaml) | [Compiler design reference](04-prompt-policy-compiler.md) |
| File-bus evidence | [`schemas/loop_task.schema.yaml`](../schemas/loop_task.schema.yaml), [registry fixture](../examples/agent_bus_adapter_registry/) | [Protocol](05-loop-file-bus.md), [architecture](06-runtime-architecture.md) |
| Audit evidence | [Report schema](../schemas/enterprise_audit_report.schema.yaml), [checklist schema](../schemas/enterprise_audit_checklist.schema.yaml) | [Audit contract](10-enterprise-audit-report-and-buyer-demo.md) |
| Pi observation/evidence | [Request schema](../schemas/pi_tool_call_observation_batch.v1.schema.json), [response schema](../schemas/pi_tool_call_evidence_response_batch.v1.schema.json) | [Versioned contract](24-pi-observation-evidence-contract-v1.md) |
| Data-access evidence | [`src/agentharness/data_access_evidence_v1.py`](../src/agentharness/data_access_evidence_v1.py) | [Separate synthetic lab](31-synthetic-data-access-lab.md) |
| Business-action evidence | [`src/agentharness/business_action_evidence_v1.py`](../src/agentharness/business_action_evidence_v1.py) | [Contract](business-action-evidence-v1.md), [sandbox boundary](32-business-sandbox-maintenance-handoff.md) |

Patterns and compiler documents include design/reference material; their
presence does not imply a complete compiler, runtime or enterprise approval
product. Implemented command forms and supported behavior are described in the
[engineering guide](engineering-guide.md) and verified by [tests](../tests/).

## Demonstrate and review

- [Research-review workbench](research-review-workbench.md): separate local
  sandbox, offline replay or explicitly enabled live DeepSeek/Jev observation,
  initial/final annotations and export. No business execution is authorized.
- [Reproducible repository demo](11-reproducible-enterprise-demo.md): local
  fixtures, reports and saved-artifact readback.
- [Reviewer decisions](12-buyer-reviewer-decision-guide.md) and
  [reviewer checklist](13-external-reviewer-checklist.md): evidence acceptance
  criteria, not runtime approval.
- [Retained Jev evaluation](33-jev-shadow-maintenance-handoff.md): historical
  synthetic results, model/rubric pins, limitations and separate ownership.

## Contracts and maintenance

- [Terminology and product contract](08-glossary-and-product-contract.md)
- [Enterprise boundary](07-enterprise-positioning-and-boundary-audit.md) and
  [source-backed integration strategy](09-source-backed-integration-strategy.md)
- [Pi mapping](18-pi-tool-call-mapping-fixture.md),
  [static CLI](19-pi-contract-check-cli.md) and
  [external wiring guide](20-pi-dual-repo-dry-run-e2e.md)
- [Runtime readiness ADR](25-pi-runtime-authorization-readiness-adr.md) and
  [Phase-0 preflight](27-pi-runtime-authorization-phase0-preflight.md): proposed
  external requirements, **NO-GO / NOT IMPLEMENTED**
- [Engineering designs](superpowers/README.md), [maintenance](maintenance.md)
  and [release history](../release/README.md)
- [Repository guidance](../AGENTS.md): Superpowers is the development workflow

The earlier T0xx development chronology and superseded phase/packaging notes
are available through [fixed historical versions](maintenance.md#engineering-history).
`allow_candidate` remains candidate evidence; applicable outputs preserve
`result_status: not_executed`.
