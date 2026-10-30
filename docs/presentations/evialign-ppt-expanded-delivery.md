# EviAlign expanded PowerPoint delivery — 2026-10-30

The user requested another huashu skill and a more substantive PowerPoint. This is an iteration of the [approved presentation design](../superpowers/specs/2026-10-29-evialign-ppt-poc-film-design.md), following the [content-expansion plan](../superpowers/plans/2026-10-30-evialign-ppt-content-expansion.md). The original eight-slide deck and independent movie were preserved.

## Current reviewer edition: links and click-to-play — 2026-10-30

The user requested a clickable repository address and a prominent central movie-play button. The existing content-enhanced PPTX was locked by another Windows process, confirmed by an exclusive-file-open check. It was preserved, and a separate reviewer edition was delivered in the same `D:\Sayitout\小强创新` directory:

- `EviAlign-黑客松汇报-审稿版.pptx`: 20 slides and 309 native text shapes. Slide 16 has clickable project-home labels and URL; slide 20 links directly to the Chinese purpose-and-progress document. Slide 12 has a prominent play poster and an explicit native PowerPoint first-click Media Play effect.
- `EviAlign-黑客松汇报-审稿版.pdf`: matching native PowerPoint export, with all three project hyperlinks retained. The video poster is static in PDF.
- `EviAlign-审稿版讲稿.md` and `EviAlign-审稿版制作源文件.zip`: updated notes and maintainable production source, including the PowerPoint-authored playback timing.

Reviewer PPTX SHA-256: `7fd00f9645415cac22d6b32c5e7af7d3382ed0447c162d4a13aa948ced7dcac5`.

Reviewer PDF SHA-256: `4bc8bf92a0cb1bfcadebb3a0be2433985c1052c778569a7b92e54880a2df0a86`.

