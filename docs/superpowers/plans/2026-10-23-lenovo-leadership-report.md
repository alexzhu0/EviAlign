# Lenovo Leadership Report Revision Plan

> **For agentic workers:** Use superpowers:executing-plans for this continuation of the existing inline document task, with one fresh read-only review at the end.

**Goal:** Deliver a leadership-oriented Chinese HTML report explaining the project, business scenarios, employee efficiency and enterprise benefits for the Lenovo Group hackathon.

**Architecture:** Preserve the existing eight-page native HTML/CSS/JS document and its approved white/navy/teal visual system. Replace the technical narrative with business copy; change the three static case tabs to customer service, sales operations and finance. Keep detailed evidence and implementation boundaries in an expandable appendix.

**Tech Stack:** Existing single-file HTML/CSS/JS/SVG, isolated agent-browser/Chrome QA, temporary browser assertions.

**Spec:** `docs/superpowers/specs/2026-10-23-lenovo-leadership-report-design.md`; the user's direct editorial correction is the authority for this revision, not a new product implementation.

## Global constraints

Business benefits and employee review-page integration are proposed, not measured/delivered. No invented Lenovo deployment or ROI. Prototype still supplies evidence correlation and intent observations; existing enterprise approval/execution remains separate. Retain synthetic evidence limitations and not_executed in the appendix. No external resources required for viewing, no provider calls, product code, sandbox changes, commits or pushes. Update the authorized D-drive copy only after QA, retaining its prior content as a technical-version backup.

## Tasks

- [x] 1. Add a temporary browser acceptance test for the three business cases, assert that switching changes the request/benefit/attention texts and keeps case keyboard focus; run it against the current document and observe the expected missing-case failure.
- [x] 2. Replace the eight-page narrative and static cases; retain navigation/accessibility. Visually check the cover, all desktop pages, mobile and print. Test offline, eight-page navigation and PDF, keyboard tabs, no-script fallback, and fit without overlap.
- [x] 3. Run the six AGENTS.md checks, request fresh read-only review of content truth and UI, resolve material findings, copy/verify the finalized HTML to D drive, preserve the earlier technical version, and remove task-specific QA artifacts.

## Review focus

1. Business wording must not imply autonomous approval/execution or a delivered employee-facing product.
2. Efficiency and enterprise value must be concrete but explicitly unmeasured; no invented Lenovo facts.
3. All three scenario tabs must update their full content, including accessible tab labels and keyboard behavior.
4. Long Chinese headings and the appendix must remain readable on small screens and all eight printable pages.
5. Source and D-drive delivery must match byte-for-byte, with prior destination content retained.

## Execution notes

- Continue in place on the already authorized uncommitted report. The user requested correcting this exact artifact and its existing delivery location; no branch integration or new approval gate is part of the task.
- Preserve the accepted visual system instead of generating a new aesthetic concept: the correction concerns leadership communication and content hierarchy.

## Verification and delivery — 2026-10-23

- Business-case acceptance failed first on the old document's missing customer-service case, then passed on the new document. Verified all seven case fields, selected tab, accessible panel name, keyboard wrap/focus, directory, skip-link, page boundaries, invalid deep links, offline reload and mobile overflow.
- No built-in browser was available. Used an isolated agent-browser/system Chrome session, with CDP for printing and script-disabled checks. Fullscreen entry/exit worked; no page errors or required external resources were observed.
- Inspected all eight desktop pages at 1366×768; each fit exactly within the viewport. Captured the cover at the approved concept's native 1672×941 and viewed it alongside the concept with `view_image`. Inspected mobile cover, scenario, efficiency, value, results and closing at 390×844.
- Printed exactly eight 16:9 pages, with every section 1280×720 CSS pixels. Printed content ended before the footer area on all pages. Disabling JavaScript left all eight sections readable.
- Expanded-appendix inspection found that the inherited sticky footer overlapped long content. A focused browser assertion failed on `sticky`, then passed after expanded-appendix footers were moved into normal document flow. Collapsing restores presentation navigation. Re-ran business-case and full visual/print checks after this fix.
- Fresh read-only review found no Critical, Important or Minor issues. It checked business clarity, proposed versus delivered capability, synthetic-result accuracy, approval boundaries, case updates and keyboard behavior. Its deferred-to-author checks (visuals, repository commands and destination integrity) were completed here. Raw sandbox evaluation was outside scope; all numerical statements remain attributed to the retained dated sources, without a new provider run.
- All six AGENTS.md commands passed: policy validation, 3/3 smoke cases, both loop fixtures, 538 unit tests in 37.476 seconds, and `git diff --check`. Python bytecode was disabled. No evidence-contract source changed, so the extra evidence suite did not apply. New untracked documents were also checked directly for whitespace and HTML reference integrity.
- Updated `D:\Sayitout\小强\agentharness-enterprise-hackathon.html` (65,055 bytes) and verified its bytes against the source. Preserved and verified the previous destination as `agentharness-enterprise-hackathon-技术版.html` in the same directory.
- No deferred review findings. No commits, pushes, sandbox modifications, real-data pilot, deployment or new model evaluation.

## Visual/content fidelity record

| Point checked | Result |
| --- | --- |
| Copy | Intentionally replaced the engineering narrative under the user's correction; cover says “让 AI 走进业务 / 让协作更有把握”, and event context is Lenovo Group hackathon. Technical vocabulary appears only in the expandable appendix. |
| Hierarchy | Larger conclusions, plain business explanations and a small number of visible ideas per page. Business scenarios and before/after workflow replace code and architecture internals. |
| Composition | Retained left cover headline, right layered illustration, open layouts, generous space, inset progress rail and restrained toolbar. |
| Palette | Retained pure white, navy, teal and pale gray rules; no invented corporate logo or external brand assets. |
| Artwork/icons | Retained inline SVG and outline controls; plane labels now say business needs, AI plan, action review and business system. |
| Responsive reading | Chinese heading phrases stay together; mobile footers follow long content. Expanded appendix also uses document flow on desktop. |
| Print | Eight pages with no trailing blank page and no content past the footer area. |

Remaining adaptations are intentional: the user-directed business copy and labels, system fonts for offline portability, and native SVG instead of a bundled concept raster. Cross-browser/device glyph differences were not exhaustively tested.
