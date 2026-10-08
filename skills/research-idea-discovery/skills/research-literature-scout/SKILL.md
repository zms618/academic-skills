---
name: research-literature-scout
description: Use when user requests paper literature retrieval evidence mapping query planning and source verification. Works within the general Research Idea Discovery plugin and any user-selected field.
---

# 文献调查 + Idea 后主动检索数据集

先阅读可获得论文资料，构建带来源的失败现象/机制差异 Evidence Map；**不必先找数据才能让 Hypothesis Lab 产生 IDEA_SEED**。当收到 Seed 后，根据其所需模态、字段、标签、评测/最小证伪实验，主动搜索现有数据/父数据、官方 benchmark、论文项目页、许可、代码、可复现 baseline。优先近邻论文的数据集，扩展跨平台/官方仓库；条件允许时通过 ChatGPT web 工具或宿主中的 `scripts/dataset_discovery.py` 检索线索，再逐项核查。

每个 Seed 输出 `dataset-search-ledger.json`：搜索词、日期、至少若干潜在数据来源、官方链接与元数据/下载/访问证据、字段标签、许可、划分、基线、与 E0 适配、低成本衍生方案。若找不到，`NO_DATA_PATH` 并回到种子生成；不得要求用户预先给已核实数据集。

区分 `METADATA_ONLY / PAGE_CHECKED / ACCESS_CONFIRMED / DERIVATION_FEASIBLE / BLOCKED / UNKNOWN`。元数据不等于下载成功，离线检查不等于真实许可已核验；没有证据就不能通过 D0。不可声称绝对不存在数据集。

当常规文献搜索达到实质性证据瓶颈或用户请求深度调研时，交给 `research-deep-research-bridge` 构建**有具体缺口的可复制 Prompt**，记录已检查文献/查询与不确定性。外部报告回传后作为二手来源，不直接升级 E2/E3 全文证据等级。
