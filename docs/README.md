# EviAlign 文档导航

EviAlign 是面向 AI 行动请求的执行前依据核对原型。真实审批内容与拟提交动作的业务对照属于待验证方向；独立业务沙箱另有可选意图观察。按阅读目的选择入口：

## 项目与业务价值

| 文档 | 适合了解的内容 |
| --- | --- |
| [英文项目首页](../README.md) · [简体中文版](../README.zh-CN.md) | 项目是什么、业务场景、已有成果和下一步；GitHub 默认展示英文。 |
| [联想集团黑客松评审材料](actlumen-reviewer-brief.md) | 命名、问题、方案特点、企业收益和试点建议。 |
| [八页管理层汇报](presentations/agentharness-enterprise-hackathon.html) | 下载后可离线演示、切换场景、全屏和打印。 |
| [品牌与能力范围](actlumen-brand-and-scope.md) | EviAlign 的统一名称、产品化状态与兼容标识。 |

## 工程与资产

| 文档 | 用途 |
| --- | --- |
| [完整工程参考](engineering-guide.md) | 安装、命令、CI、功能边界、源码布局与历史工程入口。 |
| [资产地图](00-asset-map.md) | 模式库、治理策略、评测与编译器等资产总览。 |
| [设计模式](01-agent-design-pattern-library.md) | Agent 设计方法与可复用工程模式。 |
| [工具治理策略](02-tool-governance-policy.md) | 风险、审批证据与工具治理设计。 |
| [安全评测](03-agent-safety-eval-suite.md) | 可回归的策略与安全检查设计。 |
| [策略编译](04-prompt-policy-compiler.md) | 结构化策略与指令投影的设计。 |
| [文件总线](05-loop-file-bus.md) | 本地证据与任务记录协议。 |
| [证据架构与运行时边界](06-runtime-architecture.md) | 本项目的证据职责与外部执行职责。 |
| [企业定位](07-enterprise-positioning-and-boundary-audit.md) | 工程类别与相邻系统的分工。 |
| [术语与产品契约](08-glossary-and-product-contract.md) | 统一术语、当前范围和执行边界。 |
| [外部系统集成策略](09-source-backed-integration-strategy.md) | 基于来源记录的未来集成方案。 |
| [业务行动证据契约](business-action-evidence-v1.md) | 当前请求与行动依据的匹配检查。 |
| [独立合成数据实验室](31-synthetic-data-access-lab.md) | 独立实验室的使用与职责边界。 |

## 评审与复现

- [工程证据演示](10-enterprise-audit-report-and-buyer-demo.md)
- [可复现演示步骤](11-reproducible-enterprise-demo.md)
- [评审决策指南](12-buyer-reviewer-decision-guide.md)
- [检查清单](13-external-reviewer-checklist.md)
- [评审复现记录](14-reviewer-dry-run-and-reproducibility.md)
- [Pi 边界方案](17-pi-integration-boundary-and-contract.md)、[静态映射](18-pi-tool-call-mapping-fixture.md)、[契约检查命令](19-pi-contract-check-cli.md)、[双仓 dry-run 说明](20-pi-dual-repo-dry-run-e2e.md)

工程演示检查的是证据与契约，不会自动授权或执行真实业务操作。

## 维护与历史追溯

- [EviAlign 品牌与 GitHub 维护记录](34-actlumen-brand-maintenance.md)
- [独立沙箱交接](32-business-sandbox-maintenance-handoff.md)
- [Jev 留存评测与交接](33-jev-shadow-maintenance-handoff.md)
- [历史发布记录索引](../release/README.md)
- [仓库工作规则](../AGENTS.md)

历史发布、验收和交接记录保留 AgentHarness 名称、当时版本与证据。现有 `agentharness` 命令、包名、协议和兼容路径继续可用。历史开发循环文档不定义当前工作流程；新工作以 AGENTS.md 的 Superpowers 规则为准。
