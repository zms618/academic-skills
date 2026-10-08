---
name: research-novelty-auditor
description: Use when user requests prior art novelty scooping collision auditing scientific research papers. Works within the general Research Idea Discovery plugin and any user-selected field.
---

# 机制级论文撞车审计

先冻结 idea 版本，再检索同问题/同机制/同目标/跨任务四类近邻。为 3–7 篇危险论文写六轴对照与来源深度评级，允许 HIGH_RISK 或 UNVERIFIED。阅读主 Skill references/novelty-protocol.md，不把缺乏检索当不存在先例。

开始正式撞车审计前确认该候选有已通过 G0 的 Feasibility Card；无资源时仅可答用户明确要求的文献事实查重，不能因此判定某个不可行 Idea 值得做。

所有事实记录引用、证据级别、未核实项。输出可审计的交接对象，包括 `inputs`, `sources`, `questions`, `verdict`, `next_gate`。用户明确更换研究领域时重置当前研究假设，不强行继承上一主题。
