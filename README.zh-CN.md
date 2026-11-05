# EviAlign

[English](README.md) | **简体中文**

**让每次行动有依据，让每一步放权有根据。**

EviAlign 是一项前沿研究：探索企业如何审核 AI 拟采取的业务行动，以及如何通过积累判断和结果，研究哪些环节需要人、哪些环节可以减少人工介入。当前基础是执行前依据核对原型，完整业务审核与经验积累闭环仍待建设。

**EviAlign** 取 Evidence（依据）与 Align（对齐）的含义，强调让一次行动请求与其依据有清楚的联系。身份、授权、审批和实际执行继续由企业现有系统负责。

[项目目的与当前进展](docs/project-purpose-and-progress.zh-CN.md) · [项目评审材料](docs/actlumen-reviewer-brief.md) · [最新版 PPT 交付记录](docs/presentations/evialign-ppt-expanded-delivery.md) · [文档导航](docs/README.md) · [工程参考](docs/engineering-guide.md)

## 为什么做这个项目

企业已经构建了很多智能体，其中不少仍以问答、查询和辅助分析为主。未来，AI 可能更多参与流程重构、提出业务决定，甚至推动事情真正发生。我们希望提前研究这些行动的审核依据和责任边界。

业务愿景是“让 AI 做事前经过签字与审核”：看清它准备做什么、依据是什么、哪里需要人的确认。未来的业务接入可将 AI 提议、人工确认或修改，以及最终结果关联起来，研究哪些特定情形需要人的判断，哪些情形有条件减少人工介入。

这套积累与调整过程是研究目标。历史上经常获批不等于安全，需要验证结果、例外和变化条件；减少人工介入仍须由企业限定范围、评估并批准。[完整目的与研究路径](docs/project-purpose-and-progress.zh-CN.md)

## 现在做到了哪一步

**已有依据核对基础、独立合成观察实验和本地研究复核台。** 本仓库在受信请求和保留原有证据的前提下，核对当前结构化请求与证据是否对应，输出有界、确定性的结果。独立沙箱支持历史回放，以及显式开启的 DeepSeek 实时提案、独立初审、Jev 实时观察、复核和 JSON 导出；尚未采集完整真实业务历史，也不会调整审核规则。

独立沙箱已有采用 **Jev 决策模型**的合成评测，用于观察 AI 提议是否符合用户意图。Jev 提供判断信号，企业原有控制仍负责审批与执行。[中英文项目简介及 Jev 分工](docs/hackathon-entry.md)

| 职责 | 当前状态 |
| --- | --- |
| 身份、授权、审批有效性与实际执行 | 继续由现有外部系统负责。 |
| 结构化请求与证据的对应 | 本仓库已有原型，依赖受信输入与保留原有证据。 |
| 原始意图与 AI 计划 | 独立本地业务沙箱提供可选 Jev 决策模型观察；提示不构成执行授权。 |
| 真实审批记录与拟提交业务字段 | 需要单独设计、可信接入与验证。 |
| 研究复核记录 | 独立本地沙箱提供初审/复核、历史回放或显式 DeepSeek/Jev 实时调用、未评分草案和 JSON 导出。 |
| 真实业务结果与人工参与调整 | 研究目标；尚无可信业务结果接入、业务同事试审或自动调整功能。 |

当前业务证据契约会绑定所提供的审批字段，但不解释字段含义。请求改变后，旧证据不会与新请求匹配；摘要一致也不能证明来源身份、审批有效、业务正确或允许执行。[业务证据契约](docs/business-action-evidence-v1.md)

## 试用研究复核原型

在**独立本地仓库** `agentharness-business-sandbox` 中运行
`./run-sandbox review --port 8769`，打开 `http://127.0.0.1:8769`。
阅读原始案例，保存初审，查看 Jev 留存结果，再填写复核结论并导出。
共有六条已见合成案例，不产生新的模型调用或业务动作。记录保存在内存中，
服务重启后清空。这是工程 PoC，尚未由业务同事试审。[启动、演示与范围](docs/research-review-workbench.md)

