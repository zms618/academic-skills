# Best Idea Card — 交付标准模板

## -3. Idea Seed（先形成初步假设，不要求用户提供数据集）
- 来自哪些论文失败/研究缺口？科学命题、机制思路、输入输出与唯一预测是什么？
- 需要哪些模态/字段/标签和 E0 诊断？简单竞争方案是什么？
- 标 `IDEA_SEED / UNVERIFIED`，不等于可行或可投稿。

## -2. Plugin-discovered D0 Dataset Anchor (after Idea Seed)
- 由插件自己发现的现有原始数据集名称、官方下载/有效本地路径、实际访问核验及许可来源；用户无须提供。
- `mode=EXISTING` 或 `DERIVED_FROM_EXISTING`；不得凭空创建大规模新数据。
- 字段/标签、数据划分与公平实验评价，相关公开代码或可重建 baseline。
- Derived 另写父数据集、衍生变换步骤、标签来源、制作预算及防泄漏方案。
- 指明该数据支持哪一项可推翻假设的实验；若 D0 UNKNOWN，则只能保留探索性种子，不得输出正式 Idea Card。


## -1. Mandatory Feasibility Card — Idea Seed 后、正式候选之前
- G0 结论：FEASIBLE_VERIFIED / CONDITIONALLY_FEASIBLE / INFEASIBLE / UNKNOWN（必须说明验证深度）。
- **具体数据与可获取权限**：名称、URL/本地来源、许可、字段/标签、规模和划分；理论型注明为何不需要数据。
- **Baseline 与评价**：可复现途径、评价指标、可观察反例。
- **预算与时限**：真实拥有的 GPU/显存/设备/人力、估算耗时/费用、审批/伦理状态。
- **E0 最小验证**：1 个低成本可执行步骤、停止信号与最大阻碍。
- 若 G0 未通过，本卡只能作为 feasibility rescue plan，不继续声称可投稿 Idea。

## -0.5. M1 Motivation Card（G0 后、正式新颖性审计前）
- 失败现象与具体证据、影响/科学意义、根因/隐含假设、两个竞争解释、最强简单基线为何不够、为何现在值得做、可证伪预测。
- 对每个核心 Claim 标 `SUPPORTED / PLANNED / UNKNOWN` 与来源、locator，拒绝仅靠热词或视觉包装称重要。
- 动机不强或证据不够时，不再给出正式投稿候选。

## -0.35. N → L → M2 审查记录（故事审查之前）
- N：危险近邻 3–7 篇（或明确覆盖局限），实际引用与机制差异，近邻作者最强解释；记录 `idea_id + revision`。
- L：根因→新机制→可测预测→最简 rival→必要性消融；混杂因素与可推翻效应的实验。
- M2：原动机、近邻已覆盖范围、剩余重要缺口、修订主张、独有预测、为什么研究仍值得做。若已解决则 STOP/PIVOT。

## -0.25. S Story Card（M2 通过之后）
- 9 环论证链；30 秒 pitch；Introduction 逻辑提纲；Claim→Evidence/Experiment 图谱。
- M（动机）/ N（新颖性与必要性）/ R（冷读审稿）三类质疑及每轮真实新证据或机制修改、尚未解决的关键反驳。
- 明确区分“论证结构通过”与“审稿人真正会认可”，不能提前写作论文已验证结论。

## 0. Verdict & Scope
- 模式、目标会议/论文类型（如果已核实）、检索截止日期和文献覆盖边界
- `PROCEED_TO_PILOT / REFINE / PIVOT / STOP / UNVERIFIED`
- 一句话最核心判断与最危险的前提

## 1. Problem: 一句话研究问题
- 应用场景；输入/输出；可用训练和测试信息；当前方法难以解释的失败。
- 源文件/论文明确证据（含页码或 URL），与猜想严格分离。

## 2. Failure → Assumption → Hypothesis
- 观察到什么失败 F？
- 以往方法暗含何假设 A？
- 新假设 H 是什么？什么条件下 H 为假？
- 两个竞争解释是什么？

## 3. Central Insight & Mechanism
- 不超过三句话的机制故事。
- 一个主贡献而不是堆叠模块。
- I/O、数据流、关键决策、冻结/更新参数、训练/测试目标。
- 必要时给出伪代码或玩具数值推演。

## 4. Prior-Art Collision Matrix
- 三个（或证据允许的若干）最危险近邻：论文、准确来源、具体机制、相同点、实质区别、未核实处。
- One-sentence novelty delta。
- 是否等价于已有组件换名？

## 5. Naive Baseline & Unique Prediction
- 不低估现有强 baseline；另列能替代新方法的最简单 baseline。
- 预期在何条件下本方法与两个 baseline 的行为会显著不同？

## 6. Killer Experiment
- 假设；干预；控制；指标；预期成功/失败信号；混杂变量；标签可见性；资源开销。
- 什么实验结果应该迫使我们放弃此 Idea？

## 7. Research Package
- 必须完成的主实验、消融、成本评估、诊断图和失败案例。
- 数据与代码可取得性，最小实现路径。
- 会议适配仅在官方会议规则核实后写出。

## 8. Reviewer Attack & Next 3 Actions
- 三条最尖锐、各不相同的拒稿理由及需要补的证据。
- 三个最小下一步；每步附 go/no-go 条件。
- 真实事实、合理推断、待核实项列表。

## v2.7 Provenance & Pilot Evidence（强制披露）
- `dataset_sample_status`: CATALOG_LEAD / OFFICIAL_PAGE_CHECKED / LOCAL_SAMPLE_CHECKED / NOT_VERIFIED，附样本 hash（若执行）、实际字段与缺失字段。
- `license_status`: official source identified / permission checked / not checked，**不同于样本下载状态**。
- `review_status`: ROLE_SIMULATED / INDEPENDENT_MODEL_RUN（确有 run_id）/ REVIEW_PENDING，必须列关键未解答异议。
- `pilot_status`: PLANNED / DRY_RUN / EXECUTED_WITH_METRICS / FAILED_WITH_LOG / NOT_EXECUTED，附日志路径与实际基线对照。
- `prior_search_coverage`: 同问题、同机制、同目标、跨领域查询，检索日期、正文阅读深度与缺口；缺口须标明。
- `kill_or_revisit`: 当简单 baseline 更优、动机被实验否定或危险近邻补足时撤销或修订 Idea。
