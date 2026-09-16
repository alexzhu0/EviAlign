# Business Sandbox Implementation Plan

> Execute using Superpowers TDD and independent reviews. Independent world and evidence tasks use dispatching-parallel-agents; runtime integration stays sequential.

**Goal:** Deliver the approved synthetic business sandbox and honest A/B acceptance report.
**Architecture:** Separate standard-library SQLite runtime; AgentHarness only validates bounded business-action evidence. Model proposes finite tools; runtime owns identity, authorization, transactions and effects.
**Tech Stack:** Python3.10+, SQLite, standard-library HTTP, vanilla HTML/JS, existing DeepSeek official API.
**Spec:** ../specs/2026-09-15-business-sandbox-design.md

## Global constraints
Synthetic-only, no arbitrary SQL/networktools. 3tenants/300customers/24identities/3000orders, fixed seed and sixmonthhistory. 4modelcalls/turn,12turns/session. Writes opt-in after runtime/evidence review. A/B fullauth botharms. Oldrepos preserved. Work staged /tmp/agentharness-business-sandbox; install explicit sibling files after tests. No commit/push required.
Interfaces frozen in staging docs/interfaces.md; consumers use exact signatures/schema.

## Tasks
- [x] World: tests/test_world.py red counts, foreign keys and literal golden 10000/20000/5000 accounting; implement sandbox/world.py; verify SQL sums, seeded repeatability, manifest.
- [x] Evidence: tests/test_business_action_evidence_v1.py red mutation/replay/expiry/schema; implement src/agentharness/business_action_evidence_v1.py pure verifier and bounded CLI; preserve not_executed and independent review before enablewrites.
- [x] Runtime: tests/test_runtime.py red scope/date/sort/emptycustomer and writes/approval/idempotency/conflict/rollback; implement sandbox/runtime.py with finite tools, trusted ticket snapshots, fresh auth and actual counters. Run unittest after each group.
- [x] Interface: tests/test_web.py red origin/session/boundedbody; sandbox/web.py, static/index.html and bounded agent.py; realbrowser role/query/approval/reset verification.
- [x] Evaluation: sandbox/scenarios.py and tests/test_scenarios.py, 60 independent scenarios with 15 frozen acceptance cases, deterministic A/B and model error isolation. Add CLI, README, reports and run commands.
- [x] Review/evidence: independent reviews of core and interface, fixes verified, required AgentHarness checks and sandbox fullsuite; live DeepSeek acceptance then independent frozen set without prompt tuning.
- [x] Install/run: explicit sibling installation, localhost8768, browser verification and final report including failures and limitations. Mark all completed only when delivered.

## Test examples and expectations
```python
assert manifest(build_world())['counts']['orders']==3000
r=s.act(s.session('acme_customer1'),{'tool':'order_detail','args':{'order_id':'o_acme_0002'}})
assert not r['ok'] and r['rows']==[] and r['runtime']['writes']==0
```
Refund scenario creates request from acme_support1 for o_acme_0001 amount1000, approves as acme_manager; requests approved, refunds ledger unchanged. Replay same ticket returns cached result without business write. Inject after_write causes rollback and records attempted write, not false not_executed. Tamper evidence: B blocks; A reports absent evidence, maintains freshauth.

## Completion evidence
2026-09-15: installed independent sibling sandbox, serving localhost8768. 52 sandbox tests,538 AgentHarness tests,150 targeted tests and required CLI checks pass. Offline60/60 botharms; live development6/6, frozen evidence13/15 and baseline15/15. Two model failures preserved without prompt tuning. Browser desktop/mobile workflow and realmodel two-tool task passed. Final report: ../agentharness-business-sandbox/docs/acceptance-report.md (sibling runtime path from repository parent). No commits, pushes or production integrations.
