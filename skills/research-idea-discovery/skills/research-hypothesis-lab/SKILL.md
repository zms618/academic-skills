---
name: research-hypothesis-lab
description: Use when user requests research hypothesis discovery candidate generation mechanistic gap analysis. Works within the general Research Idea Discovery plugin and any user-selected field.
---

# 研究缺口与可证伪假设 — Idea First

先阅读论文、失败与反例，产生 2–4 个 `IDEA_SEED`，列出科学问题、最小机制、独特可证伪预测、所需数据/标签字段与 E0、最简竞争方案；**不得要求用户提前提供数据集或通过 G0 后才允许创意生成**。论文证据不足标 `HYPOTHESIZED`，不能伪称观察事实。

把每条 Seed 交给 Literature Scout **主动检索数据与 baseline**，再进行 D0/G0；仅通过可行性及动机审查的 Seed 可冻结为 Research Candidate。没有现有/轻量衍生数据则放弃或重构该 Seed，不推荐为值得投稿的 Idea。

所有事实记录引用、证据级别及未核查事项。输出交接对象包括 `idea_id, hypothesis, falsifier, required_data_fields, baseline, E0, sources, status`。
