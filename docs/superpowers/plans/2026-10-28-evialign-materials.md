# EviAlign Materials and Repository Branding Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this approved documentation plan. Preserve the user's explicit instruction to complete the work without redundant permission requests. Steps use checkboxes for tracking.

**Goal:** Present EviAlign's pre-execution evidence checks accurately to business and technical readers, and deliver the requested reviewer materials and GitHub update.

**Architecture:** Rework the existing four-page Markdown reviewer brief, eight-slide offline HTML, bilingual README and current navigation/brand statements. Export the brief to editable DOCX and A4 HTML/PDF and export the existing slide deck to PDF; the external-runtime and synthetic sandbox boundaries remain unchanged.

**Tech Stack:** Markdown, existing standalone HTML/CSS/JavaScript, isolated temporary document-rendering tools, Python unittest, Git and GitHub.

**Spec:** `docs/superpowers/specs/2026-10-27-action-consistency-materials-design.md`, explicitly approved by the user on 2026-10-28.

## Global constraints

- The user selected EviAlign despite a separately identified same-name AI research paper. Do not claim trademark or domain availability.
- English is the default README; provide a linked Simplified Chinese README. Do not invent a new Chinese product name.
- Clearly separate current request/evidence correlation, optional Jev intent observation in the separate sandbox, and future business-level comparison of real approval details with a proposed action.
- Describe existing API, authorization and approval capabilities fairly. Compare current controls, improved existing controls, and a proposed EviAlign addition; a stand-alone platform is justified only by measured incremental value.
- Keep `result_status: not_executed`; `allow_candidate` is candidate evidence only. No runtime authorization, signing, approvals, code behavior, models, thresholds, or paid calls change.
- Retain the 2026-10-21 synthetic evaluation with 36/36 overreach flags, 24/24 unclear review hints, 3/24 fit review hints, 33 correlated families, AI-authored/blind-labeled caveats; do not treat it as proof of the new business-field comparison.
- Preserve the exact README `## Continuous Integration` contract and unchanged `.github/workflows/ci.yml`; preserve `agentharness` compatibility names and historical records.
- The native managed worktree was created read-only by this environment; in accordance with the worktree skill's sandbox fallback, work in the existing authorized checkout with explicit paths only. Leave `.cursor/` and unrelated worktrees alone.
- The user approved the GitHub repository rename, content sync and Windows delivery as part of the spec. Do not create tags, releases, packages or a new sandbox remote.

## Review focus

- A reader must not infer that current code compares real approval amounts with action amounts or validates approval identity.
- Every matching or changed example is explicitly a static proposed scenario, not a real Lenovo result or a completed runtime gate.
- Former-brand operational links resolve after GitHub rename; historical commit-pinned links and identifiers remain understandable.
- Every printed page and every interactive example remains legible, linked to the retained evidence limitations, and usable offline.
- No file outside the owned list, generated document, local credential, unrelated worktree or `.cursor/` enters the commit.

### Task 1: Rewrite, verify and commit the reviewed source

**Files:** modify `README.md`, `README.zh-CN.md`, `docs/README.md`, `docs/actlumen-reviewer-brief.md`, `docs/actlumen-brand-and-scope.md`, `docs/presentations/agentharness-enterprise-hackathon.html`, current brand-facing docs that explicitly use the old name, and `docs/34-actlumen-brand-maintenance.md`; add this plan and the approved spec. Keep stable filenames where compatibility matters.

- [ ] Replace broad product-value claims with the approved single refund scenario and three contrasting cases; describe business-field comparison as proposed.
- [ ] Replace the interactive deck's three static examples without changing its navigation logic, and carry evidence caveats into print-visible text.
- [ ] Keep the English-first README, Chinese counterpart, developer commands, compatibility notes and the exact folded CI section.
- [ ] Independently review claims, project name consistency and product boundary. Correct any material findings.
- [ ] Run the README CI contract test, link/whitespace and interaction checks, then all six commands in AGENTS.md. No implementation code or feature behavior changes; do not add tests that merely mirror copy.
- [ ] Stage only the reviewed named paths, inspect `git diff --cached --name-status`, run `git diff --cached --check`, and make one scoped documentation commit.

### Task 2: Deliver Windows materials and synchronize the existing GitHub repository

**Files:** create `EviAlign-项目评审材料.docx`, `.html` and `.pdf`, plus `EviAlign-项目汇报.html` and `.pdf`, under `D:\Sayitout\小强`; update the existing generic HTML entry; retain prior brand files as backups.

- [ ] Generate editable DOCX and A4 HTML/PDF from the final reviewer source in temporary storage; confirm complete text, four A4 pages, page layout and DOCX structure.
- [ ] Generate the offline eight-slide HTML/PDF from the final deck; check desktop/mobile, scenario switches, offline operation and print layout. Compare copied files to their source bytes.
- [ ] Rename `alexzhu0/ActLumen` to `alexzhu0/EviAlign`, update origin and GitHub About/homepage/topics without changing the repository ID, privacy or default branch.
- [ ] Fetch without tags, confirm a normal fast-forward, push the reviewed commit and verify the exact remote main SHA and both READMEs. Check the resulting GitHub CI status.
- [ ] Report the exact delivered Windows paths, GitHub URL and actual validation outcome, including any environment limitation or blocked action.
