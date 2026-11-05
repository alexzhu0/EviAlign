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

Scope: the main repository. Windows deliverables, the separate business sandbox,
unrelated runtime worktrees, credentials and local editor settings were not
deleted. Runtime code, schemas, policies, tests, fixtures, release records,
engineering designs and retained evaluation evidence remain in place.

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
