# ActLumen · 明行

**English** | [简体中文](README.zh-CN.md)

**AI action review for enterprise workflows**

Make AI actions clear. Make business collaboration more effective.

ActLumen helps enterprise teams review proposed AI actions before execution: **what was requested, what AI plans to do, and whether the supporting evidence matches the current action**. This repository provides evidence checks and reviewable records. An optional intent observer in a separate business sandbox can highlight potential deviations for human review.

**Act** stands for action; **Lumen** evokes light and clarity. The Chinese name, **明行**, expresses the same idea: make AI actions understandable and give teams a clear basis for review.

[Reviewer brief (中文)](docs/actlumen-reviewer-brief.md) · [Leadership presentation (中文)](docs/presentations/agentharness-enterprise-hackathon.html) · [Documentation index (中文)](docs/README.md) · [Engineering guide](docs/engineering-guide.md)

## Why teams need ActLumen

As AI starts helping with orders, customers, and expenses, employees still need to check whether a proposal matches the request, whether its supporting material belongs to the current action, and what needs attention.

- **Less repeated checking:** reduce the need to retrace long conversations and search for supporting material.
- **Earlier visibility of deviations:** highlight plans that go beyond the request, such as preparing an approval when only a status lookup was requested.
- **A clearer record for review:** retain checks tied to the current action so teams can explain what happened and learn from it.

These are intended benefits. Time savings and reduced rework still need to be measured in a real business pilot.

## Where to start

| Workflow | Proposed task | What to watch for | Intended benefit |
| --- | --- | --- | --- |
| Customer service | Look up a refund's progress and draft a reply. | A status lookup must not turn into an approval. | Spend less time searching records and more time helping customers. |
| Sales operations | Summarize order delivery progress and follow-up items. | Checking progress must not turn into changing a delivery date. | Reduce repeated confirmations and explanations. |
| Finance coordination | Match refunds to orders and flag items to reconcile. | Reconciliation must not turn into initiating payment. | Focus attention on items that need business judgment. |

These are proposed applications. They have not been connected to Lenovo's business systems. A consolidated review interface for employees is planned product work.

## How it fits into a workflow

```text
Employee request → AI proposal → ActLumen evidence checks and intent hints → Existing enterprise process
```

Evidence checks establish whether supporting material is bound to the current action. Intent observation highlights possible departures from the request. Both support human judgment. Approval and execution remain the responsibility of existing enterprise processes and external systems.

## What exists today

| Current foundation | Next validation step |
| --- | --- |
| This repository implements pre-execution evidence checks, deterministic validation, and reviewable records. | Build a business review interface and pilot one approved, read-only workflow. |
| A separate local business sandbox implements optional Jev intent observation. | Compare task outcomes, total handling time, added review burden, and maintenance effort. |
| A synthetic evaluation with frozen inputs has been retained. | Use real business comparisons to decide whether to expand. |

In a single evaluation run in that separate sandbox on **2026-10-21**, all 36 overreach cases were flagged, all 24 unclear-intent cases received review hints, and 3 of the 24 fitting cases also received review hints: **84 synthetic cases** in total.

The cases were AI-authored and independently blind-labeled by another AI. They span 33 correlated scenario families and are neither human ground truth nor Lenovo business data. Zero observed misses do not establish production accuracy; the review burden on fitting requests also matters. [Full evaluation record](docs/33-jev-shadow-maintenance-handoff.md)

Time savings, cost savings, and ROI in Lenovo workflows have not been measured. A useful pilot should assess correct outcomes, faster overall handling, and an acceptable added review burden.

## Find the right material

| Reader | Start here |
| --- | --- |
| Leaders and hackathon judges | [Four-page reviewer brief (中文)](docs/actlumen-reviewer-brief.md), [eight-slide offline presentation (中文)](docs/presentations/agentharness-enterprise-hackathon.html) |
| Business pilot owners | [Brand and capability scope (中文)](docs/actlumen-brand-and-scope.md), plus scenarios, expected benefits, and the pilot proposal in the reviewer brief |
| Developers and platform teams | [Engineering guide](docs/engineering-guide.md), [asset map](docs/00-asset-map.md) |
| Security and evidence reviewers | [Product contract](docs/08-glossary-and-product-contract.md), [reproducible engineering demo](docs/11-reproducible-enterprise-demo.md), [review checklist](docs/13-external-reviewer-checklist.md) |
| Maintainers | [Maintenance record (中文)](docs/34-actlumen-brand-maintenance.md), [repository guidance](AGENTS.md) |

GitHub shows the presentation's HTML source. Download the single HTML file to present it offline in a browser, navigate slides, switch scenarios, or print. Source links remain subject to repository access permissions.

## Developer quick start

Run from the repository root with Python 3.10 or later:

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

See the [engineering guide](docs/engineering-guide.md) for installation requirements, the full command reference, CI, evidence contracts, external runtime responsibilities, and historical milestones.

## Continuous Integration

<details>
<summary>Verification details and complete local commands</summary>

[![CI](https://github.com/alexzhu0/ActLumen/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alexzhu0/ActLumen/actions/workflows/ci.yml)

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

</details>

## Brand, compatibility, and scope

ActLumen · 明行 is the new project brand for AgentHarness. The existing `agentharness` command, Python package name, protocols, and file paths remain compatible. Historical release and handoff records retain their original names. The source prerelease remains `v0.2.0-alpha.1`; the branding update is not a new version or package publication.

This repository is a pre-execution evidence control plane. `allow_candidate` denotes candidate evidence only; current evidence and shadow outputs retain `result_status: not_executed`. Identity, authorization, approval semantics, transactions, and actual execution belong to external systems. [Full scope statement (中文)](docs/actlumen-brand-and-scope.md)

Licensed under the [MIT License](LICENSE).