The project links are [the GitHub homepage](https://github.com/alexzhu0/EviAlign) and [the Chinese purpose-and-progress statement](https://github.com/alexzhu0/EviAlign/blob/main/docs/project-purpose-and-progress.zh-CN.md). GitHub metadata was read back: the repository remains private. Reviewers need the existing access permission; this update does not change visibility or grant access.

Native PowerPoint opened and exported all 20 final pages. A click-message test targeted only the newly created fullscreen `screenClass` window: before the click, slide 12 / player state 3; afterward, still slide 12 / state 0 (Playing) / position 3451 ms. Initial default-media click handling advanced the slide in this automation, so an explicit [native Media Play effect](https://learn.microsoft.com/en-us/office/vba/api/PowerPoint.Sequence.AddEffect) was added; it starts on the first slide click, including the central play area, without macros, external programs or autoplay. Direct physical-cursor testing was refused when Windows did not allow foreground focus; the successful final test used messages to the owned slideshow window without moving the cursor or clicking another application.

The final PPTX and PDF links, media relationships, native timing and unchanged movie bytes were checked. Browser and native previews were inspected; the 20-page PDF contains no out-of-page text. A fresh independent reviewer found no Critical, Important or Minor issue and rechecked the final native timing and links, but did not personally run the Windows click test. The source generation script inherits that timing. The final layout check has zero red findings and the same expected advisory for a bundled relative HTML poster.

All six repository checks passed, including 538 unit tests in 42.232 seconds. Only this delivery record changes in the repository; runtime code, business behavior, the separate sandbox and the movie itself are unchanged. Previous local files were retained, with pre-edit enhanced-file backups under `.evialign-production-expanded/backup-641a502b`.

## Earlier content-enhanced delivery

Directory: `D:\Sayitout\小强创新`.

- `EviAlign-黑客松汇报-内容增强版.pptx`: 20 editable slides, comprising 16 main pages and four appendices; 306 native text shapes, speaker notes, primary-source links and the unchanged embedded PoC movie.
- `EviAlign-黑客松汇报-内容增强版.pdf`: all 20 pages exported by native Windows PowerPoint.
- `EviAlign-内容增强版讲稿.md`: slide text and speaking guidance.
- `EviAlign-内容增强版制作源文件.zip`: HTML pages, source generators, fonts and licenses, existing-template derivative, movie, checks and relevant third-party script/license provenance. This local production archive is not a runtime dependency or a Git binary artifact.

PPTX SHA-256: `641a502b2ccfac9edcb5301fb620c83b69adb54184435857737e0ad5c378ec4f`.

PDF SHA-256: `f66468992c98bfe1d59a8a8bf4b1f37dc9eb09c004ea739bc36c8ec4e2e02e8f`.

The embedded movie SHA-256 remains `08e27db4761198c998166e99b21626018b4ba0bc4c181c2e844bd207263d3c0b`, matching the original standalone movie. Its provenance and remaining limitations are recorded in the [original delivery](evialign-ppt-poc-delivery.md).

## What became more substantive

The deck now explains the research timing, three types of existing industry work, the relationship with API permissions and approvals, a richer cross-team supply-chain exception, proposed human/AI responsibilities, action categories, the proposed decision record, the evidence needed before reducing human involvement, implemented versus future capabilities, the PoC, historical evaluation signals, enterprise value measures, and a staged validation proposal. Appendices cover existing mechanisms, the unsigned correspondence contract, evaluation details and executive questions.

The new material explicitly permits a conclusion that existing systems already suffice or that improving them is cheaper. Enterprise benefits remain hypotheses, with proposed measures rather than invented ROI. The supply-chain background and complete workflow are research illustrations; E173 remains only the historical pending-confirmation transfer example. A review suggestion is not described as actual entry into an approval workflow. Evidence/observations remain `not_executed` and do not grant runtime authorization.

## Skill and source verification

[huashu-design 3.0.0](https://github.com/alchaincyf/huashu-design) was read and used for its deck workflow, actual overview shell, actual rendered-DOM-to-editable-PPTX builder and text-completeness comparison, and actual design-lint script. The existing PPTX supplied the template. Its documented same-project iteration exception applied to the previously approved direction; no new visual direction was presented as user-approved. Browser launch was adapted to the installed Chrome; local production records were stored under the task's temporary directory rather than installing a global skill.

Primary sources were reopened on 2026-10-30: [NIST's initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative), [WEF and Capgemini's ACAP white paper](https://www.weforum.org/publications/ai-agents-in-action-a-playbook-for-trusted-adoption-authorization-and-scaling), and [Microsoft's agent-flows documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview). These are distinct research, framework and product outputs, not project partners or proof of a completed universal standard.

## Checks and review

- The final browser-to-PPTX comparison found no missing text across 20 pages. All pages have speaker notes, and exactly one embedded movie appears on page 12.
- huashu-design's final check found zero red findings. One yellow advisory concerns the HTML source's relative poster path; this is intentionally packaged inside its multi-file source directory. The delivered PPTX contains the actual media and requires no external poster file.
- A fresh independent reviewer read all page text/notes, checked project evidence and inspected seven browser renders. No Critical issue was found. The Important wording about review hints and the two Minor wording issues were corrected and checked in the final output.
- Native Windows PowerPoint opened the final deck, exported every page, and played the embedded movie with `Player.State = 0` (Playing). The initial full native-render contact sheet and the final corrected pages were visually inspected. The final PDF has 20 pages, the corrected review wording and no out-of-page text blocks. The delivered PPTX hash matches the checked source file.
- All six AGENTS.md commands passed: policy validation; 3/3 smoke cases; both loop fixtures; 538 unit tests in 42.038 seconds; and whitespace checks. No evidence-contract or runtime code changed.

No paid model request, credential-file access, new evaluation batch, sandbox modification, real business approval or execution, tag, release or deployment was part of this presentation task. This expansion does not revalidate the unchanged movie's narration or remove the original synthetic-evaluation limits.

Temporary source: `/tmp/evialign-ppt-expanded`. Native PowerPoint previews: the destination's `.evialign-production-expanded` directory. Delivery and source-archive checks are retained there and in the source archive.
