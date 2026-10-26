# ActLumen · 明行

**企业 AI 行动质检助手**

让 AI 行动清晰，让业务协作高效。

ActLumen 帮助企业在 AI 进入业务处理前，看清三件事：**本次要完成什么、AI 准备做什么、行动依据是否对应**。项目提供执行前的依据核对与可复查记录，并配合独立业务沙箱中的意图偏差提示，支持业务人员判断。

Act 表示行动，Lumen 借“光”的意象表达清晰与可理解。“明行”希望让 AI 的行动看得清，让团队的协作有据可循。

[项目评审材料](docs/actlumen-reviewer-brief.md) · [八页管理层汇报](docs/presentations/agentharness-enterprise-hackathon.html) · [文档导航](docs/README.md) · [工程参考](docs/engineering-guide.md)

## 企业为什么需要明行

当 AI 开始协助处理订单、客户和费用，员工仍需要确认建议是否符合需求、材料是否对应、哪些地方需要关注。

- **减少重复确认：**避免为了核对一份建议，反复回看长对话、翻找材料。
- **提前呈现偏差：**帮助关注“只让查询，却准备审批”等偏离原意的计划。
- **让复盘有线索：**保留与本次行动对应的检查记录，帮助团队说明经过、积累经验。

这些是项目的价值方向。能否节省处理时间、减少返工，需要在真实业务试点中测量。

## 从哪些业务场景开始

| 场景 | 拟议任务 | 关注重点 | 预期帮助 |
| --- | --- | --- | --- |
| 客户服务 | 查询退款进度并准备回复。 | 查询不变成审批。 | 少翻找记录，把精力留给客户沟通。 |
| 销售运营 | 整理订单交付进度与待跟进事项。 | 查进度不变成改交期。 | 减少来回确认和补充解释。 |
| 财务协同 | 汇总退款与对应订单，标出待核对项。 | 核对不变成付款。 | 集中处理需要业务判断的事项。 |

上述场景为应用方案，尚未接入联想真实业务系统。面向员工的集中核对界面属于下一步产品化工作。

## 明行怎样参与流程

```text
员工说明需求 → AI 拟出计划 → 明行提供依据核对与意图提示 → 企业按既有规则处理
```

依据核对检查材料是否对应当前行动；意图观察提示计划是否可能偏离原需求。两者为人工判断提供支持。是否批准、是否执行，继续由企业现有流程和外部系统负责。

## 已有成果与下一步

| 当前基础 | 接下来验证 |
| --- | --- |
| 本仓库已实现执行前行动依据核对、确定性检查与可复查记录。 | 建设业务核对界面，选择一个获批的只读流程开展试点。 |
| 独立本地业务沙箱已实现可选的 Jev 意图观察。 | 对照任务结果、整体处理时间、额外复核负担与维护投入。 |
| 留存了固定输入的合成案例评测。 | 由真实业务对照结果决定是否值得推广。 |

2026-10-21 的 **84 个合成案例**中：36 个越界案例全部被标记；24 个意图不清案例全部收到复核建议；24 个正常案例中仍有 3 个被建议复核。

案例由 AI 编写并由另一 AI 独立盲标，非人工真值、非联想业务数据，覆盖 33 个相关场景族。零观察漏检不证明生产准确率；正常请求带来的复核负担也需要纳入评估。[完整评测记录](docs/33-jev-shadow-maintenance-handoff.md)

当前尚未实测联想业务中的节省工时、成本或 ROI。建议以“结果正确、整体处理更快、额外复核负担可接受”作为试点判断框架。

## 按角色阅读

| 读者 | 建议入口 |
| --- | --- |
| 领导与黑客松评审 | [四页项目评审材料源文](docs/actlumen-reviewer-brief.md)、[八页离线汇报](docs/presentations/agentharness-enterprise-hackathon.html) |
| 业务试点负责人 | [品牌与能力范围](docs/actlumen-brand-and-scope.md)、评审材料中的场景、收益与试点方案 |
| 开发与平台团队 | [完整工程参考](docs/engineering-guide.md)、[资产地图](docs/00-asset-map.md) |
| 安全与证据评审 | [产品契约](docs/08-glossary-and-product-contract.md)、[可复现工程演示](docs/11-reproducible-enterprise-demo.md)、[检查清单](docs/13-external-reviewer-checklist.md) |
| 后续维护者 | [维护记录](docs/34-actlumen-brand-maintenance.md)、[仓库工作规则](AGENTS.md) |

GitHub 源码页显示 HTML 源文；下载单文件汇报后可在浏览器离线展示、翻页、切换场景和打印。材料中的来源链接按仓库访问权限查阅。

## 开发者快速开始

在仓库根目录执行，使用 Python 3.10 或以上版本：

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

安装要求、完整命令、CI、证据契约、外部运行时边界和历史里程碑见[工程参考](docs/engineering-guide.md)。

## Continuous Integration

<details>
<summary>开发者验证说明与完整命令</summary>

[![CI](https://github.com/alexzhu0/ActLumen/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alexzhu0/ActLumen/actions/workflows/ci.yml)

The CI workflow runs on pull requests and pushes to `main`, using a Python 3.10,
Python 3.11, and Python 3.12 matrix. Reproduce its local verification sequence
with:

```bash
python -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
mkdir -p artifacts
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --all --format junit > artifacts/eval-results.xml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --all --format json > artifacts/eval-results.json
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -q
git fetch origin main
git diff --check origin/main...HEAD
```

Failure-only 14-day report artifacts are retained when both reports were
generated. If either report is missing, CI fails a missing-evidence check before
upload.

CI is not runtime authorization and does not execute Agent Runtime tools.

</details>

## 品牌与兼容

ActLumen · 明行是原 AgentHarness 的新项目品牌。现有 `agentharness` 命令、Python 包名、协议与文件路径保留兼容；历史发布和交接记录保留当时的名称。当前源码预发布版本仍为 `v0.2.0-alpha.1`，本次品牌更新不构成新版本或包发布。

本仓库是执行前证据控制平面。`allow_candidate` 仅表示候选证据，当前证据与观察输出保留 `result_status: not_executed`。身份、授权、审批语义、事务和实际执行由外部系统负责。[完整范围说明](docs/actlumen-brand-and-scope.md)

MIT License · [许可证](LICENSE)
