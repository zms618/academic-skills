# 检索工具连接协议

## 优先级

1. 用户已上传/Project 文献，先逐篇读其 Method、图表、Appendix、Related Work。
2. ChatGPT 中若有原生 Web 搜索，检索公开论文/会议官网并附公开来源。工具检索是当前对话发生的，不把结果当插件自带持续数据服务。
3. 如果处于支持执行的**本地项目**且用户允许联网，可用本插件 `scripts/literature_search.py` 调 Crossref + OpenAlex。记录 API 报错和用量；网络不足时不要用模拟样本假装在线结果。
4. arXiv/DBLP/OpenReview/Semantic Scholar、PatSnap 等作为**外部可选连接源**，只有提供验证过的客户端/鉴权后才宣称已连接。

## 查询矩阵

`Q_problem`：任务 + 失败条件 + benchmark/protocol。
`Q_mechanism`：粒度、核心运算、路由/校准/一致性/后验更新的功能等价词。
`Q_objective`：实际优化目标、监督信号、更新时机。
`Q_cross`：不同数据形态、邻近学科、同一计算操作。

至少查看：最新相关/经典先例/近期预印本/引用链/强基线；仅返回摘要者的证据等级最多 E1。对每项结果存查询、title、DOI、published date、URL、索引源、是否读全文、来源置信状态。必须区分：检索“索引库” ≠ 检索“所有论文”。

## CLI 使用示例（不是 ChatGPT 云端自动功能）

```
python scripts/literature_search.py --query "instance selective test time adaptation" --limit 12 --out literature.json
python scripts/workflow.py init --project ./my-study --domain "robotics" --goal "ICRA"
python scripts/workflow.py audit --project ./my-study --idea ./idea.json
```

OpenAlex works endpoint: https://api.openalex.org/works?search=...
Crossref works endpoint: https://api.crossref.org/works?query.bibliographic=...
官方文档：https://help.openalex.org/api/ 及 https://www.crossref.org/documentation/retrieve-metadata/rest-api/ 。两者均为元数据索引，不证明方法独特性。OpenAlex 可能要求计费或 API key，检查响应并尊重额度。

## Idea-First 数据集发现（v2.4）

对每一条 Idea Seed，从论文中寻找真实 benchmark，并使用宿主 Web 查询官方数据页面、许可、字段、标签、split、baseline 与指标；**不要求用户提供数据集**。可运行网络 CLI 时：

```bash
python scripts/dataset_discovery.py --query "cross-modal shift benchmark" --out ./work/dataset-leads.json
```

该脚本检索 Hugging Face 和 Zenodo 目录**元数据**，并不下载、核查 license、验证数据字段或保证可用于实验。对论文专门数据集要进一步检查作者/会议页面；不能使用 API 结果代替访问授权。找不到就为该 Seed 给出 NO_DATA_PATH，尝试另一个假设或缩小任务。
