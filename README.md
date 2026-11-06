# EviAlign

**English** | [简体中文](README.zh-CN.md)

**Reviewable AI actions. Evidence for human oversight.**

EviAlign is a forward-looking research project on how enterprises can review AI-proposed business actions and use accumulated decisions and outcomes to study where human involvement is needed. Its current foundation is a pre-execution evidence-checking prototype; the complete business review-and-learning cycle is still future work.

**EviAlign** combines *evidence* and *align*: keeping an action request and its supporting evidence connected. Identity, authorization, approvals, and execution remain the responsibility of existing enterprise systems.

[Purpose and progress](docs/product/project-purpose-and-progress.md) · [Reviewer brief (中文)](docs/product/evialign-reviewer-brief.md) · [Current PowerPoint delivery record](docs/presentations/evialign-ppt-expanded-delivery.md) · [Documentation index (中文)](docs/README.md) · [Engineering guide](docs/guides/engineering-guide.md)

## Why this repository exists

Many enterprise agents still support questions, queries and analysis. EviAlign anticipates a possible next stage: agents helping redesign workflows, propose decisions and advance business processes. We want to investigate the basis for reviewing those actions before that stage becomes widespread.

The ambition is business sign-off before consequential AI actions: understand what an agent proposes, its supporting basis, and what needs a person's confirmation. In a future integration, records of proposals, human confirmations or modifications, and eventual outcomes could help identify which specific situations require human judgment and which might justify less intervention.

That cycle is a research goal. A high approval rate alone does not establish safety; outcomes, exceptions and changing conditions need validation. Any reduction in human intervention remains a scoped enterprise decision. [Full purpose and research path](docs/product/project-purpose-and-progress.md)

## Where we are today

**Evidence-checking foundation, separate synthetic experiments, and a local research-review workbench.** With a trusted request and retained evidence, this repository checks whether the evidence still corresponds to the current structured request and emits a bounded, deterministic result. The separate sandbox supports historical replay and an explicit live mode with DeepSeek proposals, independent initial judgments, Jev observations, final annotations and JSON export. It does not collect a complete business history or adjust oversight rules.

The separate sandbox has evaluated **Jev, TypeSafe's structured decision model**, to observe whether AI proposals align with user intent. Jev supplies an observation signal, while existing enterprise controls retain approval and execution authority. [Bilingual project description and Jev's role](docs/product/hackathon-entry.md)

| Responsibility | Current status |
| --- | --- |
| Identity, authorization, approval validity, and execution | Existing external systems remain responsible. |
| Structured request and evidence correspondence | Implemented in this repository, subject to trusted inputs and retained evidence. |
| User intent versus AI proposal | Optional Jev decision-model observation in a separate local business sandbox; its hints do not authorize execution. |
| Real approval records versus proposed business fields | Requires a separate design, trusted integration, and validation. |
| Research-review records | Separate local sandbox: initial/final judgments, historical replay or opt-in live DeepSeek/Jev calls, unassessed drafts and JSON export. |
| Observed business outcomes and changes to human involvement | Research goal; no trusted outcome integration, business-reviewer study or automatic adjustment is implemented. |

The current business evidence contract binds approval fields as supplied but does not interpret them. A receipt for one request will not match a changed request; matching digests alone do not authenticate the source, validate an approval, establish business correctness, or authorize execution. [Business evidence contract](docs/contracts/business-action-evidence-v1.md)

## Try the research-review prototype

From the **separate local** `agentharness-business-sandbox` repository, run
`./run-sandbox review --port 8769` and open `http://127.0.0.1:8769`.
Review an original case, save an initial judgment, reveal the retained Jev result,
then record a final judgment and export. Six seen synthetic cases are available;
no new model call or business action occurs. Records stay in memory until restart.
This is an engineering PoC; business colleagues have not yet trialed it.
[Launch, demonstration and scope](docs/guides/research-review-workbench.md)

