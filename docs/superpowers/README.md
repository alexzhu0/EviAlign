# Engineering designs

Design specifications remain in `specs/`. They record scoped decisions, not
permission to activate a runtime or repeat a model evaluation. Current behavior
and evidence are described in the [engineering guide](../engineering-guide.md)
and [project status](../project-purpose-and-progress.md).

| Area | Design references |
| --- | --- |
| Development workflow | [Superpowers migration](specs/2026-08-13-omx-to-superpowers-migration-design.md) |
| Local verification | [Declarative evaluator](specs/2026-08-14-declarative-eval-engine-design.md), [CI](specs/2026-08-17-github-actions-ci-design.md) |
| External DeepSeek shadow | [Integration](specs/2026-08-19-deepseek-harness-shadow-design.md), [locked launch](specs/2026-08-20-deepseek-shadow-locked-launch-design.md), [diagnostics](specs/2026-08-31-deepseek-shadow-controlled-diagnostics-design.md), [live driver](specs/2026-08-31-deepseek-shadow-live-driver-design.md) |
| Independent synthetic runtime | [Data-access lab](specs/2026-09-14-data-access-lab-design.md), [business sandbox](specs/2026-09-15-business-sandbox-design.md) |
| Jev observation | [Shadow observer](specs/2026-10-14-jev-sandbox-shadow-design.md), [corpus](specs/2026-10-14-jev-intent-eval-corpus-design.md), [rubric v2](specs/2026-10-19-jev-rubric-unclear-design.md) |

The 15 historical implementation checklists are available at the
[pre-cleanup revision](https://github.com/alexzhu0/EviAlign/tree/0fefab9c521fc4de876e1eba718b751de2e2c30b/docs/superpowers/plans).
This archive does not mean every old checklist item was completed or authorize
its execution again. New implementation work needs a current plan under the
[repository workflow](../../AGENTS.md).
Implementation-plan paths quoted inside historical specifications refer to
that archive rather than a current pending task.

The root `.superpowers/` directory is ignored, temporary per-plan work state.
It is separate from these tracked specifications and from the installed skills.
It can be recreated by the skill's workspace helper; deleting it may lose local
progress/review drafts but does not delete committed code or design documents.
Recreating the directory does not recover deleted ledgers or review drafts.
