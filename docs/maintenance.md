# Project maintenance

Updated: 2026-11-05. Current maintenance entry for EviAlign. The user reports
that hackathon registration has closed and the earlier materials were uploaded.
This does not independently verify a competition submission or submit a new one.

## Current sources

- [Purpose and progress](project-purpose-and-progress.md) · [中文版](project-purpose-and-progress.zh-CN.md)
- [Research-review workbench and actual live acceptance](research-review-workbench.md)
- [Retained Jev evaluation](33-jev-shadow-maintenance-handoff.md)
- [Final presentation files and provenance](presentations/evialign-ppt-expanded-delivery.md)
- [Engineering guide](engineering-guide.md) · [Repository rules](../AGENTS.md)

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
