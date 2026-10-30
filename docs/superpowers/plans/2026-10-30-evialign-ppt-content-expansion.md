# EviAlign PPT content expansion plan

> **For agentic workers:** Use superpowers:executing-plans for this presentation iteration; perform one independent final review.

**Goal:** Deliver a fuller, editable executive hackathon presentation, retaining the approved positioning, visual direction and existing mock PoC movie.

**Architecture:** Iterate the approved 2026-10-29 presentation design. Use huashu-design's deck module, HTML source pages, rendered DOM-to-PowerPoint conversion with the existing deck as template, and native Windows PowerPoint verification. Deliver a separate content-enhanced file and a PDF, preserving the previous deck and movie.

**Tech Stack:** huashu-design 3.0.0, local Playwright, python-pptx, Windows PowerPoint.

**Spec:** ../specs/2026-10-29-evialign-ppt-poc-film-design.md

## Constraints

- User requests more substantive content, not a new product design. Keep the previously approved frontier research positioning and delivery-exception / pending-transfer scenario.
- Existing implementation, independent synthetic sandbox observations, future workflow and value hypotheses must remain distinguishable.
- Keep enterprise identity, permissions, approval and execution responsibilities explicit. Evidence and Jev observations do not authorize execution; retain `not_executed`.
- No paid requests, credentials, sandbox changes, tags, publication or new execution integration.
- Deliver under `D:\Sayitout\小强创新` as `EviAlign-黑客松汇报-内容增强版.pptx` and matching PDF. Preserve earlier files.
- Authoring sources and temporary skill scripts go under `/tmp/evialign-ppt-expanded`; keep production-source archive with the delivery.

## Review focus

Business readability; substantive distinction from existing API/approval controls; honest interpretation of the 84-case historical evaluation; native text and slide editability; presentation-engine layout and embedded video playback.

## Tasks

### Task 1: Editorial expansion

- [x] Verify primary industry sources and current project evidence.
- [x] Write 16 main slides plus four appendix slides with speaker notes: importance, timing, industry, incremental research question, workflow, scenario, decision boundaries, recording and learning path, implementation, PoC, evaluation, value, next steps and hard questions.
- [x] Record why this uses the same-project iteration exception to huashu-design's three-direction gate, and inherit the previously approved design rather than inventing new style directions.

### Task 2: Presentation production

- [x] Build independent 1920×1080 HTML slide pages and the skill's overview shell.
- [x] Convert rendered elements into native PowerPoint objects using the existing deck as template; embed the unchanged MP4, add notes and links.
- [x] Inspect browser renders, text completeness and bounds. Archive source and exact third-party provenance.

### Task 3: Review and delivery

- [x] Independently review claims and visuals, correct material findings.
- [x] Open and export the final deck in native Windows PowerPoint, verify all pages and embedded playback, deliver PDF and PPTX and record hashes.
- [x] Run the repository's six required checks if committing maintenance records. Stage only explicit documentation paths; report actual Git sync state.

## Execution notes

This is a presentation-content iteration of an approved design, not a runtime behavior change. No new software regression tests are warranted; validation targets document fidelity, business claims, layout and media instead.
