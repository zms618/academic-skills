# 可配置范围与启动协议

## 使用原则

研究方向由用户决定，不是插件配置常量。**用户无需提供数据集，插件在生成 Idea 种子后自己检索合适的现有/衍生数据集并核验。**CCF-A 是可选目标之一，而不是科学领域或通用论文质量定义。

### 1. 用户明确给方向

`domain="三维视觉"`, `goal="CVPR 2027"`, `focus="遮挡下跨场景多视图匹配"`：直接工作；不得误切回原用户过去关心的领域。

### 2. 用户只给论文集合

根据上传论文提炼 2–4 个交汇的问题簇，报告覆盖偏差，不将论文作者当前方向当唯一可行方向。

### 3. 用户明确要求通用/跨方向

形成研究机会矩阵：`领域/目标问题 | 可核实失效证据 | 现有强基线 | 可证伪假设 | 资源门槛 | 先例覆盖缺口`。先选问题簇，再对首选深查。不宣称已经完成整个领域的全面系统综述。

### 4. 用户未指定任何领域

如果问的是“怎么使用”则示范流程；如果要求“现在找 Idea”且没有任何主题，可问一个核心问题（方向由用户选还是全领域探索），不弹出冗长的配置表。用户授权自行选择时，按已有证据、研究价值和资源假设先选再推进。

### 5. 会议目标

会议、期刊、行业项目、学位论文都可作为目标。只有用户明确要求且最新官方信息可核实时才使用特定届次的真实 track/审稿条件。CCF-A 会议名单/评级若未核验不能先行断言。不同研究类别的方法、理论、系统、资源、benchmark 论文不套同一个评判模板。

## 运行模式

`DISCOVER`：找有证据的研究问题→想法；`OPEN_EXPLORE`：跨方向选问题；`VALIDATE`：查新颖性；`REFINE`：优化机制；`PIVOT`：撞车或失败后重构；`COMPARE`：多选一。

`QUICK`：20% 深度早期排雷；`STANDARD`：聚焦一个足够深入的 idea card；`DEEP`：可复查 evidence ledger 与完整实验设计。以上百分比不表示真实工具成本或检索覆盖率。

## Research Brief 轻量模板

```yaml
domain: "由用户指定或 OPEN"
focus: "一句话研究任务或留空"
goal: "CCF-A / 具体会议年份 / 期刊 / 其他 / 未指定"
contribution_type: AUTO
mode: DISCOVER
depth: STANDARD
seed_papers: []
constraints: {compute: unknown, data: "agent_must_discover_existing_or_low_cost_derived", time: unknown}
forbidden_assumptions: []
verified_sources: []
open_questions: []
```

不强制要求用户按模板填写；通常直接从自然语言提取即可。
