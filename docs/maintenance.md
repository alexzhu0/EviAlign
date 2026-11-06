# Project maintenance

Updated: 2026-11-06. Current maintenance entry for EviAlign. The user reports
that hackathon registration has closed and the earlier materials were uploaded.
This does not independently verify a competition submission or submit a new one.

## Current sources

- [Purpose and progress](product/project-purpose-and-progress.md) · [中文版](product/project-purpose-and-progress.zh-CN.md)
- [Research-review workbench and actual live acceptance](guides/research-review-workbench.md)
- [Retained Jev evaluation](research/33-jev-shadow-maintenance-handoff.md)
- [Final presentation files and provenance](presentations/evialign-ppt-expanded-delivery.md)
- [Engineering guide](guides/engineering-guide.md) · [Repository rules](../AGENTS.md)

## Documentation layout on 2026-11-06

After the user approved a light organization pass, 36 documents moved from the
`docs/` root into four groups: [project introduction](product/),
[technical contracts](contracts/), [usage guides](guides/) and
[research/handoffs](research/). This index and the [documentation index](README.md)
remain at the root; presentation and engineering-design directories keep their
existing locations. Current `actlumen-brand-and-scope.md` and
`actlumen-reviewer-brief.md` are now named `evialign-brand-and-scope.md` and
`evialign-reviewer-brief.md` under `product/`.

Relative navigation links and the AGENTS verification-reference path follow the
new locations. Historical filenames, literal command transcripts, source
anchors, hashes, dates and frozen results retain their original meanings.
In particular, the Pi readiness ADR and Phase-0 preflight, together with their
linked contract/review records, stay adjacent in `contracts/` so their bound
source bytes and line references remain intact. The contract directory includes
these historical readiness records; it does not imply implemented execution.
Existing specification follow-up links and release navigation were rebased;
original design decisions and historical release statements were not rewritten.

