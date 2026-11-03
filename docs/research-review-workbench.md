# EviAlign research-review workbench / 行动复核台

Updated: 2026-11-03. Local engineering PoC in the **separate**
`agentharness-business-sandbox` repository. Cloning this main repository alone
does not install the sandbox or this UI. This is not a new `agentharness` CLI command.

## Run locally

Use Python 3.10+ and the standard library. With the sandbox and main repository
in sibling directories (`agentharness-business-sandbox/` and `AgentHarness/`):

```bash
cd ../agentharness-business-sandbox
./run-sandbox review --port 8769
```

Open `http://127.0.0.1:8769`. If the main checkout has another name or location,
set `AGENTHARNESS_SOURCE` to its root before launching. No environment file or
provider key is needed. The server listens only on loopback.

## Demonstrate the complete flow

1. Choose one retained synthetic case and a self-declared reviewer alias.
2. Read the original user request, prior turns and unmodified proposed action.
3. Save an independent initial judgment and reason, then reveal the historical
   Jev choice, confidence, triage and pinned model. No new scoring takes place.
4. Record a final research judgment and reason. An optional revised proposal is
   retained as a separate, unassessed draft; it cannot inherit the old score.
5. Leave business outcome as unavailable, or add an explicitly simulated note.
   These source cases contain no observed business outcomes.
6. Save and download JSON containing completed reviews, original cases, historical
   observations, both judgments, reasons, drafts and outcome provenance.

The six cases are E120, E122, E167, E173, E176 and E099, drawn from previously
seen development/selection inputs and their retained v2 rescore reports.
Exact file digests and request/proposal/rubric binding checks protect the replay
correspondence. They are not signatures or source authentication. No holdout was
rescored and no original report or model/rubric/threshold was changed.

## What has been demonstrated

Automated engineering checks exercised all six cases, real browser downloads,
refresh/resume, browser-session isolation, separate drafts, inert HTML-like text,
desktop and mobile layouts, and prohibited business routes. No business colleagues
have trialed it, so the demo annotations are not human-study evidence. The prototype
does not measure review quality, time savings, classification accuracy or ROI.

Records live in server memory: at most 64 reviews per browser session and 128
browser sessions per service. Refresh restores saved stages; service restart,
loss of the browser session cookie or changing hostname does not restore access.
Download before restarting. An unfinished review cannot be silently overwritten.
Exports identify any unfinished count and include completed records only.

Review mode does not create the business runtime or expose execution/control APIs.
No credentials, planner, provider calls or simulated/real business actions are used.
Research labels are not authenticated approvals; all outputs retain
`result_status: not_executed`. Existing enterprise systems remain responsible for
identity, permissions, approval validity and execution. The ordinary sandbox's
optional live Jev mode remains a distinct feature.

## 中文演示说明

这是已经可以操作的“研究复核记录”原型。它将原始案例、人的初审、Jev 历史
观察、复核及理由放在同一条可导出的记录里，演示如何为人机分工研究积累依据。
页面采用现有沙箱样式，不依赖新增前端框架或数据库。

启动后选案例，先独立初审，再看 Jev，最后记录复核意见和可选修改草案。
原始请求与评分保持原样；修改草案单独存放、没有评分、不会执行。
结果来源只能是“未获得”或“模拟说明”，没有把业务成功写成已发生。

记录保存在服务内存中，同浏览器刷新可以继续已保存的阶段。重启服务会清空；
Cookie 丢失或换主机名也不能恢复原会话。请及时下载 JSON。
每浏览器最多 64 条记录、每服务 128 个会话；未完成当前案例时不能直接覆盖。

本轮已经完成工程与浏览器验收；尚未安排业务同事试审，不提供真实审批、
数字签名或业务结果接入，也不主张节省工时、ROI 或自动放权效果。
Jev 为历史观察回放，0 次新模型请求，继续保留 `not_executed`。

## Maintainer verification

On 2026-11-03, the corrected sandbox passed 124 unit/HTTP tests, its 60/60
deterministic suite and both 60/60 comparison arms, with zero model calls.
The main repository passed all 538 tests, policy validation, 3/3 smoke
evaluations, both required loop checks and whitespace checks. A separate
read-only reviewer identified one intermediate-directory symlink omission;
its regression failed before the fix, then passed with the complete suite.
No other Critical, Important or Minor findings remained from that review.
Browser automation completed all six paths and actual JSON downloads at
1440×1000 and 390×844. These results are session-captured engineering evidence.

From the separate sandbox root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
./run-sandbox test
./run-sandbox compare
git diff --check
```

Source, tests and the detailed sandbox runbook remain separate from this main
repository. Keep commits and release units separate; this delivery creates no
sandbox remote, tag, public app or production execution integration.

Local sandbox source checkpoint: `aad752b8afd2ad019bd891937956bfbd886e4b7a`
on `jev-intent-eval`; main-repository documentation is committed separately.