For live calls, use `./run-sandbox review --live --port 8770` with the existing
provider configuration. On 2026-11-04, three DeepSeek and three OpenRouter/Jev
requests returned valid responses through the browser workflow. An actual
operation video and normalized trace were retained. Each service permits at most
three attempts per provider; synthetic inputs are sent externally and incur API
usage. [Actual results and limits](docs/guides/research-review-workbench.md#live-acceptance-on-2026-11-04)

## A business question to investigate

In a fictional delivery exception, sales, logistics and service teams need to coordinate. An AI could gather information, prepare follow-up suggestions and propose transferring a ticket; the responsible person may require confirmation before ownership changes. We want to study how to connect that proposed action, the relevant confirmation and its conditions, and the eventual outcome.

This is a future workflow illustration. Historical synthetic case E173 covers only a pending-confirmation ticket transfer, not a delivery exception or a connected approval workflow. [PoC provenance](docs/presentations/evialign-ppt-expanded-delivery.md#evidence-and-provenance)

## What evidence exists

A single run on **2026-10-21** in the separate sandbox used 84 synthetic intent-observation cases: all 36 overreach cases were flagged; all 24 unclear cases received review hints; and 3 of the 24 fitting cases also received hints.

The cases were AI-authored and independently blind-labeled by another AI, across 33 correlated scenario families. They are not human ground truth or Lenovo business data. These results do not establish production accuracy, real approval-to-action comparison, time savings, or ROI. [Full evaluation record](docs/research/33-jev-shadow-maintenance-handoff.md)

## How to assess the value

Existing APIs, fine-grained authorization, approvals and audit systems may already cover the necessary controls. An additional component must demonstrate a real gap or a measurable reduction in repeated integration and review effort.

Compare three approaches on one approved, read-only replay of a business workflow: the existing controls; practical improvements to those controls; and a proposed EviAlign integration. Measure discrepancies found, total handling time, extra review burden, integration and maintenance costs, and actual reuse across agents. If existing controls already suffice or costs exceed demonstrated benefits, retain the existing approach.

If the comparison justifies further work, separately design trusted business-record access and an observation study that accumulates human judgments and outcomes while existing controls remain in force. Researching changes to human involvement comes after validation and enterprise approval; the current prototype grants no execution authority.

## Find the right material

| Reader | Start here |
| --- | --- |
| Leaders and hackathon judges | [Purpose and progress](docs/product/project-purpose-and-progress.md), [reviewer brief (中文)](docs/product/evialign-reviewer-brief.md), [current PowerPoint delivery record](docs/presentations/evialign-ppt-expanded-delivery.md) |
| Business pilot owners | [Brand and capability scope (中文)](docs/product/evialign-brand-and-scope.md), including the proposed comparison and pilot |
| Developers and platform teams | [Engineering guide](docs/guides/engineering-guide.md), [asset map](docs/guides/00-asset-map.md) |
| Security and evidence reviewers | [Product contract](docs/contracts/08-glossary-and-product-contract.md), [reproducible demo](docs/guides/11-reproducible-enterprise-demo.md), [review checklist](docs/guides/13-external-reviewer-checklist.md) |
| Maintainers | [Current maintenance record](docs/maintenance.md), [repository guidance](AGENTS.md) |

The current formal PowerPoint has 20 pages, an embedded real-operation movie and a PDF copy, delivered locally. Its files and provenance are indexed in the [presentation record](docs/presentations/evialign-ppt-expanded-delivery.md). Superseded production drafts are available through the [fixed history links](docs/maintenance.md#archived-production-materials).

## Repository structure

The version-controlled folders are organized by purpose:

| Folder | Contents |
| --- | --- |
| [src/](src/) | Python implementation of the CLI, evidence checks and local evaluation/reporting logic. |
| [tests/](tests/) | Unit, CLI, adversarial-input and end-to-end evidence regression tests. |
| [docs/](docs/) | Project purpose, current progress, contracts, engineering guides, retained results and presentation-file locations. |
| [examples/](examples/) | Sample policies, synthetic evidence records and fixtures for local demonstrations and tests. |
| [schemas/](schemas/) | Policy, task, request/response and audit-document definitions, plus argument-canonicalization test vectors. |
| [policies/](policies/) | Tool-risk classifications and governance-policy data. |
| [patterns/](patterns/) | Machine-readable agent architecture and design patterns. |
| [evals/](evals/) | Local safety-case data, including smoke cases and declarative assertions. |
| [release/](release/) | Dated source-release, milestone and handoff records; an entry does not automatically mean a published release. |
| [.github/](.github/) | GitHub configuration, currently the automated CI verification workflow. |

<details>
<summary>Subfolders and example-fixture contents</summary>

| Subfolder | Contents |
| --- | --- |
| [src/agentharness/](src/agentharness/) | The Python package: command dispatch, validators, evidence binding, local evaluators and audit builders. |
| [.github/workflows/](.github/workflows/) | CI jobs that validate policies, evaluate local cases and run tests. |
| [docs/product/](docs/product/) | Project purpose, current progress, positioning and reviewer materials. |
| [docs/contracts/](docs/contracts/) | Evidence protocols, product boundaries and related Pi readiness/verification records. |
| [docs/guides/](docs/guides/) | Engineering reference, asset map, demonstrations and review instructions. |
| [docs/research/](docs/research/) | Integration research, independent-lab handoffs and retained DeepSeek/Jev results. |
| [docs/presentations/](docs/presentations/) | Presentation delivery index, artifact digests and recording provenance. PPT/video binaries are delivered separately. |
| [docs/superpowers/](docs/superpowers/) | Engineering-design index and links to historical implementation plans. |
| [docs/superpowers/specs/](docs/superpowers/specs/) | Retained engineering specifications and scoped design decisions. |

Each folder below is a self-contained synthetic fixture, not a live business workflow:

| Example folder | Demonstrates |
| --- | --- |
| [examples/agent_bus/](examples/agent_bus/) | Basic task, evidence, review and ledger structure. |
| [examples/agent_bus_tool_gate/](examples/agent_bus_tool_gate/) | Tool-policy gate evidence. |
| [examples/agent_bus_approval/](examples/agent_bus_approval/) | Correspondence checks for retained approval records. |
| [examples/agent_bus_preflight/](examples/agent_bus_preflight/) | Pre-execution readiness-report validation. |
| [examples/agent_bus_handoff/](examples/agent_bus_handoff/) | Handoff-report inspection. |
| [examples/agent_bus_adapter_registry/](examples/agent_bus_adapter_registry/) | Registry-backed adapter declarations; the main export, manifest and audit example. |
| [examples/pi_tool_call_mapping/](examples/pi_tool_call_mapping/) | Synthetic Pi-like observations and their expected mappings. |

The file-bus fixtures reuse these subfolder names where needed:

| Fixture subfolder | Contents |
| --- | --- |
| `tasks/` | Structured sample task requests. |
| `evidence/` | Retained attempt evidence referenced by the ledger. |
| `reviews/` | Review records for those attempts. |
| `tool_gates/` | Tool-policy gate reports. |
| `approvals/` | Sample approval records; not authenticated enterprise approvals. |
| `preflight/` | Saved preflight reports. |
| `handoffs/` | Saved handoff reports. |
| `adapters/` | Adapter specifications and, where present, their registry. |

</details>

<details>
<summary>Local folders that may appear outside the version-controlled tree</summary>

| Folder | Purpose |
| --- | --- |
| `.git/` | Git history and repository metadata. |
| `.superpowers/` | Temporary task progress and review drafts; separate from tracked `docs/superpowers/`. |
| `.cursor/` | Local Cursor editor settings. |
| `.worktrees/` | Isolated local Git checkouts used by other tasks. |
| `.understand-anything/` | Generated code-analysis index and local analysis settings. |
| `.venv/` | Local Python virtual environment. |
| `__pycache__/`, `.pytest_cache/` | Generated Python/test caches. |
| `artifacts/` | Generated local evaluation reports. |
| `build/`, `dist/`, `*.egg-info/` | Generated package/build output. |

Skills can recreate `.superpowers/` when needed, but recreating the directory
does not restore deleted progress records or review drafts. The independent
`agentharness-business-sandbox` lives in a separate repository, not in a folder here.

</details>

## Developer quick start

Run from the repository root with Python 3.10 or later:

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

See the [engineering guide](docs/guides/engineering-guide.md) for the complete command reference, contracts, runtime responsibilities, and historical milestones.

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

EviAlign is the current project name; AgentHarness and ActLumen · 明行 are historical names. The existing `agentharness` command, Python package, protocols, and source paths remain compatible. Historical records retain the names used at the time. The source prerelease remains `v0.2.0-alpha.1`; this update is not a new version or package publication.

`allow_candidate` denotes candidate evidence only; current evidence and shadow outputs retain `result_status: not_executed`. This repository does not provide identity verification, trusted signatures, runtime authorization, approval semantics, transactions, or tool execution. [Full scope statement (中文)](docs/product/evialign-brand-and-scope.md)

Licensed under the [MIT License](LICENSE).
