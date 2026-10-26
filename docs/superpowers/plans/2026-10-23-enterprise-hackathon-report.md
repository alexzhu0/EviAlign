# Enterprise Hackathon Report Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for the already approved single-file presentation; request one independent review before handoff.

**Goal:** Deliver an attractive Simplified Chinese, eight-slide, offline HTML report for the internal theme “AI empowering enterprise workflows”.

**Architecture:** One standalone document under docs/presentations. Inline CSS, JavaScript and SVG; no runtime, provider, CDN, server, build system or product-code changes. Keep the accepted white/navy/teal cover, typographic hierarchy, outlined evidence-flow artwork, toolbar and footer. Reuse its visual system for seven content slides.

**Tech Stack:** Native HTML/CSS/JavaScript; isolated agent-browser with installed Chrome for QA, Node assertions in temporary QA files.

**Spec:** The user approved the in-chat eight-slide design and cover image on 2026-10-23 by replying “确认”. This plan records that scope without a new approval gate.

## Global constraints

- Eight slides: cover; workflow opportunity; refund example; roles/architecture; selectable static scenarios; retained 84-case evaluation; enterprise value and proposed measures; proposed pilot roadmap and evidence sources.
- All visible copy in Simplified Chinese except project/tool names and evidence labels.
- Single file: docs/presentations/agentharness-enterprise-hackathon.html; file:// must work offline. No generated image dependency: the concept's geometric illustration is code-native SVG.
- UI: table of contents, previous/next, Home/End/arrow navigation, fullscreen, print all eight slides to PDF, static scenario tabs, responsive reading, reduced-motion and no-JS fallback.
- Current evidence: 84 synthetic cases; overreach miss0/36 (36 flagged), unclear miss0/24 (24 review), fits review3/24, false flags0/24, labels83/84, costUS$0.003486756; dates/AI-label/family-correlation limitations visible.
- AgentHarness validates supplied evidence bindings; Jev observes intent in a separate sandbox; external runtime owns identity/authorization/execution. Keep not_executed. No pretend live validation, new model calls, ROI numbers or production claims.
- Future pilot and business metrics must be labeled proposals/unmeasured. No automatic commit, push, deployment or sandbox changes for this report delivery. Existing .cursor and unrelated worktrees untouched.

## Tasks

- [x] 1. Write and run meaningful temporary browser acceptance assertions before implementation: offline opening, eight-page navigation, boundaries, TOC, scenario state, print, mobile overflow.
- [x] 2. Implement the complete document and run assertions to green; inspect cover at concept native1672x941, other slides at1366x768 and mobile390x844. Match palette, typography, composition, illustration, toolbar/footer and cover copy. Validate print pagination and script-disabled fallback.
- [x] 3. Run required AgentHarness checks, inspect source/data accuracy, request independent review, fix material issues, remove temporary project artifacts and hand over file link.

## Review focus

1. History/deep-link boundaries must not leave zero visible slides.
2. Keyboard controls must respect dialogs and focused interactive elements.
3. Demo state must not imply current-call evidence/assessment reuse or actual tool execution.
4. Print must include all eight slides even when screen slides are hidden.
5. Small screens and no-JS mode must retain readable content and core navigation.

Verification: browser acceptance and screenshots plus the six AGENTS.md commands. No Python evidence-contract behavior changes, so extra evidence suite is not applicable.

## Execution and verification — 2026-10-23

- Temporary browser acceptance started red because the offline document was absent, then passed against the implementation. Navigation boundaries, valid/invalid deep links, dialog selection, tab changes, print invocation, and all eight mobile pages were checked.
- No built-in Browser/IAB was available. Used agent-browser with an isolated system Chrome session, then its CDP interface for print and script-disabled checks. No external requests were needed to display the report; a reload while offline passed. Fullscreen entry/exit passed and the browser recorded no page errors.
- Viewed the approved concept and final Chrome capture with `view_image`, at the concept's native 1672×941. Also inspected all eight desktop pages at 1366×768, mobile cover/demo/results/closing at 390×844, and the print evaluation page. Desktop pages fit exactly within 1366×768; mobile pages had no horizontal overflow. Small-screen headings balance across lines and navigation follows long content instead of covering it.
- Printed all eight hidden/visible sections at 1280×720 CSS pixels each. The final PDF has exactly eight pages, each 960×540 PDF points (16:9), with no trailing blank page. Content bounds fit within every page. Disabling JavaScript in Chrome yields eight visible sections and the continuous-reading explanation.
- Independent read-only review found one important sample-tool mismatch and two minor issues. Fixed the tool to `request_refund`, kept skip-link focus on the current page, and explicitly identified the independent labels as AI-produced, not human ground truth. Reviewer rechecked these fixes and reported no remaining Critical/Important issues. An additional print regression proved and fixed a 1px screen-reader-text overflow that had produced a ninth blank page.
- All six required repository checks passed: policy validation; three smoke evaluations; both loop fixtures; 538 unit tests in 45.683 seconds; `git diff --check`. Every Python invocation disabled bytecode. Checked the new untracked document and plan separately for whitespace because ordinary Git diffs do not include untracked files.
- No product code, runtime authorization, sandbox files, provider evaluations, commits, pushes or deployment were part of this delivery.

### Visual fidelity ledger

| Comparison | Evidence and correction | Final assessment |
| --- | --- | --- |
| Cover copy | Matched both headline lines, subtitle, supporting sentence, toolbar labels and footer to the approved concept; no added visible cover copy. | Match |
| Layout and spacing | Compared left headline/right layered artwork, generous white space and inset progress rail; corrected initial margins and footer position. | Match to approved composition |
| Typography | Increased initial headline size/weight and subtitle size; all controls have explicit typography. | System-font glyphs vary by platform; no external font dependency |
| Palette | Pure white background, navy text, teal evidence plane and accents, pale blue-gray rules; no added gradients. | Match |
| Artwork and icons | Rebuilt the approved layered planes, person/document/search/cube metaphors and connecting ring in inline SVG; corrected initial generic icons. | Code-native SVG, as approved |
| Responsive/print | Balanced mobile headings, flowed long-page footer, all eight printable pages and readable footnotes. | Verified in Chrome |

The approved image is a visual reference, not a bundled asset. Inline SVG and system fonts are the recorded intentional adaptations for a self-contained offline document. No material visual or functional issue remains from the checks above; cross-browser/device-specific glyph rendering was not exhaustively tested.
