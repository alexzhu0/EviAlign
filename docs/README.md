# EviAlign 文档导航

EviAlign 研究企业如何审核 AI 拟采取的行动，以及如何通过判断与结果积累研究人机分工。当前已有依据核对基础、独立合成意图观察和可操作的研究复核台；完整业务审核与经验积累闭环仍待建设。按阅读目的选择入口：

## 目录分组

| 目录 | 内容 |
| --- | --- |
| [product/](product/) | 项目目的、当前进展、定位与评审材料。 |
| [contracts/](contracts/) | 证据协议、产品边界，以及与契约绑定的 Pi 准备状态和历史验收记录。 |
| [guides/](guides/) | 工程参考、资产地图、演示和评审操作指南。 |
| [research/](research/) | 集成研究、独立实验室交接及 DeepSeek/Jev 留存结果。 |
| [presentations/](presentations/) | 最终汇报文件位置、摘要和录屏来源。 |
| [superpowers/](superpowers/) | 工程设计规格及历史实施计划索引。 |

`README.md` 是总导航，`maintenance.md` 保存跨目录维护记录。
历史编号、源码锚点和当时名称保留用于追溯；旧路径的查询方式见
[目录整理记录](maintenance.md#documentation-layout-on-2026-11-06)。

## 项目与业务价值

| 文档 | 适合了解的内容 |
| --- | --- |
| [英文项目首页](../README.md) · [简体中文版](../README.zh-CN.md) | 项目是什么、业务场景、已有成果和下一步；GitHub 默认展示英文。 |
| [项目目的与当前进展（English）](product/project-purpose-and-progress.md) · [中文版](product/project-purpose-and-progress.zh-CN.md) | 主仓库为何存在、长期研究目标、现在做到哪一步及下一阶段验证路径。 |
| [中英文项目简介与 Jev 分工](product/hackathon-entry.md) | 留存的跨流程项目介绍，以及已有 Jev 决策模型实验的作用与边界；本轮报名已截止。 |
| [行动复核台 / Research-review workbench](guides/research-review-workbench.md) | 本地可操作原型：历史回放或显式实时调用、初审/复核、独立草案和 JSON 导出；尚无业务同事试审。 |
| [联想集团黑客松评审材料](product/evialign-reviewer-brief.md) | 命名、问题、方案特点、企业收益和试点建议。 |
| [最新版 PPT 与 PoC 交付记录](presentations/evialign-ppt-expanded-delivery.md) | 正式答辩版为 17 页主讲、3 页附录；最终文件、制作源文件、影片来源和验收结果。 |
| [品牌与能力范围](product/evialign-brand-and-scope.md) | EviAlign 的统一名称、产品化状态与兼容标识。 |

## 工程与资产

| 文档 | 用途 |
| --- | --- |
| [完整工程参考](guides/engineering-guide.md) | 安装、命令、CI、功能边界、源码布局与历史工程入口。 |
| [资产地图](guides/00-asset-map.md) | 模式库、治理策略、评测与编译器等资产总览。 |
| [设计模式](guides/01-agent-design-pattern-library.md) | Agent 设计方法与可复用工程模式。 |
| [工具治理策略](contracts/02-tool-governance-policy.md) | 风险、审批证据与工具治理设计。 |
| [安全评测](guides/03-agent-safety-eval-suite.md) | 可回归的策略与安全检查设计。 |
| [策略编译](guides/04-prompt-policy-compiler.md) | 结构化策略与指令投影的设计。 |
| [文件总线](contracts/05-loop-file-bus.md) | 本地证据与任务记录协议。 |
| [证据架构与运行时边界](contracts/06-runtime-architecture.md) | 本项目的证据职责与外部执行职责。 |
| [企业定位](product/07-enterprise-positioning-and-boundary-audit.md) | 工程类别与相邻系统的分工。 |
| [术语与产品契约](contracts/08-glossary-and-product-contract.md) | 统一术语、当前范围和执行边界。 |
| [外部系统集成策略](research/09-source-backed-integration-strategy.md) | 基于来源记录的未来集成方案。 |
| [业务行动证据契约](contracts/business-action-evidence-v1.md) | 当前请求与行动依据的匹配检查。 |
| [独立合成数据实验室](research/31-synthetic-data-access-lab.md) | 独立实验室的使用与职责边界。 |

## 评审与复现

- [工程证据演示](guides/10-enterprise-audit-report-and-buyer-demo.md)
- [可复现演示步骤](guides/11-reproducible-enterprise-demo.md)
- [评审决策指南](guides/12-buyer-reviewer-decision-guide.md)
- [检查清单](guides/13-external-reviewer-checklist.md)
- [Pi 边界方案](contracts/17-pi-integration-boundary-and-contract.md)、[静态映射](guides/18-pi-tool-call-mapping-fixture.md)、[契约检查命令](guides/19-pi-contract-check-cli.md)、[双仓 dry-run 说明](research/20-pi-dual-repo-dry-run-e2e.md)

工程演示检查的是证据与契约，不会自动授权或执行真实业务操作。

## 维护与历史追溯

- [当前维护与清理记录](maintenance.md)
- [工程设计索引](superpowers/README.md) · [历史阶段与实施清单](maintenance.md#engineering-history)
- [独立沙箱交接](research/32-business-sandbox-maintenance-handoff.md)
- [Jev 留存评测与交接](research/33-jev-shadow-maintenance-handoff.md)
- [历史发布记录索引](../release/README.md)
- [仓库工作规则](../AGENTS.md)

历史发布、验收和交接记录保留 AgentHarness 名称、当时版本与证据。现有 `agentharness` 命令、包名、协议和兼容路径继续可用。历史开发循环文档不定义当前工作流程；新工作以 AGENTS.md 的 Superpowers 规则为准。

已被最终材料替代的竞赛制作计划和早期汇报不再放在当前目录；固定版本的追溯入口见[维护记录](maintenance.md#archived-production-materials)。
