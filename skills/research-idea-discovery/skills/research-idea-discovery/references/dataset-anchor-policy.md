# D0 — IDEA-FIRST Dataset Discovery and Audit

## 核心职责与顺序

**先找科学问题与 Idea Seed，然后由插件主动检索数据并核查。用户无须提供经过核实的数据集。** 数据集可行性是**候选晋级门槛**，不是 Idea Seed 生成的门槛。用户资源约束保持：只允许已有合法可用数据 `EXISTING` 或从该父数据低成本生成 `DERIVED_FROM_EXISTING`；不得从零开展大规模数据采集、昂贵人工标注或默认私有数据可用。

顺序：`已有工作/未解释现象 → IDEA_SEED(输入/标签/验证需求) → 插件 DATA_SEARCH → D0 Dataset Audit → G0 Full Feasibility → 正式研究候选`。

## 主动搜索步骤（由插件执行，不能要求用户先找）

1. 对 Idea Seed 列出具体可观测需求：模态、传感器/图像、时间分辨率、标签、train/test protocol、必要干预、评测指标及最小 E0。先问「需要什么数据才能证伪这个假设」，不是先问用户有哪个数据集。
2. 沿 Idea 所依赖的论文、最危险近邻论文、相关 benchmark 与公开代码找其使用的数据集；扩展查官方数据网页、开发者仓库、数据开放平台、Hugging Face、OpenML、Zenodo 等领域合适来源。推荐每条种子搜索 2–5 个潜在数据源；若搜索不足，明确覆盖限制。
3. 对每个候选检索并记录 `dataset_name / source_url / actual_access / license / fields_and_labels / split / metric / baseline / code / fit_to_E0`；官方 metadata、预览、下载样本和已成功取文件属于不同访问证据级别，不得混淆。
4. 检查输入/标签实际覆盖；若标签缺失，评估能否使用现成标签、合法自动变换或用户资源内的少量加工。单纯能够下载，不意味着该数据能验证科学假设。
5. 如需衍生：记录父集合访问证据、转换步骤、标注来源、衍生许可证、预算、先划分后增强防止泄漏、开放代码和可重现路径。
6. 找不到合格数据则给 `NO_DATA_PATH / PIVOT_OR_STOP`，优先缩小问题、转换验证目标或选择另一条 Idea；**不能把继续找数据的责任交给用户**，也不能冒险推荐不具备验证条件的成熟 Idea。

## 来源类型与审核状态

- `EXISTING`: 数据的真实官网与获取路径、可用标签/模态/划分、授权、合适 baseline/评测均有具体证据。
- `DERIVED_FROM_EXISTING`: 父数据合法可取得；变换/重划分/已有标签映射/合成偏移在资源预算内且测量仍有效，排除泄漏。
- `SOURCED_BUT_UNVERIFIED`: 找到官方或论文链接，但未检查下载、授权或必要字段。只能作为需要核实的候选数据集，**不算 D0 通过**。
- `BLOCKED`: 获取、字段、权限、预算或衍生条件不满足，淘汰该数据路径。

`dataset_anchor.py` 只验证数据卡字段结构，不执行真实下载和许可证法律判断；`dataset_discovery.py` 仅检索公开元数据线索。ChatGPT 使用可用 web/file 工具核查来源；如果工具不能访问，明确 `NOT_CHECKED`，不能称 `VERIFIED`。D0/G0 未证实之前一律不得宣称成熟论文候选。

## 数据适配问题

- 数据有无关键输入、标注字段以及可观测偏移或实际实验干预？
- 有没有可靠 train/val/test protocol，可否避免原样本跨 split 泄漏？
- 可用代码是否与同一版本的样本、标注、指标、预训练权重兼容？
- 该数据能否**区分新机制与最简单对手**，而不只是训练一个漂亮网络？
- 需要新标注/私有传感器/数千 GPU 时，该 Idea 是否应缩小或转向？

## 每条 Idea Seed 的数据搜寻结果

`idea_id | required_data | dataset_candidates[链接/证据状态/字段/许可/成本/fit] | best_existing_or_derived_path | D0 verdict | G0 blockers | next action`。

**不能因为未发现数据而禁止提出构想；也不能因为构想有趣而忽略没有可行数据的事实。**
