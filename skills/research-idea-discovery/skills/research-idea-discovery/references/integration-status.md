# 上游项目整合清单 / 许可证和能力边界

截至 2026-10-08。外部仓库随时可能变化；以下只表示核查到的公开能力和本插件对应的**独立新实现**，不意味着复制了仓库全部代码。

| 上游项目 | 可见工作流/接口 | 本插件现状 | 不具备或需外部部署 |
|---|---|---|---|
| microsoft/ResearchStudio / ResearchStudio-Idea (MIT) | Paper-Search, Scoop-Check, Idea-Spark; arXiv/DBLP/OpenAlex/OpenReview/S2/Crossref | 检索和查重角色 + 本地 Crossref/OpenAlex CLI；原创实现 | 未复制 1,947 篇论文训练语料、完整 pattern cards 和 LaTeX renderer |
| mikubaka88/CCFA-Skills (MIT) | Idea Optimizer/Reviewer、Experiment Designer、literature Searcher | 优化器/批判者/实验规划独立角色协议 | 未搬运全部 17 skills 和专用报告绘制代码 |
| ozrwayne/rw-research-skill (Apache-2.0) | 研究问题、来源证据、冲突/异常、交接状态 | Evidence ledger + 停止/修复标记 | 未移植其全部知识原子、公理和 21 skills |
| wanshuiyin/Auto-claude-code-research-in-sleep (许可证待逐项核对) | idea-discovery, novelty-check, experiment-queue, review-loop | 迭代状态机、实验结果反馈桥接 | 无自动多模型 API、云 GPU 或通知后台 |
| Robin9989Law/innovation-proposition-hunting | 可验证命题/边界与审计：仓库本次无法确认全文 | 保留自主实现的命题冻结、证据状态 | 未导入代码；无许可核验 |
| CliffKai/skillhub | innovation-validator: 本次无法确认具体源文件 | 质疑/对立解释协议 | 未导入代码；无外部模型接入 |
| patsnap/skills (具体子项许可与服务认证需核实) | innovation-radar 使用 PatSnap MCP 专利检索 | 引入问题—方案—效果提炼作为可选视角 | 未连智慧芽账号/PatSnap 专利 API，不主张专利查新功能 |
| fengmo11/awesome-paper-research-skills | 工具目录/入口 | 用于审计外部工具需求 | 不是执行型引擎 |
| microsoft/ai_night_scientist | verl+GRPO/Qwen3-8B 构成训练型系统 | 跨范式发散与收敛的行为准则 | 不能在 Skill 内移植训练后权重、CUDA/RL 训练或全部依赖 |
| TashanGKD/tashan-research-skills / Scispark | 分阶段 fact→hypothesis→idea→mechanism review | evidence map/机制评估与固定交接 | 未调用外部 SciSpark 服务/脚本 |
| Elsevier LeapSpace | 商业外部服务 | 不自动使用 | 无服务凭据、许可和正式接口集成 |
| 重庆医科大学/SCNET agent | 网页 agent 服务，接口未核验 | 无 | 无授权 API 或接入点 |

**版权**：本插件新增内容和脚本均为独立编写；保留上游链接、作者和许可证名称用于方法来源说明。不得把第三方 Git 仓库当成本插件的可随意复制素材。若日后实际拷贝上游实现，需附原 LICENSE、署名、修改记录并核对每个子目录许可和依赖。

## 联网功能现状

- `scripts/literature_search.py` 在**允许命令执行且网络可用的本地环境**中调用公开 Crossref/OpenAlex API；API 使用策略与费用以官方文档为准；**ChatGPT 聊天内部不自动运行**。
- `scripts/workflow.py` 完全离线可运行，保留 stage/审计门槛与证据包校验；不替代语义创新判断。
- `scripts/pilot_bridge.py` 仅在本地明确 `--execute` 时运行指定程序，保留日志与哈希，不会后台自动训练模型。
- 当前 ChatGPT 插件**未绑定远程 MCP 服务器**，没有可独立执行的 cloud runner，也没有自动连接 GitHub/PatSnap/GPU 资源的权限。真实多模型代理需要用户授权具体服务后再部署。

## 上游链接

https://github.com/microsoft/ResearchStudio ; https://github.com/mikubaka88/CCFA-Skills ; https://github.com/ozrwayne/rw-research-skill ; https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep ; https://github.com/patsnap/skills ; https://github.com/fengmo11/awesome-paper-research-skills ; https://github.com/microsoft/ai_night_scientist ; https://github.com/TashanGKD/tashan-research-skills ; https://github.com/Robin9989Law/innovation-proposition-hunting ; https://github.com/CliffKai/skillhub
