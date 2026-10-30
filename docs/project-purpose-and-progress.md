# EviAlign: purpose and current progress

**English** | [简体中文](project-purpose-and-progress.zh-CN.md)

Updated: 2026-10-30. This is the main repository's research purpose and status statement. It separates the long-term goal from the capabilities implemented today.

## Why this project exists

EviAlign researches how an enterprise can review AI-proposed business actions, retain the basis for those decisions, and accumulate evidence for deciding where human involvement is necessary.

The starting observation is that many enterprise agents still support questions, queries and analysis. The project anticipates a possible next stage: agents helping redesign workflows, propose decisions and advance business processes. That is a reason to investigate review and accountability early, rather than a claim that enterprises already need a new approval layer for every agent.

When an agent prepares to act, an enterprise should be able to examine what it proposes, the relevant business basis, the conditions that still apply, and who must confirm a consequential change. Afterward, it should be possible to relate the decision to the actual outcome.

“Sign-off before AI acts” describes the business ambition. The current implementation is an evidence-checking prototype; it does not implement trusted digital signatures or a complete approval service.

## The research hypothesis

Start with existing enterprise rules. In a future business integration, associate a proposed action with its supporting records, the responsible person's confirmation, modification or deferral, and the eventual business outcome. Study those records to identify recurring conditions, mistakes and exceptions.

That evidence could help an enterprise decide which narrowly defined situations still require human judgment and which might justify less intervention. Any adjustment would need validation and enterprise approval, a defined scope, continued observation and a way to restore review. This accumulation-and-adjustment cycle is a research goal, not an implemented capability.

A high approval rate is not proof that an action is safe. Human decisions can be wrong, rare failures can be missing, and business conditions can change. Review burden, independent checks and actual outcomes matter alongside approval history.

## What APIs, permissions and approvals already do

Existing systems remain responsible for identity, access, business approval validity, transactions and execution. They may already retain the relationship between a request, its approval and its result.

EviAlign's proposed contribution is to investigate whether reusable action-to-evidence checks and review records help across agents and systems. Compare that with improving the original systems. If those systems suffice, or can be improved more simply and cheaply, reuse them. The existence of an AI agent alone does not justify another component.

## Where we are today

**Current stage: partial foundation prototype plus separate synthetic observation experiments. The complete business review-and-learning cycle is still future work.**

| Area | What exists | What it does not establish |
| --- | --- | --- |
| Main-repository evidence checks | Check a structured current request against retained evidence and emit a bounded, deterministic result. A changed request does not match its old receipt. | No real approval-source integration, business-field interpretation or execution permission. The receipt is unsigned; if both inputs can be replaced, matching digests do not establish authenticity. |
| Separate local business sandbox | Synthetic business environment and optional Jev intent observations, with retained evaluations. | Not part of this repository's CLI; a review hint does not pause a workflow, approve an action or execute a tool. |
| Demonstration | An editable presentation and mock-data film show an actual read-only result capture, independent correspondence checks and a historical E173 observation. | These are separate demonstrations, not a connected enterprise approval transaction. |
| Human judgments and business outcomes | Defined as the next research direction. | No complete collection of business confirmations, reasons and outcomes, or validated method for reducing human intervention. |
| Enterprise value | Proposed comparison of existing controls, improvements to them, and a future EviAlign integration. | No measured enterprise time savings, ROI or production-safety claim. |

Current evidence and shadow results retain `result_status: not_executed`. `allow_candidate` means candidate evidence only. A successful check does not authorize a real action. See the [business evidence contract](business-action-evidence-v1.md).

## What the retained experiments tell us

On 2026-10-21, a single frozen-rubric run in the separate sandbox tested 84 then-unseen synthetic cases. All 36 overreach cases were flagged; all 24 unclear cases received review suggestions; 3 of 24 fitting cases also received attention. One unclear case received a different class label but still a review suggestion, so this is not 84 correct classifications.

The cases were AI-authored and independently blind-labeled by another AI across 33 correlated scenario families, not human ground truth or Lenovo production data. Zero observed misses does not imply zero future risk. The results support further study of observation hints under those conditions; they do not validate a full approval workflow, business-outcome learning, production accuracy or ROI. [Evaluation record](33-jev-shadow-maintenance-handoff.md)

## A business question to investigate

A fictional delivery exception involves sales, logistics and service teams. An AI could gather information, prepare follow-up suggestions and propose transferring a ticket. The responsible person may want to confirm a change of ownership before it happens.

The research question is how to distinguish preparation from a business commitment, relate the proposed action to the relevant confirmation and conditions, and retain the eventual result for review. The full scenario is a future workflow illustration. Historical synthetic case E173 covers only a pending-confirmation ticket transfer; it does not establish a delivery exception or a working approval integration. [PoC provenance](presentations/evialign-ppt-poc-delivery.md)

## What comes next

1. Choose one workflow segment with business and system owners; establish whether a repeatable gap exists in the current controls.
2. Design trusted, read-only access to the relevant business confirmations and state. Define the proposed action, applicable conditions, human decision and outcome records needed for the research.
3. Use approved historical or synthetic records to compare existing controls, practical improvements and the proposed EviAlign capability. Measure discrepancies, total handling and review time, extra attention, rework and integration cost.
4. If justified, separately design a side-by-side observation study to accumulate judgments and outcomes without changing existing execution controls.
5. Only after further evidence and enterprise approval, study limited changes to human involvement. A real execution integration requires a separate external-runtime design, implementation, adversarial testing and approval gate.

These are proposed research steps, not authorization to access real business data, launch a new paid evaluation or integrate execution. Stopping when there is no incremental value is a valid research outcome.

The aim is to make each action's basis reviewable and each future change in oversight evidence-based.

## Reading onward

- [English project homepage](../README.md) and [Chinese homepage](../README.zh-CN.md)
- [Brand and capability scope](actlumen-brand-and-scope.md)
- [Reviewer brief](actlumen-reviewer-brief.md)
- [Current PowerPoint delivery record](presentations/evialign-ppt-expanded-delivery.md)
- [Engineering guide](engineering-guide.md)
