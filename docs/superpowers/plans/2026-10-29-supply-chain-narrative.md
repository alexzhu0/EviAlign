# Supply-chain leadership narrative implementation plan

> **For agentic workers:** Use superpowers:executing-plans. The user approved the linked design and asked for implementation; do not add redundant approval gates. Steps use checkbox syntax.

**Goal:** Replace the refund-led pitch with a supplier procurement story, beginning with sourced industry context and adding short HR and sales examples.

**Architecture:** Update the existing four-page reviewer Markdown, bilingual README example and eight-slide, offline HTML in one coherent change; generate Windows deliverables from the reviewed sources, then fast-forward the existing repository. No runtime code or model behavior changes.

**Tech stack:** Markdown, existing standalone HTML/CSS/JavaScript, temporary Python document tools and Playwright, Git, GitHub.

**Spec:** `docs/superpowers/specs/2026-10-29-supply-chain-narrative-design.md`, approved 2026-10-29.

## Global constraints

- Procurement is synthetic: supplier 甲, 1,000 devices, delivery 12 月 15 日; compare unchanged, 1,500 units, and 12 月 20 日. Changes can be legitimate; the existing business process judges them.
- NIST initiative is research, WEF/Capgemini ACAP is a whitepaper framework, Microsoft Copilot Studio offers human-in-the-loop actions. Link the primary sources without implying affiliation or product integration.
- Existing controls may suffice. Keep three-arm comparison, proposed-only field comparison and credible integration, unproven ROI, AI-authored/blind-labeled 84-case limitations, and the `allow_candidate` / `result_status: not_executed` boundary.
- Preserve technical commands, CI section, eight slides, offline use, keyboard navigation and historical material. Do not modify runtime authorization, models, thresholds or `.cursor/`.
- The user approved normal GitHub sync and Windows delivery; back up existing named deliveries first. No tags, releases or packages.

## Review focus

- Three supply-chain states, tab labels, visible fields, static no-JS and printed summary must agree and explicitly remain hypothetical.
- Print-visible industry sources must be accurate and accessible as links, without fabricating official standards or claiming external affiliations.
- Distinguish current request binding from future comparison of business fields; never imply the project authorizes, signs or executes.
- Source limitations, additional review burden and plausible reuse of existing mechanisms must be visible to leaders.
- Windows deliverables must match reviewed sources, preserve old versions and have no clipped content; README CI contract remains byte-for-byte stable.

### Task 1: Rewrite the linked sources and validate the complete deliverable

**Files:** Modify `README.md`, `README.zh-CN.md`, `docs/actlumen-reviewer-brief.md`, `docs/presentations/agentharness-enterprise-hackathon.html`, `docs/superpowers/specs/2026-10-29-supply-chain-narrative-design.md`; create this plan. Add a dated maintenance note to `docs/34-actlumen-brand-maintenance.md`.

- [ ] Mark the design approved. Rewrite the brief with sourced industry context, the synthetic supply-chain example, HR/sales extensions, current capability, limitations and a three-arm pilot.
- [ ] Rewrite the slide content and scenario data, preserving the existing controls; fit eight slides. Replace the two README examples while preserving each CI section.
- [ ] Exercise the three cases in the browser, navigation, mobile, offline and no-JS presentations. Render four A4 brief pages and eight slide pages, inspect content geometry and PDF text. Generate DOCX and verify its content and structure.
- [ ] Verify source links and all six AGENTS.md commands plus the README CI contract; expected exit status 0 and no missing local links. No new repo tests mirroring presentation copy.
- [ ] Stage the six named sources and plan only, inspect the staged file list and `git diff --cached --check`, then make a scoped commit.

**Final task command:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q` (expected: all tests pass).

## Review and delivery

- [ ] Request one independent review of the source against the approved spec and Review focus; resolve material findings and reverify.
- [ ] Generate final Word/HTML/PDF and slide HTML/PDF in temporary storage; confirm page count, actual rendering and source-to-output match. Preserve existing Windows files with dated backups before replacing them, and verify hashes.
- [ ] Fast-forward the user's local `main` only after confirming it is still at the expected design commit. Fetch remote main without tags, push normally, and verify the exact remote SHA, bilingual README blobs and CI result.
