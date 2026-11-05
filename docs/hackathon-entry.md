# EviAlign project descriptions / 项目简介

Updated: 2026-11-05. Retained project descriptions from the competition entry;
the user reports that registration has closed. Business examples do not limit
the project's intended scope.

## English project description

EviAlign is a forward-looking research project on making AI-proposed enterprise actions reviewable. It connects proposed actions with their supporting context, decision-model observations and review records, helping people examine the basis for a proposal and study where human involvement matters. The project has built an evidence-checking foundation and a working PoC with live DeepSeek proposals, TypeSafe's Jev decision-model observations, research review and export. It has been demonstrated with synthetic tasks and real model APIs. The ambition is to give enterprises a basis for improving workflows and carefully expanding AI participation; existing systems retain identity, permissions, approvals and execution.

## 中文项目简介

EviAlign 是面向企业各类流程的 AI 行动审核前沿研究项目，将拟议行动、相关依据、决策模型观察与复核记录关联起来，帮助人们看清 AI 为什么提出这项动作，并为研究人机分工积累证据。项目已具备依据核对基础和可操作 PoC，接通 DeepSeek 实时提案、Jev 决策模型观察、研究复核与导出，并使用合成任务完成真实模型 API 联调。项目希望为流程优化及有依据地扩大 AI 业务参与范围提供支持；身份、权限、审批和实际执行继续由企业原有系统负责。

## Jev's role / Jev 在项目中的作用

TypeSafe describes Jev as a structured decision model: it evaluates focused questions against supplied context and returns typed results such as choices and probabilities. Our experiment uses a Choice question to observe alignment between the user's request and an AI proposal. [Official introduction](https://docs.typesafe.ai/introduction)

本项目已有的 Jev 实验使用 Choice 问题，比较用户请求与 AI 拟议动作，形成“符合请求、可能越界、意图不清”等观察结果。本地分流规则会将意图不清或低置信结果标为复核建议。观察器在独立沙箱中默认关闭，提示本身不会暂停、批准或执行操作，也不属于主仓库 CLI。

The retained experiment requests `typesafe/jev-1.13` through OpenRouter and accepts only the pinned returned model `typesafe/jev-1.13-20260917`. Mentioning Jev does not change that pin, the 0.8 threshold or the rubric, and does not claim use of the latest release. This copy makes no unsupported popularity, performance or production-accuracy claim. [Retained experiment and limitations](33-jev-shadow-maintenance-handoff.md)

Jev supplies an intent-observation signal. The local workbench supports historical replay and opt-in live DeepSeek proposals, initial judgments, live Jev observations, final reasons and JSON export. Three real requests to each provider completed on 2026-11-04, with actual video and normalized traces. Annotations are automated demo records, without a business-reviewer trial or observed business outcomes. [Workbench / 复核台](research-review-workbench.md) · [Purpose and current progress](project-purpose-and-progress.md) · [中文说明](project-purpose-and-progress.zh-CN.md)

## Presentation material

- [Current PowerPoint delivery record](presentations/evialign-ppt-expanded-delivery.md)
- [Production history and archived materials](maintenance.md#archived-production-materials)
