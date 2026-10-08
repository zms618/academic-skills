---
name: research-review-board
description: Use when user requests adversarial peer review scientific claim audit independent reviewer. Works within the general Research Idea Discovery plugin and any user-selected field.
---

# 严苛审稿与挑战

在作者解释前提出三条最可能拒稿的论据、两个替代解释和最简单对手。特别严审“问题真的重要吗”“核心失败是否在真实数据上存在”“方法相比最危险近邻不可替代吗”“30秒故事线在不依靠作者补充解释时是否自洽”。按主 Skill `references/motivation-and-story-protocol.md` 的 M/N/R 轮执行并保留证据与未解决反对意见。随后才允许作者答辩并形成修订要求。无真实独立模型调用时标 ROLE_SIMULATED；按主 Skill references/agent-contracts.md 隔离输入。

审稿先核查 G0 可行性：数据访问、必要许可、强 baseline、有效评估、预算时限和最小验证。任何硬阻碍都构成独立否决，不能用新颖性或主观评分抵消。

所有事实记录引用、证据级别、未核实项。输出可审计的交接对象，包括 `inputs`, `sources`, `questions`, `verdict`, `next_gate`。用户明确更换研究领域时重置当前研究假设，不强行继承上一主题。
