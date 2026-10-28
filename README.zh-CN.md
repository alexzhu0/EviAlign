# EviAlign

[English](README.md) | **简体中文**

**面向 AI 行动请求的执行前依据核对原型**

EviAlign 在受信请求和保留原有证据的前提下，核对当前结构化请求与其证据是否对应，并生成可复查的检查记录。独立本地业务沙箱中另有可选的意图观察。

**EviAlign** 取 Evidence（依据）与 Align（对齐）的含义，强调让一次行动请求与其依据有清楚的联系。身份、授权、审批和实际执行继续由企业现有系统负责。

[项目评审材料](docs/actlumen-reviewer-brief.md) · [八页管理层汇报](docs/presentations/agentharness-enterprise-hackathon.html) · [文档导航](docs/README.md) · [工程参考](docs/engineering-guide.md)

## 企业需要回答的问题

当企业考虑让更多 AI 智能体参与业务处理，一个具体问题是：拟提交的动作与本次保留的依据是否仍然对应。现有 API、细粒度授权和审批系统可能已覆盖所需控制；引入额外组件的理由，需要真实缺口或减少重复接入、核对成本的实证。

## 一个拟议示例

假设原有流程确认**订单 A 退款 100 元**，拟议对照可呈现 AI 准备提交的对象和金额是否发生变化。此示例为合成材料：真实审批字段与行动字段的业务对照尚未实现，不执行实际退款。

| 职责 | 当前状态 |
| --- | --- |
| 身份、授权、审批有效性与实际执行 | 继续由现有外部系统负责。 |
| 结构化请求与证据的对应 | 本仓库已有原型，依赖受信输入与保留原有证据。 |
| 原始意图与 AI 计划 | 独立本地业务沙箱提供可选观察；提示不构成执行授权。 |
| 真实审批记录与拟提交业务字段 | 需要单独设计、可信接入与验证。 |

当前业务证据契约会绑定所提供的审批字段，但不解释字段含义。请求改变后，旧证据不会与新请求匹配；摘要一致也不能证明来源身份、审批有效、业务正确或允许执行。[业务证据契约](docs/business-action-evidence-v1.md)

## 已有证据

2026-10-21，独立沙箱对 84 个合成意图观察案例进行单次评测：36 个越界案例均被标记，24 个意图不清案例均收到复核提示，24 个正常案例中有 3 个也收到复核提示。

案例由 AI 编写并由另一 AI 独立盲标，覆盖 33 个相关场景族，非人工真值、非联想业务数据。这些结果不能证明生产准确率、真实审批与行动对照能力、节省工时或 ROI。[完整评测记录](docs/33-jev-shadow-maintenance-handoff.md)

## 怎样判断价值

选择一个获批的业务流程，以只读回放比较三种做法：现有机制、合理补强现有机制，以及拟议接入 EviAlign。记录差异发现情况、整体处理时间、新增复核负担、接入维护成本与跨智能体复用投入。若现有能力已满足需要，或新增成本超过可证明的收益，就继续复用现有方案。

## 按角色阅读

| 读者 | 建议入口 |
| --- | --- |
| 领导与黑客松评审 | [项目评审材料](docs/actlumen-reviewer-brief.md)、[八页离线汇报](docs/presentations/agentharness-enterprise-hackathon.html) |
| 业务试点负责人 | [品牌与能力范围](docs/actlumen-brand-and-scope.md)、评审材料中的拟议对照与试点 |
| 开发与平台团队 | [完整工程参考](docs/engineering-guide.md)、[资产地图](docs/00-asset-map.md) |
| 安全与证据评审 | [产品契约](docs/08-glossary-and-product-contract.md)、[可复现演示](docs/11-reproducible-enterprise-demo.md)、[检查清单](docs/13-external-reviewer-checklist.md) |
| 后续维护者 | [维护记录](docs/34-actlumen-brand-maintenance.md)、[仓库工作规则](AGENTS.md) |

下载单文件汇报后可在浏览器离线展示、翻页、切换示例和打印；来源链接按仓库访问权限查阅。

## 开发者快速开始

在仓库根目录执行，使用 Python 3.10 或以上版本：

```bash
python3 -m pip install -e .
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
```

完整命令、证据契约与外部运行时职责见[工程参考](docs/engineering-guide.md)。

## 持续集成

<details>
<summary>开发者验证说明与完整命令</summary>

[![CI](https://github.com/alexzhu0/EviAlign/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alexzhu0/EviAlign/actions/workflows/ci.yml)

CI 在拉取请求和推送至 `main` 时运行，覆盖 Python 3.10、Python 3.11 与 Python 3.12。在本地复现完整验证流程：

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

仅在验证失败且两份报告均已生成时保留报告文件，保存 14 天。若任一报告缺失，CI 会在上传前因缺少证据而失败。

CI 不授予运行时授权，也不执行 Agent Runtime 工具。

</details>

## 品牌与兼容

EviAlign 是当前项目名称；AgentHarness 和 ActLumen · 明行是历史名称。现有 `agentharness` 命令、Python 包名、协议与文件路径保留兼容，历史记录保留发生时的名称。当前源码预发布版本仍为 `v0.2.0-alpha.1`，本次更新不构成新版本或包发布。

`allow_candidate` 仅表示候选证据，当前证据与观察输出保留 `result_status: not_executed`。本仓库不提供身份认证、可信签字、运行时授权、审批语义、事务或工具执行。[完整范围说明](docs/actlumen-brand-and-scope.md)

MIT License · [许可证](LICENSE)