For old paths quoted by earlier records or companion repositories, see the
[complete pre-layout documentation tree](https://github.com/alexzhu0/EviAlign/tree/9cc423817b484221aabf99227283a6df536f3997/docs).
The [current index](README.md) gives their maintained locations. This move does
not create automatic redirects for old GitHub `main` URLs. Independent runtime
repositories and Windows deliverables are outside this pass. Source, tests,
fixtures, schemas, policy/data assets, CI, package and command paths are unchanged.

Verification on the isolated documentation worktree based on `9cc4238` passed
all six repository checks: policy validation, 3/3 smoke evaluations, both loop
fixtures, 538 tests in 37.856 seconds and whitespace checks. The documentation
check covered 88 Markdown files, local paths and anchors, fixed-revision Git
targets and bilingual directory/command parity. All existing code blocks and
non-document assets match the baseline. Current reviewer-material source
citations were converted from old literal paths to links at their new locations.
The initial baseline attempt under the default sandbox had two temporary-directory
write errors; enabling workspace writes resolved both without changing tests.

Independent read-only review found no Critical, Important or Minor issue. It
checked the directory mapping, bilingual navigation, local/immutable targets,
current source citations and the 21 ADR source lines/digests. It did not repeat
the test suite, inspect external runtimes or Windows files, or verify GitHub
online availability; fixed Git targets were checked against local objects.

## Cleanup on 2026-11-05

The initial pass covered the main repository; the separately authorized Windows
pass is recorded below. The business sandbox, unrelated runtime worktrees,
credentials and local editor settings were not deleted. Runtime code, schemas,
policies, tests, fixtures, release records, engineering designs and retained
evaluation evidence remain in place.

- Remove 17 superseded competition-production files: nine material-production
  plans, five presentation/branding designs, the old eight-page HTML, its cover
  prompt and the original film delivery note. Some historical checklists still
  had unchecked steps; their later deliverables supersede those plans. Their
  original states remain available in the fixed revision below.
- Consolidate presentation history into one current delivery index. It retains
  final artifact digests, actual recording provenance, native acceptance and
  immutable links to the full earlier history.
- Update bilingual README/navigation to the current 20-page formal edition and
  current maintenance entry; retain reusable bilingual project descriptions.
- Remove 29 generated cache files (1,241,026 bytes): Python bytecode and the
  analysis graph generated on 2026-08-14. Its local ignore configuration remains.
  Temporary recovery copies were kept during this cleanup.
- Ignore local Cursor settings, Superpowers scratch state and generated CI
  report artifacts to keep them out of future commits.

The removed tracked files total 141,036 bytes. The full historical presentation
record is also condensed; no Git history is rewritten.

## Windows materials cleanup

The user additionally authorized: “也整理 Windows 历版材料，保留最终版和制作源文件”.
`D:\Sayitout\小强创新` now has five project directories and a directory guide:

| Entry | Retained content |
| --- | --- |
| `EviAlign-正式答辩版-20261104` | Final 20-page PPTX/PDF, original movie, overview, notes and presentation ZIP; latest reviewer DOCX/PDF and bilingual description copied here. |
| `制作源文件` | Six distinct existing source ZIPs, including the unique pre-publication source backup; historical code/text archive and the preserved `EviAlign1030.pptx` edit. |
| `提交留档` | The original prepared submission ZIP, unchanged. |
| `EviAlign-实时联调` | Live launcher, normalized actual records and screenshots, unchanged. |
| `EviAlign-行动复核台` | Offline-review launcher and demonstration records, unchanged. |
| `EviAlign-目录说明.txt` | Current local navigation and playback instructions. |

Nine entries were moved, three latest documents copied, 161 obsolete files
removed (82,217,948 bytes), and six empty directories removed. No file was
skipped. Moves/copies preserve their original bytes; 22 existing final/demo files
were checked before and after, and all retained ZIPs passed CRC checks. The
current 20-page edited submission PPT was also verified against the baseline
inside the formal-edition source ZIP before its unpacked duplicate was removed.

Independent review found that two original narration inputs were not in the
existing source ZIPs. The correction permanently archived all 38 historical
script/JSON/HTML/Markdown/text sources, including `voice.ps1` and `voice.json`,
to `制作源文件\历史版本\EviAlign-历史制作脚本与文本源文件.zip` before deleting
their old paths. Every archived member was checked against its original digest
again after cleanup. This archive's SHA-256 is
`971f32539505a1ec08d2c0e108c970110682a1e3daa59a021d25178dda0ccd7a`.

A verified task-local recovery ZIP was created before deletion. A durable
operation receipt is in `制作源文件\整理记录-20261105.json`. The reviewer did
not perform the Windows operations; the implementer verified the corrected
source archive, moves, final files and absence of planned obsolete paths. No
Office document was closed and no model, runtime or presentation was rerun.

## Archived production materials

Pre-cleanup revision:
[`306b85ff30bdf479875f1d546283884456f2b026`](https://github.com/alexzhu0/EviAlign/tree/306b85ff30bdf479875f1d546283884456f2b026).
Historical design approvals and original evidence descriptions can be read at
that exact revision:

- [Material plans](https://github.com/alexzhu0/EviAlign/tree/306b85ff30bdf479875f1d546283884456f2b026/docs/superpowers/plans)
- [Design records](https://github.com/alexzhu0/EviAlign/tree/306b85ff30bdf479875f1d546283884456f2b026/docs/superpowers/specs)
- [Full presentation-production history](https://github.com/alexzhu0/EviAlign/blob/306b85ff30bdf479875f1d546283884456f2b026/docs/presentations/evialign-ppt-expanded-delivery.md)
- [Original mock-film provenance](https://github.com/alexzhu0/EviAlign/blob/306b85ff30bdf479875f1d546283884456f2b026/docs/presentations/evialign-ppt-poc-delivery.md)

Retrieve any historical file without changing the working tree:

```bash
git show 306b85ff30bdf479875f1d546283884456f2b026:docs/superpowers/plans/2026-11-04-formal-presentation-polish.md
```

## Verification

On `306b85f` plus this documentation/ignore cleanup, all six AGENTS.md commands
passed: policy validation, 3/3 smoke evals, both loop fixtures, 538 unit tests in
38.975 seconds and `git diff --check`. All checked local links in 110 Markdown
files resolve; fixed-revision targets were verified against Git objects, and
bilingual README command blocks remain identical. The 17-file deletion set
matches the reviewed manifest; implementation, contract, fixture, CI and release
trees have no diff from the baseline.

Independent read-only review found no Critical, Important or Minor issue. It
checked the deletion manifest against Git objects, current documents, local
targets/anchors and retained provenance; it did not independently run the test
suite, Windows presentation, external sandbox or historical paid requests.
No new paid/live call, PowerPoint rendering, runtime authorization or release
is part of this cleanup.

## Engineering history

A further repository-only pass removed 23 historical documents: 15 old
implementation checklists and eight superseded workflow, phase-packaging,
fake-read, brand-history or compatibility notes. The asset map and engineering
guide now describe current assets/commands rather than repeat the T0xx
chronology. Original content remains at the
[pre-pruning revision](https://github.com/alexzhu0/EviAlign/tree/0fefab9c521fc4de876e1eba718b751de2e2c30b/docs),
including the [old implementation plans](https://github.com/alexzhu0/EviAlign/tree/0fefab9c521fc4de876e1eba718b751de2e2c30b/docs/superpowers/plans).
Archiving an old checklist does not assert that all its steps were completed.

The 12 retained [design specifications](superpowers/README.md) and eight key
Pi contract/readiness/verification documents were protected byte-for-byte.
In particular, the runtime-readiness ADR and Phase-0 preflight remain available
with their existing source bindings and **NO-GO / NOT IMPLEMENTED** decision.
Source, tests, schemas, policies, fixtures and CI are unchanged.

The user separately deleted the ignored root `.superpowers/` scratch directory.
It contained no tracked files; installed skills and `docs/superpowers/specs/`
remain present. This loses local historical task state, not committed code or
designs. The installed workspace helper recreates scratch directories when
needed. Current housekeeping uses Git and temporary receipts rather than an
old ledger; no progress state was fabricated or marked complete.

This pass passed all six repository checks, including 538 tests in 37.484
seconds with root scratch state absent. The link check covered 88 Markdown
files, 402 local targets and 18 fixed-revision targets without a missing target.
The 23-file deletion manifest and all 20 protected document digests match.
Independent read-only review found no Critical, Important or Minor issue. It
verified the deletion scope, preserved documents, command semantics, fixed Git
targets and scratch-directory explanation. It did not independently rerun the
test suite, query GitHub, recover deleted local state or inspect external
runtimes/paid evaluations.
