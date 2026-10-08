# 迭代研究状态机与停止条件（Idea First, Data Search by Agent）

1. **SCOPE**: 用户指定方向或 OPEN；只记录资源边界，不要求用户提供数据集。
2. **SEARCH**: 阅读已有论文/文献，寻找异常、矛盾、未解释失效及隐藏假设。
3. **EXPLAIN**: 形成可证伪命题和反对解释，标注已观察与合理猜测。
4. **DIVERGE / IDEA_SEED**: 产生 2–4 个不同科学命题的候选种子，写清所需数据字段、对照实验、kill signal；**允许 D0 尚未核实**。
5. **DATA_SEARCH**: 插件为各 Seed 搜集和检查 2–5 个公开/授权数据集/可衍生父数据、实验代码与公开评价协议；用户不承担搜索责任。
6. **DATA_ANCHOR (D0)**: 判断哪些数据真实适配且可使用，哪些仅为网页/元数据线索；没有可行路径的 Seed 不再推进，改构或淘汰。
7. **FEASIBILITY (G0)**: 针对匹配的数据路径查 baseline、GPU/设备、时间预算、合规、最小 E0 实验，记录 CONDITIONAL/UNKNOWN/BLOCKED。
8. **MOTIVATION_INITIAL (M1)**: 可行性后先审问题的真实性、重要性与强 Baseline 局限，检索近邻后要复核，不能预先宣称首创。
9. **FREEZE & SCOOP (N)**: 冻结 M1 存活的候选 Idea ID/revision，检索强近邻并逐机制查重。
10. **MECHANISM_LOGIC (L)**: 根因→机制→独特预测→最简 Rival→必要性消融；不能直接跳到文案。
11. **MOTIVATION_RECHECK (M2)**: 依据近邻已解决部分，重新审查原动机和剩余研究空白；动机不成立要撤销。
12. **NARRATIVE (S)**: 先证据链再表达；故事线只暂时成立，待实验回填。M/N/R 冷读三类质疑不能替代 M1/N/L/M2。
13. **REVIEW**: 审稿人最强拒稿理由与可判别反证，必要时返回上游重新构思。
14. **PILOT**: 有授权后执行 E0–E4，未执行标 PLANNED；失败应改变前述假设、机制和故事。
15. **UPDATE**: 保存被否定想法、新数据与近邻审查；以新证据重启合理节点，不反复复活已撞车机制。

**迭代边界**：默认最多三次新增证据/机制的实质修订（可以一轮完成）；若无新证据停止故事重写。无可行数据/资源/近邻高度重合可返回 Seed 再尝试其他方案。无合格候选输出 0 个正式 Idea。仅有真实独立代理和计算运行时才声称已并行/自动执行。

## Deep Research 证据升级分支（不绕过科学硬门）

若 `NO_DEFENSIBLE_IDEA_FOUND / COVERAGE_GAP / DATA_GAP / MOTIVATION_CONFLICT / STAGNATION`，或者用户主动请求，转 `RESEARCH_HANDOFF_PENDING`：保存截止日、已查文献、负面候选、关键未知、研究资源边界，输出由该记录生成的完整复制提示词。手工 Deep Research 报告返回后置 `RESEARCH_REPORT_IMPORTED_UNVERIFIED`，以 source-by-source verification 增量合并，恢复最早受影响阶段；不能因为外部报告动听就跳过 D0/G0/N/L。升级无需等待固定轮次，优先针对已确定证据缺口。
