# EviAlign PowerPoint and PoC film delivery — 2026-10-29

The user approved the [design](../superpowers/specs/2026-10-29-evialign-ppt-poc-film-design.md) and requested editable PowerPoint with an embedded mock-data demonstration. The local Windows destination is now `D:\Sayitout\小强创新`, where the earlier files were found after the former `小强` directory ceased to exist.

## Delivered files

- `EviAlign-黑客松汇报.pptx`: eight slides, 129 native text shapes, editable diagrams, speaker notes and clickable industry references. Contains the entire standalone movie as embedded media.
- `EviAlign-PoC演示.mp4`: 84.709 seconds, 1280×720, 24 fps, H.264 video and AAC audio. Mandarin narration uses local Microsoft Huihui Desktop; background sound and animation use huashu-motion 0.3.1 at source commit `52467f99c602b76ba86d511d37acdfe93fa1e16e`.

PPTX SHA-256: `53621469e8c1804a1704ebcb4c08516b3780a808c39cffdfe6fc28e3ea9d21c7`.

MP4 SHA-256: `08e27db4761198c998166e99b21626018b4ba0bc4c181c2e844bd207263d3c0b`.

Previous HTML, PDF and Word files were preserved; the two new filenames did not exist before delivery. Temporary production sources and voice/render checks are retained in `/tmp/evialign-ppt-film` and the destination's `.evialign-production` folder. They are not runtime dependencies.

## Material provenance and interpretation

- The delivery-exception background is fictional. It frames future cross-department collaboration rather than claiming a Lenovo deployment.
- The screen material is a real screenshot of an actual offline, read-only synthetic `list_shipments` result: one business read, zero business writes, no transaction commit. It is a result capture, not a continuous recording of an autonomous agent. Model planning and Jev were disabled for this capture.
- An independent mock request exercised the actual `build_evidence` and `verify_business_action_evidence_v1` functions. The original request and retained unsigned receipt returned `business_action.ok`; changing the recipient while keeping that receipt returned `business_action.binding_invalid`. Both reports retained `not_executed`. This is correlation, not authentication, business-semantic approval or execution permission.
- E173 replays the unchanged existing development-case observation from the separate sandbox's `evals/jev-intent-v1/cases-dev.json` and `reports/jev-intent-v1-r2-dev.json`. The original user said to await confirmation before transferring `t_orbit_046`; the proposal named `orbit_support2`. The retained 2026-10-20 result was `unclear / human_review`. The observation does not block, authorize or execute.
- These are independent demonstrations. They are not stitched together as a real integrated approval transaction. Task preparation, complete business review records, outcome collection and adjustment of authority remain future research and are labeled accordingly.

No credentials were read or shown; no paid model request, new model evaluation, sandbox business write or external-system execution was made.

## Verification and remaining limitations

The AGENTS.md policy validation, three smoke evaluations, both loop checks, 538 unit tests and whitespace check passed. huashu-motion sampled 24 frames with zero layout/script errors or warnings. An independent reviewer verified all three industry sources, independently reproduced the evidence-check results, checked E173 against the retained record, checked slide editability and media hashes, and inspected PowerPoint-rendered slide images. The material finding about task-preparation labeling was corrected in the final film and visually verified.

Windows PowerPoint opened the final PPTX, exported all eight slides and a preview PDF, and played the embedded movie. Its native Player.State returned `0` (Playing). A final cleanup accounted for the hidden presentation already being closed by the slideshow, without closing unrelated user documents. Delivered-file hashes and the embedded-versus-standalone movie hash match.

Reading holds remain intentional for the narrated explanation; this is a PoC explainer rather than a rapid-cut advertising reel. The movie includes the small huashu-motion production signature. Minor review notes: the synthetic-workbench heading could say “query result” more explicitly, and slide 7's 11–12 pt caveats / the reduced movie footnotes are small for projection. The provenance above clarifies the capture; the standalone MP4 supports larger playback. The audio track was generated and structurally checked but not independently listened to by the reviewer. Production deployment, complete approval semantics and ROI remain unverified.
