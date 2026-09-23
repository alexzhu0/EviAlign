# Business Sandbox Maintenance Handoff

Updated: 2026-09-16

## Current decision

Keep AgentHarness and the separate `agentharness-business-sandbox` runtime as
an internal technical foundation. The synthetic stage is complete enough to
stop expanding tables, roles and scenarios. The next useful experiment is a
bounded, read-only shadow pilot against one real internal data source.

This is a local development handoff. It is not a Git tag, hosted release,
package publication, deployment, production certification or runtime
authorization decision.

## Delivered boundary

AgentHarness now has two separate local evidence contracts for the test labs:

- `data-access-evidence-v1` correlates the earlier read-only customer/order lab.
- `business-action-evidence-v1` correlates the richer business sandbox request,
  identity context, proposal, authorization decision, resource state and
  approval references.

Both contracts parse bounded inputs, fail closed and emit a bounded report with
`result_status: not_executed`. Their digest equality is correlation evidence;
it is not identity authentication, a signature, permission or execution.

The external business sandbox owns synthetic identity, current authorization,
tool argument validation, transactions, idempotency and effects. It contains a
fixed-seed in-memory world with 3 tenants, 24 actors, 300 customers and 3,000
orders, plus payments, refunds, shipments, tickets, documents and audit events.
Its four simulated write tools never contact payment, logistics, email or other
real systems. Approval changes a synthetic request state and does not move
money.

## Acceptance evidence

The sandbox acceptance report dated 2026-09-15 records:

- 59/59 sandbox unit, integration and HTTP tests passed.
- 60/60 deterministic offline scenarios passed in both evidence and baseline
  arms, with zero unauthorized successes in either arm.
- E01-E03 demonstrated receipt mismatch detection while both arms retained the
  same runtime authorization checks.
- AgentHarness recorded 538/538 full tests and 150/150 evidence-contract target
  tests at that checkpoint.
- DeepSeek `deepseek-v4-pro` completed the final 6/6 development regression and
  15/15 previously seen v1 safety regression. The original v2 frozen reports
  remain 14/15 in both arms because the frozen evaluator rejected a valid
  two-step lookup; the later business-trace review records 15/15 without
  rewriting the frozen score.

These are dated acceptance records. They do not establish production accuracy,
latency, availability, investigation-time savings or business value. A new
maintenance run should use the repository commands below; paid model calls are
not required merely to refresh documentation.

## Fresh maintenance verification

On 2026-09-16, the current local trees passed the repository policy validation,
3/3 smoke evaluations, both required loop checks, the 150-test targeted evidence
suite and all 538 AgentHarness tests. Before follow-up review, 59/59 sandbox
tests passed when the HTTP cases could bind a temporary loopback port. Its
offline run was 60/60, and its baseline and evidence comparison arms were each
60/60 with zero unauthorized successes and zero model calls. `git diff --check`
also passed.

An independent read-only review found no Critical, Important or Minor issue in
the three pending change groups. That review also passed 52 focused tests and
checked 118 local links and anchors in the changed documentation. This evidence
supports local source checkpoints; it does not change the runtime or release
boundary above.

A separate review of the external sandbox then found two Important defects and
one Minor logging defect: ticket-scoped support transfers were rolled back after
the assignee changed, simulated login labels could collide during replay, and
the default HTTP error hook could print local tracebacks. Each fix was developed
from a failing regression test. The external runtime subsequently passed 63/63
tests and repeated both 60/60 deterministic arms with zero unauthorized
successes and zero model calls.

## Operator runbook

From AgentHarness, run the repository-required checks without Python bytecode:

```bash
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
git diff --check
```

For evidence-contract changes, also run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q \
  tests.test_handoff_exporter \
  tests.test_handoff_manifest \
  tests.test_loop_bus \
  tests.test_pi_tool_call_mapping \
  tests.test_pi_evidence_contract_v1 \
  tests.test_pi_evidence_contract_cli_v1
```

From the separate sandbox directory, deterministic verification is:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
./run-sandbox test > reports/offline.json
./run-sandbox compare > reports/comparison.json
```

The two scenario commands do not call a model. Model suites consume API quota
and require a new versioned freeze before a new blind acceptance run. Do not
overwrite v1 or v2 historical reports.

## Next experiment

Select one low-risk source such as an internal ticket system or knowledge base.
Use 2-3 real roles and 20-30 representative tasks. Start with read-only shadow
mode: the existing system remains authoritative, the runtime performs its normal
authorization, and AgentHarness records evidence for comparison before any
business result is returned or action is considered.

Record at least task correctness, overreach or unauthorized attempts, evidence
mismatch rate, human review time, false block rate and integration effort. Use
pseudonymized or minimized fields and retain only reviewed bounded evidence.
Do not add production writes, autonomous decisions or a new execution path in
this phase.

Any future effectful path requires a new external-runtime design, adversarial
tests and approval gate. It cannot be inferred from sandbox scores or a
successful `business_action.ok` report.

## Repository handoff

Keep AgentHarness and the sandbox as separate review, commit and release units.
Stage explicit paths only. Before each commit, inspect the exact staged file
list and run `git diff --cached --check`. Generated caches, credentials, raw
provider logs and temporary evidence files do not belong in either repository.

The sandbox was initialized as its own local Git repository on 2026-09-16. Its
clean `main` checkpoint is `a22e39dbc4ed27a5459459cbb7372c2c48f74ea4`.
No remote, tag, hosted release or deployment is recorded by this handoff.

The relevant source records are:

- [Business sandbox design](superpowers/specs/2026-09-15-business-sandbox-design.md)
- [Business sandbox implementation plan](superpowers/plans/2026-09-15-business-sandbox.md)
- [Comprehensive sandbox test plan](superpowers/plans/2026-09-15-comprehensive-sandbox-testing.md)
- [Business action evidence contract](business-action-evidence-v1.md)
