# Novelty Collision Protocol — 机制级学术查重

## 1. 查询：不仅搜索关键词，还搜索机制等价词

检索四类：
- **同问题**：目标任务 + distribution shift / robustness / adaptation / grounding / reliability 等。
- **同机制**：router / selective update / conditional adaptation / gating / uncertainty / evidence verification / region-wise adaptation 等，不局限用户术语。
- **同学习目标**：contrastive, entropy minimization, pseudo labeling, consistency, regularization, Bayesian calibration 等。
- **跨任务**：相同计算机制在相邻数据形态、跨模态或 test-time learning 中是否出现。

组合布尔检索，保存日期、引擎、查询、返回条目数和筛选理由。默认优先近期，保留经典、预印本及相同机制的先例；不可按任意年限宣称早期工作不存在。通过引用追踪补齐关键词检索的盲点。

## 2. 证据等级与近邻表

`E3`：全文 Method/Experiments/Appendix 已阅读，必要时核验代码；可以进行高置信机制判断。
`E2`：全文已阅读，但实现/协议关键细节不明；只能条件判断。
`E1`：只获取摘要/第三方介绍；不能进行确定的机制不重合判断。
`E0`：未能确认文献真实性或取不到内容；禁止引用为已有研究事实。

核对 DOI/arXiv/官方 proceedings；去重并标注 workshop、预印本和正式版本差别。审稿结果或会议状态只能按可核实来源陈述。

| Field | 必填解释 |
|---|---|
| Source | 可点击官方或稳定 URL、标题、年份、版本、访问日期 |
| Locator | page, figure, section, formula 或代码定位 |
| Protocol | 输入输出、标签、域、更新时机、预算 |
| Assumption | 必须成立的假设是什么 |
| Mechanism | 精确的生产者→操作→消费者依赖 |
| Learn signal | 损失、监督、伪标签、冻结和更新规则 |
| Matching axis | 哪些机制在概念上等价 |
| Difference | 是否只是换术语、换 backbone、换数据集 |
| Threat | `HIGH / MEDIUM / LOW / UNKNOWN` 和根据 |

## 3. 六轴逐项对照（主要查重门）

1. Problem & protocol：任务、监督条件、测试协议。
2. Scientific insight：科学命题与对失败的解释。
3. Decision granularity：模态/实例/区域/时间步/组件。
4. Computational mechanism：实际计算、路由、融合、适配与耦合关系。
5. Objective / update：损失和更新规则。
6. Contribution & falsifiable prediction：方法声称产生何种不可由近邻自然推出的独特结果。

**高危情形**：3–5 轴几乎相同，仅改变第 1 轴应用场景；或修改第 4 轴的模块名而计算图等价；或只有第 6 轴的指标/命名不同。

先用近邻作者最有利的解释（steelman）描述其方法，再指出确切区别。不可故意把已有工作说弱。

## 4. Delta 写法与判定

差的 delta：`我们首次提出更可靠、细粒度、动态的模块`。

合格候选 delta：`与 X 的 [已核实具体机制] 不同，我们在 [同一协议] 中做 [具体决策/目标的改变]，因此预测在 [特定失败类型] 上相对 X 和最简方法出现 [可判别现象]`。

应能回答：
- 若把所有模块名称抹掉，计算是否依然不同？
- 是否有需要真实证明的独有预测？
- 能否用一个强简单基线直接实现同样功能？
- 关键附加假设是否强到失去实践意义？

裁决：`COLLISION_CONFIRMED / HIGH_RISK / DISTINCT_BUT_UNVERIFIED / PROVISIONALLY_DIFFERENTIATED / NOVELTY_UNVERIFIED`。请勿把“未检索到”表述为“已证明原创”。
