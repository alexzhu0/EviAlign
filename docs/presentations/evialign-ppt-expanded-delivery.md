# EviAlign presentation materials

Updated: 2026-11-05. The user reports that the earlier materials were uploaded
and hackathon registration has closed. The formal edition below was delivered
separately; no assistant-operated competition submission is claimed.

## Current formal edition

Delivered on 2026-11-04 to
`D:\Sayitout\小强创新\EviAlign-正式答辩版-20261104`:

- `EviAlign-黑客松汇报-正式答辩版.pptx` and matching `.pdf`: 20 pages,
  comprising 17 main pages and three appendices, 332 nonempty native text
  shapes, editable diagrams and one native editable chart. Original notes and
  original page copy are retained in the notes.
- `EviAlign-Live-Demo.mp4`: the actual 22.64-second silent H.264 browser
  recording, also embedded on page 13 with a central play poster.
- `EviAlign-20页总览.png`, `EviAlign-正式答辩版讲稿.md` and
  `EviAlign-正式版说明.txt`: all-page preview, speaking notes and instructions.

The presentation files above are packaged in
`D:\Sayitout\小强创新\EviAlign-正式答辩版-20261104\EviAlign-正式答辩版-20261104.zip`.
Maintainable production source is in the separate
`D:\Sayitout\小强创新\制作源文件\EviAlign-正式答辩版制作源文件.zip`.
PPTX/MP4 binaries are local deliverables, not repository runtime assets.

These digests identify the files checked on 2026-11-04:

| Artifact | SHA-256 |
| --- | --- |
| Formal-edition ZIP | `2378e47372d29e66691c35ad2d77196463338f9c7397881f91a560900f64c821` |
| Source ZIP | `4d489d23fe6189ca7e6b21ab7778438f134a59eb0171f1276eb888c5dbba1847` |
| Native-saved PPTX | `2113f1a81d247811eb07216d19ae93ac38313b2243dff1ae06540dec1e5b5c09` |
| Native PDF | `50f0eaf711253ae396edec9b7820d3b0a39a54d7915d2d1f28b610057d363ed9` |
| Actual movie | `7e46c57e67340006013dd79998378e2f243b8549bf6245bfd2741927e5261555` |

The original prepared submission ZIP is now retained unchanged at
`D:\Sayitout\小强创新\提交留档\EviAlign-参赛提交包-20261104.zip`.
On 2026-11-05, the latest bilingual description and reviewer DOCX/PDF were copied
into the formal-edition directory before the old unpacked submission directory
was removed. All package/artifact digests recorded here remain those of the checked
2026-11-04 files; relocation did not regenerate their content.
The current reusable sources are the [bilingual description](../product/hackathon-entry.md)
and [reviewer brief](../product/evialign-reviewer-brief.md).

## Evidence and provenance

The supply-chain process is a fictional research illustration. Historical E173
covers a pending-confirmation ticket transfer, not that complete process. The
actual new video demonstrates E120. The
[2026-11-04 live acceptance](../guides/research-review-workbench.md#live-acceptance-on-2026-11-04)
records three DeepSeek and three OpenRouter/Jev requests, all with valid
responses:

| Case | Actual proposal | Jev observation |
| --- | --- | --- |
| E120 | `create_ticket` | `fits / .88 / no_flag` |
| E122 | `assign_ticket` | `fits / .79 / human_review` |
| E173 | `list_tickets` | `unclear / .46 / human_review` |

The live E173 is a query, not a blocked unauthorized transfer. These are seen
synthetic tasks with automated demonstration annotations, not business-colleague
reviews or an accuracy study. The
[historical 84-case evaluation](../research/33-jev-shadow-maintenance-handoff.md) is
separate: AI-authored cases and independent AI blind labels, not human ground
truth or Lenovo business data. Neither source demonstrates enterprise ROI,
approval validity or business execution. Outputs retain `not_executed`.

## Retained presentation verification

The following checks were performed on 2026-11-04, not rerun by the later
repository cleanup:

- Native PowerPoint opened all 20 pages, exported every preview/PDF page and
  measured zero text-frame overflow candidates. PDF checks retained three
  project links, one TypeSafe link and three industry links, with no out-of-page
  text. Embedded movie bytes match the standalone MP4; ZIP checks passed.
- Native first-click playback stayed on page 13, player state 0 (Playing),
  position 3914 ms, Media Play effect 83 and trigger 1. This used the native
  click-sequence interface in the task's own slideshow, not a physical-mouse
  or venue-projection test.
- Independent review inspected all pages and confirmed a substantive visual
  improvement with no Critical or Important issue. The author corrected its
  chart-caption Minor and checked the final PDF and native bounds. The reviewer
  did not independently run Windows playback.
- All six repository checks passed, including 538 tests in 37.726 seconds.

Design guidance came from the public
[Anthropic pptx skill](https://github.com/anthropics/skills/tree/main/skills/pptx),
[huashu-design](https://github.com/alchaincyf/huashu-design) and comparison of
[huashu-slide-codex](https://github.com/alchaincyf/huashu-slide-codex).
This edition's production engine was project-local `python-pptx` plus native
PowerPoint. It does not claim execution of the vendor validators or the huashu
HTML exporter/lint for this edition. No global skill was installed.

## Earlier production history

The [full pre-cleanup delivery record](https://github.com/alexzhu0/EviAlign/blob/306b85ff30bdf479875f1d546283884456f2b026/docs/presentations/evialign-ppt-expanded-delivery.md)
retains the preceding Jev/reviewer/expanded editions, all historical artifact
digests and design approvals. The
[original mock-film record](https://github.com/alexzhu0/EviAlign/blob/306b85ff30bdf479875f1d546283884456f2b026/docs/presentations/evialign-ppt-poc-delivery.md)
is preserved at the same immutable revision. These are historical records, not
new verification or current runtime authorization.

Current repository cleanup and its checks are recorded in
[project maintenance](../maintenance.md).
