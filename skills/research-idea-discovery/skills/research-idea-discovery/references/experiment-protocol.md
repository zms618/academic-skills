# 最小实验与证伪协议

## G0 必须先完成

任何 E0–E4 的实验方案之前，先根据 `feasibility-gate.md` 证明数据/实体可获得、复现与评估可实施、预算时限与审批可满足。没有适用数据集和可执行替代方案时，不创建完整模型实验计划，不把玩具合成数据当作已有真实可用 benchmark。

## 原则

先检测科学假设是否存在，再训练复杂模型。实验可以对方法持否定意见。固定数据划分、随机种子、标注使用规则和评测预算，除目标机制外控制其他差异。

## 漏斗

**E0 — 对现象做测量（无需新模型）**：在原 baseline 上量化失败条件是否真实存在。若并无差异，立即重写问题定义。

**E1 — Mechanism probe**：用简单统计、oracle upper bound（仅明确作为诊断使用，不能当实际无标签系统）、冻结特征或低成本代理验证候选决策是否具有可分辨信号。

**E2 — Naive rival**：先跑能产生类似作用的最简单机制；例如统一熵最小化、置信度过滤、固定门控、固定可靠性权重、单一 Adapter。若完全等价，不继续堆模块。

**E3 — Minimal new mechanism**：只加入主创新，保持编码器、预训练、数据、参数预算和测试更新协议尽量可比。

**E4 — Discriminating tests**：强基线、最关键消融、负面情形、类不平衡、多个 shift 强度、标准差/置信区间、额外训练和推理时间、OOD 稳定性。

## 必需的五种实验问题

1. **Existence**：问题确实存在吗？
2. **Identification**：新估计/判断是否真的捕捉目标机制？还是仅与置信度相关？
3. **Causality/necessity**：控制其他因素后，目标机制是否决定效果？交换、打乱、反事实、去掉部件是否改变预测？
4. **Superiority**：相对最强相关基线和最简竞争方案能否得到稳定的增益？
5. **Cost/boundary**：在哪些情形失败、代价是什么？

## 实验卡标准字段

`ID | hypothesis | control baseline | intervention | dataset/split | metric(direction) | success signal | kill signal | labels available at test | GPU/time/memory estimate | confounders | status: PLANNED/RUN/FAILED/BLOCKED`

执行权限：未经授权不可自行运行长时间 GPU 实验；未运行的数值必须写 `N/A`。证据不充分或无资源时写出最低成本可行的纸面实验，而不是承诺结果。

## v2.7 Pilot feedback
- 未运行实验的唯一合法状态为 `PILOT_PLANNED` / `NOT_EXECUTED`。
- 已运行的失败实验必须保存真实 stderr/exit status，不能按计划成功汇报。
- 成功的本地命令必须伴随可核验的输出日志与 metrics JSON；指标需要同数据划分、同预算的 baseline 对照及方向。单次成功不证明统计显著性或因果有效。
- 简易 baseline 相当或更好、E0 不存在目标现象、指标泄漏等都触发重新审查，不能通过 S 故事改写来解决。
