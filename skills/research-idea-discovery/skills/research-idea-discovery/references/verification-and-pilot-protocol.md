# v2.7 实证链：数据真实访问、审稿证据、Pilot 反馈和科研回归测试

## 最重要的限制

在 ChatGPT 纯 Skill 环境，未真实下载/打开数据或运行实验的情况下，**不能**说数据可访问已验证、代码已复现、Pilot 已执行。附带 Python 脚本只有宿主具备本地执行权限时才能运行。由 Agent 自主寻找数据、官方来源、许可和可用子集，绝不能让用户提前准备好数据集。

## 数据核验的三级证据

1. `CATALOG_LEAD`：平台索引或论文提到数据集。仅候选线索，不能通过 D0。
2. `OFFICIAL_PAGE_CHECKED`：官方数据页、许可、字段说明、分割方案和可获取路径已由检索逐一核查，但尚未读取数据字节。标 `ACCESS_NOT_EXECUTED`，不得声称数据已获取。
3. `LOCAL_SAMPLE_CHECKED_REQUIRES_HUMAN_SOURCE_REVIEW`：`scripts/dataset_access.py` 读取已有本地 CSV/JSON/JSONL 小样本，实际解析出必需字段，并核对本地许可文本引用。记录 SHA256、文件大小和明确限界。**这也不是完整数据集可复现或法律授权证明。**

测试数据中存在用户自报 `access_status: DOWNLOADED`，不能单凭此判可行。无效网页、HTML 假下载、空样本、缺必要标签都不得通过样本证据关卡；遇到无权限/大文件/不能下载时保留 `CONDITIONAL` 并提供成本可控的替代路径，绝不可绕过审核。

## 执行证据不可跳跃

- `S` 故事审查可产生 `PROVISIONAL_STORY`，只是尚待实验验证的可证伪论证。
- `REVIEW` 阶段写 `review_card.json`（idea_id, revision, objections, verdict 等）。`scripts/execution_evidence.py` 可以做结构记录检查。若未解决关键拒稿点，**不能**以良好语言包装后进入 Pilot。
- `PILOT_PLANNED`：只是一份实验设计，未运行，允许用户审阅，不允许写 `PILOT_EXECUTED`。
- `PILOT` 的本地执行只能由已授权 `scripts/pilot_bridge.py --execute` 或其他能够核验的真实执行日志记录；dry run 不是运行。
- `UPDATE` 之前必须具备 `pilot_run.json` 与真实日志（成功时另需指标文件；失败时保留错误日志）；成功启动进程不是实验证明。每次阶段推进重新核验来源文件，而非信任可人工修改的 `ready: true` 字段。
- 若简单 baseline 的效果 >= 新机制：必须撤销“复杂机制不可替代”的主张，将 `requires_reaudit=true`，重审 L → M2 → S。失败运行也属于负面证据，不能扔掉。

## 证据覆盖/复现风险

- 四类检索：同问题、同机制、同目标、跨任务功能等价。`scripts/literature_coverage.py` 记录各类实际查询、日期、已读 Method/Appendix 的准确位置和缺口，任何程序报告都 **不等于**“证明全世界没有同类论文”。
- 用 `scripts/idea_ledger.py` 保存重复/否定候选及重启需要的证据；当前为本地 JSONL，不是 ChatGPT 跨会话数据库。无文件存储时在对话中保留精简清单。
- v2.7 的反例测试覆盖：无效数据地址、HTML 冒充数据、无实际样本、缺模态/标签、伪造 `ready`、无审稿日志、Dry Run、无指标、简易 baseline 等效及失败 Pilot。测试结果只代表*程序门禁*，不代表科学判断正确。

## 用户可见输出

每条 Idea 至少报告六种分离状态：`文献核查/样本真实访问/许可与协议/算力可行性/审稿结果/真实 Pilot`。若任一关键步骤未完成，结论使用 `UNVERIFIED`/`CONDITIONALLY_FEASIBLE`/`PILOT_PLANNED`，而非成熟顶会级 Idea。

如没有真正可推荐的候选，交给 Deep Research **具体的证据缺口**，保留 rejected ledger，回来后按新增证据重开相关节点。

## 检索更新及前提变更后强制回退

修订已记录的样本文件/字段要求、近邻查询记录或 Review 结论时，原下游实验准备与动机/故事审核不得继续自动沿用。`workflow.py` 在检测到相应输入变化时使相关记录失效并回退到受影响阶段。若 ChatGPT 宿主没有本地状态文件，必须在回复中显式声明哪些历史判断已经过期。
