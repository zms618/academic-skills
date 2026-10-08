# Agent contracts — 从角色分离到真实多模型代理

## 实际能力边界

本插件提供六个相互独立的**角色任务协议**，不是五个已经部署的模型。若宿主支持并行独立代理/多模型工具，分别调用并保留可核实的 run_id、模型标识、引用和任务快照；否则在单一会话按先后顺序执行**角色隔离评审**，明确标注 `ROLE_SIMULATED` 而不是 `INDEPENDENT_MULTI_MODEL`。不允许伪造投票和模型共识。

### 角色与交接数据

| 角色 | 唯一输入 | 输出对象 | 禁止事项 |
|---|---|---|---|
| Scout | Research Brief + 检索源 | `evidence-map.json`（文献问题地图）＋接收 Idea Seed 后输出 `dataset-search-ledger.json` 和 `dataset-anchor.json`（插件检索的数据/访问/代码/评价） | 不能给出“已证明新颖”或“未核实数据可获取” |
| Hypothesis Lab | evidence map + 反例/用户 Idea；**允许无数据集先生成 IDEA_SEED**；冻结时需 D0/G0 和 M1，后进入 N→L→M2→S | `ideas.json` (H0/H1、机制、独有预测、kill signal) | 不能美化证据缺口 |
| Motivation & Story Auditor | 已通过 D0/G0 的问题证据；通过近邻审计、机制逻辑与动机复审的候选用于 S | `motivation-initial.json` + `mechanism-logic.json` + `motivation-recheck.json` + `story-card.json` + `review-rounds.json` | 不能造故事、用措辞代替真实动机与实验 |
| Scoop Auditor | 冻结的 idea + 检索日志 | `collision-matrix.json` (每项六轴对比、未核验处) | 不能修改候选 Idea 以逃避撞车 |
| Skeptical Reviewer | idea + 先例 + **Feasibility Card** + 计划，不含作者辩护 | `review.json` (拒稿点、反例、建议) | 不能把假设当实验事实 |
| Pilot Designer | 审核后的冻结 idea + **通过 D0 的既有数据/父数据与 G0 的可用资源** | `pilot-plan.json` (E0-E4、预算、Go/No-Go) | 不能以编造性能作通过理由 |

### 隔离规则

0. Idea Seeds 首先由 Hypothesis Lab 生成，随后 Scout **自己搜集数据集**并执行 D0；G0 完整可行性与 M1 动机初审是正式查新候选的先决条件；`CONDITIONALLY_FEASIBLE`/`UNKNOWN` 时先转 Scout 核查，`INFEASIBLE` 时 STOP/RESCOPE，不允许 Hypothesis Lab 发布正式候选或 Reviewer 用高创新分覆盖问题。
1. 为每次候选 Idea 建立 `idea_id` 和 `revision`; 新颖性审计前冻结内容。
2. Auditor 先给机制级重合与论文证据，之后 Hypothesis Lab 才能提出 rebuttal；Reviewer 在看到作者辩护之前先生成自己的意见。
3. 如同一模型依次扮演角色，输出显式标识 `role_simulated=true`。多角色提示词并不形成统计独立性。
4. 质疑必须指明可检验的差异、文献位置或待查询内容；拒绝“因为是 CCF-A 所以创新性 9/10”。
5. 存储 `role, inputs_digest, time, model_if_known, tool_trace, sources, verdict`；无法取得则写 `UNKNOWN`。
6. 未授权的外部付费模型 API 绝不自动调用。

Scout 的 `dataset-anchor.json` 来源于其主动检索，**不得要求用户先提供已核实数据**；D0 不通过时可以保留探索性 Idea Seed，但不得移交为正式投稿候选。

流程以 `references/two-loop-review-protocol.md` 为准；N 和 M2 不能跳过；角色独立不代表模型独立。

## v2.7 Evidence execution contract

Scout 必须区别索引线索与实际读取样本，记录 source URL/许可/字段/样本访问证据。Reviewer 必须输出同一 idea_id+revision 的审核记录，并明确 unresolved critical objections。Pilot Designer 只产出 PLANNED，除非真实运行并保存输出日志和指标。Scoop 需要覆盖四类查询及所读章节；无法验证则保留 UNVERIFIED。所有角色不得用填字段/标注 `ready: true` 替代独立核查。
