# ActLumen 品牌与评审材料执行计划

> **For agentic workers:** Use superpowers:executing-plans for this continuation, with one fresh read-only review before delivery.

**Goal:** 统一 ActLumen · 明行的对外名称与业务话术，完成可供评审阅读的中文材料，并同步 Windows 交付。

**Architecture:** 在现有文档和单文件 HTML 上做品牌与内容维护，不改变产品行为。评审源文保存在 Markdown；临时导出程序生成 Word、A4 HTML/PDF。保留旧包、命令和历史记录以维持兼容。

**Tech Stack:** Markdown、现有原生 HTML/CSS/JS、Python 标准库 OOXML/ZIP、隔离 Chrome 验收。

**Spec:** `docs/superpowers/specs/2026-10-26-actlumen-brand-reviewer-design.md`。用户明确批准名称并请求执行。

## 约束

不新增运行时授权、业务执行、模型调用或真实企业部署。评审业务收益与拟议界面不得冒充实测和已交付能力。保留历史名称、稳定 CLI/包名、旧版本和协议。只修改明确文档路径与包描述；GitHub 地址是否改名等待用户说明，不推断为推送授权。

## 任务

- [x] 1. 撰写 `docs/actlumen-reviewer-brief.md` 与 `docs/actlumen-brand-and-scope.md`；更新 README、docs/00、docs/07、docs/08、pyproject 描述及现有汇报的品牌。
- [x] 2. 导出 Word/A4 HTML/四页 PDF；核对源文一致性、DOCX 结构、PDF 页数和内容布局；复验汇报改名后的导航、断网展示和八页打印。
- [x] 3. 运行 AGENTS 六项检查与本地链接/格式检查；独立审查真实性、品牌一致性及兼容边界；记录结果，向 Windows 目录复制并逐字节校验。
- [x] 4. 按用户对 GitHub 改名问题的回复处理远程名称和本地 remote；保留未授权动作不执行的准确状态，不把本地维护写成已推送。

## 审查重点

1. 明行业务名称是否清晰且未承诺审批、执行、身份或绝对安全。
2. 原型能力、独立沙箱观察、拟议用户界面、真实业务收益是否清楚区分。
3. 保留的旧命令、包、协议和历史记录是否仍可用，当前入口名称是否一致。
4. Word/PDF 是否包含完整源文、四页可读内容、证据局限和来源。
5. Windows 副本与本地源是否一致；GitHub 改名与推送状态是否依据实际回执。

## 执行记录

本次为既有材料的明确品牌维护，不重新设计产品。延续当前工作区中已交付的未提交汇报改动；GitHub 名称问题采用异步澄清，独立材料工作继续进行。

用户已明确选择同步改名 GitHub 仓库。名称、简介与 origin 已更新，repo ID、私有状态和 main 保持一致；未推送源文件。四页评审 PDF 和八页汇报 PDF 已直接渲染核验，Word 已做结构与全文检查（非 Office 渲染页数认证）。六项检查通过，538 项测试耗时 37.990 秒。

独立审稿发现的一项打印来源说明问题已补充可打印文字并复验 PDF。没有未解决的实质性问题。审查中未另做的 GitHub、Windows、版面和测试检查由主代理完成；独立沙箱原始数据、商标、域名和真实 ROI 仍在本任务范围之外。

完整维护与交付依据见 `docs/34-actlumen-brand-maintenance.md`。品牌对原视觉的有意调整为：ActLumen · 明行名称、命名说明、当前仓库地址和更长标题的字体适配；白底、深蓝青绿、层板插图、控件与留白沿用已批准样式。桌面 1672×941、1366×768 与手机 390×844 均已检查；没有新增外部图片或字体依赖。
