# EviAlign

**English** | [简体中文](README.zh-CN.md)

**Reviewable AI actions. Evidence for human oversight.**

EviAlign is a forward-looking research project on how enterprises can review AI-proposed business actions and use accumulated decisions and outcomes to study where human involvement is needed. Its current foundation is a pre-execution evidence-checking prototype; the complete business review-and-learning cycle is still future work.

**EviAlign** combines *evidence* and *align*: keeping an action request and its supporting evidence connected. Identity, authorization, approvals, and execution remain the responsibility of existing enterprise systems.

[Purpose and progress](docs/project-purpose-and-progress.md) · [Reviewer brief (中文)](docs/actlumen-reviewer-brief.md) · [Current PowerPoint delivery record](docs/presentations/evialign-ppt-expanded-delivery.md) · [Documentation index (中文)](docs/README.md) · [Engineering guide](docs/engineering-guide.md)

## Why this repository exists

Many enterprise agents still support questions, queries and analysis. EviAlign anticipates a possible next stage: agents helping redesign workflows, propose decisions and advance business processes. We want to investigate the basis for reviewing those actions before that stage becomes widespread.

The ambition is business sign-off before consequential AI actions: understand what an agent proposes, its supporting basis, and what needs a person's confirmation. In a future integration, records of proposals, human confirmations or modifications, and eventual outcomes could help identify which specific situations require human judgment and which might justify less intervention.

That cycle is a research goal. A high approval rate alone does not establish safety; outcomes, exceptions and changing conditions need validation. Any reduction in human intervention remains a scoped enterprise decision. [Full purpose and research path](docs/project-purpose-and-progress.md)

## Where we are today

**Partial foundation prototype and separate synthetic observation experiments.** With a trusted request and retained evidence, this repository checks whether the evidence still corresponds to the current structured request and emits a bounded, deterministic result. It does not yet collect a complete business history of human judgments and outcomes or adjust oversight rules.

| Responsibility | Current status |
| --- | --- |
| Identity, authorization, approval validity, and execution | Existing external systems remain responsible. |
| Structured request and evidence correspondence | Implemented in this repository, subject to trusted inputs and retained evidence. |
| User intent versus AI proposal | Optional observation in a separate local business sandbox; its hints do not authorize execution. |
| Real approval records versus proposed business fields | Requires a separate design, trusted integration, and validation. |
| Human judgments, business outcomes, and changes to human involvement | Research goal; no complete collection-and-validation cycle or automatic adjustment is implemented. |

The current business evidence contract binds approval fields as supplied but does not interpret them. A receipt for one request will not match a changed request; matching digests alone do not authenticate the source, validate an approval, establish business correctness, or authorize execution. [Business evidence contract](docs/business-action-evidence-v1.md)

## A business question to investigate

In a fictional delivery exception, sales, logistics and service teams need to coordinate. An AI could gather information, prepare follow-up suggestions and propose transferring a ticket; the responsible person may require confirmation before ownership changes. We want to study how to connect that proposed action, the relevant confirmation and its conditions, and the eventual outcome.

This is a future workflow illustration. Historical synthetic case E173 covers only a pending-confirmation ticket transfer, not a delivery exception or a connected approval workflow. [PoC provenance](docs/presentations/evialign-ppt-poc-delivery.md)

## What evidence exists

A single run on **2026-10-21** in the separate sandbox used 84 synthetic intent-observation cases: all 36 overreach cases were flagged; all 24 unclear cases received review hints; and 3 of the 24 fitting cases also received hints.

The cases were AI-authored and independently blind-labeled by another AI, across 33 correlated scenario families. They are not human ground truth or Lenovo business data. These results do not establish production accuracy, real approval-to-action comparison, time savings, or ROI. [Full evaluation record](docs/33-jev-shadow-maintenance-handoff.md)

## How to assess the value

Existing APIs, fine-grained authorization, approvals and audit systems may already cover the necessary controls. An additional component must demonstrate a real gap or a measurable reduction in repeated integration and review effort.

Compare three approaches on one approved, read-only replay of a business workflow: the existing controls; practical improvements to those controls; and a proposed EviAlign integration. Measure discrepancies found, total handling time, extra review burden, integration and maintenance costs, and actual reuse across agents. If existing controls already suffice or costs exceed demonstrated benefits, retain the existing approach.

If the comparison justifies further work, separately design trusted business-record access and an observation study that accumulates human judgments and outcomes while existing controls remain in force. Researching changes to human involvement comes after validation and enterprise approval; the current prototype grants no execution authority.

## Find the right material

| Reader | Start here |
| --- | --- |
| Leaders and hackathon judges | [Purpose and progress](docs/project-purpose-and-progress.md), [reviewer brief (中文)](docs/actlumen-reviewer-brief.md), [current PowerPoint delivery record](docs/presentations/evialign-ppt-expanded-delivery.md) |
| Business pilot owners | [Brand and capability scope (中文)](docs/actlumen-brand-and-scope.md), including the proposed comparison and pilot |
| Developers and platform teams | [Engineering guide](docs/engineering-guide.md), [asset map](docs/00-asset-map.md) |
| Security and evidence reviewers | [Product contract](docs/08-glossary-and-product-contract.md), [reproducible demo](docs/11-reproducible-enterprise-demo.md), [review checklist](docs/13-external-reviewer-checklist.md) |
| Maintainers | [Maintenance record (中文)](docs/34-actlumen-brand-maintenance.md), [repository guidance](AGENTS.md) |

The current PowerPoint and movie were delivered locally; their binaries are not stored in Git. The [earlier HTML presentation](docs/presentations/agentharness-enterprise-hackathon.html) remains a historical illustration. Source links remain subject to repository access permissions.

## Developer quick start

Run from the repository root with Python 3.10 or later:

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

See the [engineering guide](docs/engineering-guide.md) for the complete command reference, contracts, runtime responsibilities, and historical milestones.

## Continuous Integration

<details>
<summary>Verification details and complete local commands</summary>

[![CI](https://github.com/alexzhu0/EviAlign/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alexzhu0/EviAlign/actions/workflows/ci.yml)

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

EviAlign is the current project name; AgentHarness and ActLumen · 明行 are historical names. The existing `agentharness` command, Python package, protocols, and file paths remain compatible. Historical records retain the names used at the time. The source prerelease remains `v0.2.0-alpha.1`; this update is not a new version or package publication.

`allow_candidate` denotes candidate evidence only; current evidence and shadow outputs retain `result_status: not_executed`. This repository does not provide identity verification, trusted signatures, runtime authorization, approval semantics, transactions, or tool execution. [Full scope statement (中文)](docs/actlumen-brand-and-scope.md)

Licensed under the [MIT License](LICENSE).
