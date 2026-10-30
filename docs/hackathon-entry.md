# EviAlign hackathon entry

Updated: 2026-10-30. Registration copy for the research project; business examples do not limit its intended scope. Suggested team name: **Evidence in Action / 有据行动队**.

## English project description

EviAlign is a forward-looking research project on reviewing AI actions across enterprise workflows. It explores linking action requests with business evidence, human judgments and subsequent outcomes to support traceability and evidence-based human–AI collaboration. A partial evidence-checking prototype is implemented, and a separate sandbox has conducted a synthetic evaluation of TypeSafe's Jev decision model to observe whether AI proposals align with user intent. The long-term goal is to study when human confirmation remains necessary and when intervention could be reduced under validated conditions. Existing enterprise systems retain responsibility for identity, permissions, approvals and execution.

## 中文项目简介

EviAlign 是面向企业各类业务流程的智能体行动审核前沿研究项目，探索关联 AI 行动请求、业务依据、人工判断与后续结果，为审核追溯和人机分工优化积累证据。项目已完成部分依据核对原型，并在独立沙箱中采用 Jev 决策模型开展合成实验，观察 AI 提议是否符合用户意图。长期目标是研究哪些环节需要人确认、哪些特定情形可以减少人工介入，为企业有依据地扩大 AI 的业务参与范围提供支持。身份、权限、审批和实际执行继续由企业原有系统负责。

## Jev's role / Jev 在项目中的作用

TypeSafe describes Jev as a structured decision model: it evaluates focused questions against supplied context and returns typed results such as choices and probabilities. Our experiment uses a Choice question to observe alignment between the user's request and an AI proposal. [Official introduction](https://docs.typesafe.ai/introduction)

本项目已有的 Jev 实验使用 Choice 问题，比较用户请求与 AI 拟议动作，形成“符合请求、可能越界、意图不清”等观察结果。本地分流规则会将意图不清或低置信结果标为复核建议。观察器在独立沙箱中默认关闭，提示本身不会暂停、批准或执行操作，也不属于主仓库 CLI。

The retained experiment requests `typesafe/jev-1.13` through OpenRouter and accepts only the pinned returned model `typesafe/jev-1.13-20260917`. Mentioning Jev does not change that pin, the 0.8 threshold or the rubric, and does not claim use of the latest release. This copy makes no unsupported popularity, performance or production-accuracy claim. [Retained experiment and limitations](33-jev-shadow-maintenance-handoff.md)

Jev supplies an intent-observation signal. The main repository's correspondence checks, the independent sandbox experiments and future business judgment/outcome collection remain distinct; they have not been integrated into a complete enterprise approval workflow. Cross-workflow reuse is a research goal, with individual scenarios requiring trusted integration and validation. [Purpose and current progress](project-purpose-and-progress.md) · [中文说明](project-purpose-and-progress.zh-CN.md)

## Presentation and cover material

- [Current PowerPoint delivery record](presentations/evialign-ppt-expanded-delivery.md)
- [16:9 cover-image prompt](presentations/evialign-cover-prompt.zh-CN.txt)

The cover is a research concept illustration. It must not depict a real product interface, certified approval or measured business outcome as already delivered.