实时模式使用 `./run-sandbox review --live --port 8770` 和已有配置。
2026-11-04 已通过浏览器实际请求 DeepSeek 3 次、OpenRouter/Jev 3 次，均收到有效
响应，并留存实际操作视频与规范化记录。每次服务启动最多各尝试 3 次，合成输入
会外发并产生模型用量。[实测结果与限制](docs/research-review-workbench.md#live-acceptance-on-2026-11-04)

## 一个值得研究的业务问题

在虚构的交付异常中，销售、物流和服务团队需要协同。AI 可以设想承担汇总信息、准备跟进建议和提出工单转派方案；负责人可能要求在改变责任归属前先确认。我们希望研究如何关联这次提议、相关确认及其条件，并留存最终结果用于复盘。

完整场景是未来流程示意。已有 E173 合成案例只涉及待确认的工单转派，不证明交付异常背景或已有完整审批流程。[PoC 来源说明](docs/presentations/evialign-ppt-expanded-delivery.md#evidence-and-provenance)

## 已有证据

2026-10-21，独立沙箱对 84 个合成意图观察案例进行单次评测：36 个越界案例均被标记，24 个意图不清案例均收到复核提示，24 个正常案例中有 3 个也收到复核提示。

案例由 AI 编写并由另一 AI 独立盲标，覆盖 33 个相关场景族，非人工真值、非联想业务数据。这些结果不能证明生产准确率、真实审批与行动对照能力、节省工时或 ROI。[完整评测记录](docs/33-jev-shadow-maintenance-handoff.md)

## 怎样判断价值

现有 API、细粒度授权、审批和审计系统可能已经覆盖所需控制。引入额外组件的理由，需要真实缺口或减少重复接入、核对成本的实证。

选择一个获批的业务流程，以只读回放比较三种做法：现有机制、合理补强现有机制，以及拟议接入 EviAlign。记录差异发现情况、整体处理时间、新增复核负担、接入维护成本与跨智能体复用投入。若现有能力已满足需要，或新增成本超过可证明的收益，就继续复用现有方案。

如有明确价值，再单独设计可信业务记录接入与旁路观察，在保留原有控制的前提下积累人工判断和结果。研究调整人工参与应在验证及企业批准之后；当前原型不授予执行权限。

## 按角色阅读

| 读者 | 建议入口 |
| --- | --- |
| 领导与黑客松评审 | [项目目的与当前进展](docs/project-purpose-and-progress.zh-CN.md)、[项目评审材料](docs/actlumen-reviewer-brief.md)、[最新版 PPT 交付记录](docs/presentations/evialign-ppt-expanded-delivery.md) |
| 业务试点负责人 | [品牌与能力范围](docs/actlumen-brand-and-scope.md)、评审材料中的拟议对照与试点 |
| 开发与平台团队 | [完整工程参考](docs/engineering-guide.md)、[资产地图](docs/00-asset-map.md) |
| 安全与证据评审 | [产品契约](docs/08-glossary-and-product-contract.md)、[可复现演示](docs/11-reproducible-enterprise-demo.md)、[检查清单](docs/13-external-reviewer-checklist.md) |
| 后续维护者 | [当前维护记录](docs/maintenance.md)、[仓库工作规则](AGENTS.md) |

当前正式 PPT 为 20 页，附真实操作影片及 PDF，已在本地交付；文件和来源见[汇报交付记录](docs/presentations/evialign-ppt-expanded-delivery.md)。已被替代的制作草稿通过[固定历史版本](docs/maintenance.md#archived-production-materials)查阅。

## 目录结构

纳入版本控制的文件夹按用途划分：

| 文件夹 | 内容 |
| --- | --- |
| [src/](src/) | Python 实现代码，包括命令行入口、证据核对、本地评测和报告生成。 |
| [tests/](tests/) | 单元测试、命令行测试、异常输入测试和端到端证据回归测试。 |
| [docs/](docs/) | 项目目的、当前进展、契约、工程指南、留存结果和汇报文件位置。 |
| [examples/](examples/) | 用于本地演示与测试的示例策略、合成证据记录和固定样例。 |
| [schemas/](schemas/) | 策略、任务、请求/响应、审计文档的结构定义，以及参数规范化测试向量。 |
| [policies/](policies/) | 工具风险分类和治理策略数据。 |
| [patterns/](patterns/) | 机器可读的智能体架构与设计模式。 |
| [evals/](evals/) | 本地安全评测数据，包括冒烟案例与声明式断言。 |
| [release/](release/) | 按日期留存的源码发布、里程碑和交接记录；存在记录不代表已对外发布。 |
| [.github/](.github/) | GitHub 配置，目前用于自动化 CI 验证。 |

<details>
<summary>展开查看子目录和示例内容</summary>

| 子目录 | 内容 |
| --- | --- |
| [src/agentharness/](src/agentharness/) | Python 包：命令分发、校验器、证据绑定、本地评测与审计报告构建。 |
| [.github/workflows/](.github/workflows/) | CI 任务，负责策略校验、本地案例评测和测试。 |
| [docs/presentations/](docs/presentations/) | 汇报交付索引、文件摘要和录屏来源；PPT、视频二进制文件另行交付。 |
| [docs/superpowers/](docs/superpowers/) | 工程设计索引及历史实施计划链接。 |
| [docs/superpowers/specs/](docs/superpowers/specs/) | 留存的工程规格与限定范围的设计决策。 |

以下每个文件夹都是独立的合成样例，不是真实业务流程：

| 示例目录 | 演示内容 |
| --- | --- |
| [examples/agent_bus/](examples/agent_bus/) | 基础任务、证据、评审与事件台账结构。 |
| [examples/agent_bus_tool_gate/](examples/agent_bus_tool_gate/) | 工具策略门的证据记录。 |
| [examples/agent_bus_approval/](examples/agent_bus_approval/) | 对留存审批记录的对应检查。 |
| [examples/agent_bus_preflight/](examples/agent_bus_preflight/) | 执行前准备状态报告的校验。 |
| [examples/agent_bus_handoff/](examples/agent_bus_handoff/) | 交接报告检查。 |
| [examples/agent_bus_adapter_registry/](examples/agent_bus_adapter_registry/) | 基于注册表的适配器声明；也是导出、摘要清单和审计的主要样例。 |
| [examples/pi_tool_call_mapping/](examples/pi_tool_call_mapping/) | 合成的 Pi 风格观察及预期映射结果。 |

文件总线样例按需要复用以下子目录名：

| 样例子目录 | 内容 |
| --- | --- |
| `tasks/` | 结构化的示例任务请求。 |
| `evidence/` | 事件台账引用的每次尝试证据。 |
| `reviews/` | 对这些尝试的评审记录。 |
| `tool_gates/` | 工具策略门报告。 |
| `approvals/` | 示例审批记录，不代表经过认证的企业审批。 |
| `preflight/` | 已保存的执行前检查报告。 |
| `handoffs/` | 已保存的交接报告。 |
| `adapters/` | 适配器规格，以及使用注册表时对应的注册表。 |

</details>

<details>
<summary>展开查看本地可能出现、未纳入版本控制的目录</summary>

| 目录 | 用途 |
| --- | --- |
| `.git/` | Git 历史和仓库元数据。 |
| `.superpowers/` | 临时任务进度和审查草稿，与受版本控制的 `docs/superpowers/` 不同。 |
| `.cursor/` | 本地 Cursor 编辑器设置。 |
| `.worktrees/` | 其他任务使用的本地独立 Git 工作区。 |
| `.understand-anything/` | 自动生成的代码分析索引和本地分析设置。 |
| `.venv/` | 本地 Python 虚拟环境。 |
| `__pycache__/`、`.pytest_cache/` | 自动生成的 Python 或测试缓存。 |
| `artifacts/` | 自动生成的本地评测报告。 |
| `build/`、`dist/`、`*.egg-info/` | 自动生成的打包、构建产物。 |

技能需要时会重建 `.superpowers/`，但重建目录不会恢复已删除的进度和审查草稿。
`agentharness-business-sandbox` 是独立仓库，不是当前仓库中的一个文件夹。

</details>

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

EviAlign 是当前项目名称；AgentHarness 和 ActLumen · 明行是历史名称。现有 `agentharness` 命令、Python 包名、协议与源码路径保留兼容，历史记录保留发生时的名称。当前源码预发布版本仍为 `v0.2.0-alpha.1`，本次更新不构成新版本或包发布。

`allow_candidate` 仅表示候选证据，当前证据与观察输出保留 `result_status: not_executed`。本仓库不提供身份认证、可信签字、运行时授权、审批语义、事务或工具执行。[完整范围说明](docs/actlumen-brand-and-scope.md)

MIT License · [许可证](LICENSE)
