# ActLumen · 明行品牌与评审材料维护记录

维护日期：2026-10-26。此次工作统一项目名称与业务介绍，并提供面向联想集团黑客松评审的材料；不新增产品执行能力或版本发布。

## 名称与入口

项目品牌统一为 **ActLumen · 明行**，业务定位为“企业 AI 行动质检助手”，主张为“让 AI 行动清晰，让业务协作高效”。命名含义、范围与兼容关系见[品牌说明](actlumen-brand-and-scope.md)。

当前入口包括：

- [项目评审材料源文](actlumen-reviewer-brief.md)：摘要、命名、问题与场景、方案特点、原型证据、预期收益和试点建议。
- [八页管理层汇报](presentations/agentharness-enterprise-hackathon.html)：已更新显示名称，文件路径保留兼容。
- [README](../README.md)、[资产地图](00-asset-map.md)、[企业定位](07-enterprise-positioning-and-boundary-audit.md)和[产品契约](08-glossary-and-product-contract.md)：当前介绍使用新品牌，并说明历史名称。

原始发布、计划和交接记录按发生时的名称保留。CLI `agentharness`、Python 包/安装名、源码目录、版本和证据协议未改动；`pyproject.toml` 只更新描述。独立业务沙箱与无关 worktree 未修改。

## GitHub 名称回执

用户明确确认将 GitHub 仓库同步改名为 ActLumen。此次 GitHub API 更新并读回核验了：

| 项目 | 核验结果 |
| --- | --- |
| 仓库 | `alexzhu0/AgentHarness` → `alexzhu0/ActLumen` |
| 地址 | `https://github.com/alexzhu0/ActLumen` |
| 仓库标识 | 前后均为 `1268211096`，为同一个仓库。 |
| 访问级别与默认分支 | 保持私有与 `main`。 |
| 项目简介 | 更新为 ActLumen · 明行及企业 AI 行动质检定位。 |
| 本地 origin | 更新为 `https://github.com/alexzhu0/ActLumen.git`。 |

名称和简介更新不等于文档源文件已推送。本记录不作为推送、Git tag、公开发布、包发布、部署或商标确认回执。

## 材料与交付

评审材料从同一 Markdown 源文导出可编辑 Word、A4 HTML 与四页 PDF。八页汇报另导出 PDF。Word/PDF 等生成文件只交付至用户指定 Windows 目录，不纳入 Git。

交付文件为 `ActLumen-明行-项目评审材料.docx`、同名 `.pdf` 和 `.html`，以及 `ActLumen-明行-项目汇报.html` 与同名 `.pdf`。原 Windows 汇报路径同步更新，既有技术版保留，更新前的管理层版另存备份。会话中逐字节核对全部副本与其来源一致。

DOCX 通过 ZIP、XML、分页符和全文一致性核验；本环境未提供 Office 实机渲染。PDF 直接渲染后逐页检查，评审材料为四页 A4，汇报为八页 16:9，正文与页脚没有重叠。

## 本轮验证

在 `5c6c72e` 加本次明确文档和包描述变更的工作区上，以下命令均通过；Python 命令全部设置 `PYTHONDONTWRITEBYTECODE=1`：

- 策略校验：`./agentharness validate examples/agent_policy.example.yaml`。
- 三例冒烟：`./agentharness eval --cases PI-001,PD-001,SEC-001`，3/3。
- 两个 loop fixture：`examples/agent_bus` 与 `examples/agent_bus_adapter_registry`。
- 全量单元测试：`python3 -m unittest discover -s tests -q`，538 项，37.990 秒。
- `git diff --check`，以及新增源文的本地链接和空白检查。

使用独立 Chrome 会话检查品牌显示、目录与场景切换、全屏、手机宽度、断网加载、无 JavaScript 阅读及八页打印。评审 PDF 四页均含完整正文与页眉，版面边界检查通过。临时工具与导出过程未改变项目依赖。

独立只读审查未发现 Critical 或 Important；指出汇报打印版的评测归属与来源入口不够明确，已在可打印正文中补充独立业务沙箱归属及维护记录指引，并重新核验八页 PDF。

没有证据契约代码变更，因此额外的契约专项套件不适用。未重跑沙箱或任何付费模型评测；84 例数字仍归属于 2026-10-21 的留存合成评测，不作为真实业务收益或上线效果。

## 后续工作

真实业务界面、联想系统接入、企业收益验证与运行时执行，继续按独立设计和审批范围开展。品牌维护不扩大权限或执行职责。下一项业务工作是选定单流程只读试点及其对照指标。
