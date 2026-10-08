# academic-skills · 科研技能集

这是一个持续扩展的开源科研技能仓库，用来整理面向学术研究的 AI skills 与插件。当前收录的第一个项目是 [`paper-reading`](skills/paper-reading/)：一款以 **ChatGPT** 为主要使用场景、同时保留 Codex 等兼容路径的论文带读插件。后续科研技能会继续加入本仓库。

`academic-skills` 是项目集合，不是单一插件的别名；每个 skill/plugin 会在自己的目录中维护说明、脚本和版本信息。

## 当前项目：paper-reading · 论文带读

> **论文带读：面向 ChatGPT 网页聊天的图文论文学习工具。无需启动 Codex 编程任务，也无需另配 API Key 或部署本地大模型；从理解研究动机到掌握方法实现，带你一步步读懂论文。**

它的目标不是替读者快速生成一份“读完了”的摘要，而是帮助读者自己建立对问题、方法和证据的理解。

### 为什么使用论文带读

- **直接在 ChatGPT 对话中使用**：不必启动 Codex 编程任务，也不占用 Codex 专用任务额度；实际阅读仍受 ChatGPT 账号、模型、文件上传和工具使用限制。
- **无需单独配置 API Key 或部署模型**：使用 ChatGPT 当前可用的模型能力，不需要另建论文问答服务或承担单独的 API 调用配置。
- **先建立直觉，再逐层深入**：七站流程从研究动机、核心架构和样本运行开始；前三站结束后可以停下，也可以继续到数据协议、公式训练和实现细节。
- **结合论文中的真实图表学习**：优先依据论文原图与 caption 讲解；实际读取、裁图和在对话中显示图片取决于宿主提供的 PDF 与图像工具。仓库脚本不会自动识别所有 Figure/Table。
- **每一步由读者决定**：支持真实交互控件时可以点选下一站；否则回复“继续”即可，不会擅自跳过阶段。

### ChatGPT 网页端使用示例

以下截图展示了在 ChatGPT 网页端选择“论文带读”、上传论文 PDF 后生成论文分析卡，并进入第一站讲解的实际流程。最后一张中的连线图是帮助理解 Self-Attention 的示意图，**不是论文原图**。

**1. 在聊天界面选择论文带读**

![ChatGPT 网页插件选择器中的论文带读](docs/images/chatgpt-plugin-picker.png)

**2. 上传 PDF 后生成论文分析卡并展示论文架构图**

![论文带读分析 Attention Is All You Need 论文并展示 Transformer 架构图](docs/images/chatgpt-paper-reading-analysis.png)

**3. 进入第一站：从研究动机开始逐步讲解**

![论文带读第一站讲解 Transformer 的研究动机](docs/images/chatgpt-paper-reading-stage1.png)

**4. 用示意图说明 Self-Attention 如何建立位置间联系**

![用示意图解释 Transformer Self-Attention 的全局连接](docs/images/self-attention-reading-example.png)

插件提供七站式阅读流程和两个 PDF 图像辅助脚本：前三站建立直觉、理解架构并跟踪一个样本如何经过方法得到输出；之后可继续深入数据协议、数学与训练、精确执行，以及可选的实验审视与研究迁移。

阅读者可以在前三站结束后停下，也可以继续精读。每站的论文结论应区分原文报告、代码核验和合理推测；来源未提供的设置、数字和结果不得补造。七站顺序和阶段边界保留在 [`SKILL.md`](skills/paper-reading/SKILL.md)，本仓库文档更新不会改写框架。

| 层次 | 站点 | 内容 |
| --- | --- | --- |
| 泛读 | 1. 研究问题与动机 | 任务背景、已有方法局限、研究假设及论文信息核验 |
| 泛读 | 2. 核心方法与架构 | 对照原论文图梳理输入、模块、输出和设计选择 |
| 泛读，可在此停止 | 3. 方法如何工作 | 用一条样本说明从输入到输出的运行直觉 |
| 精读 | 4. 数据与实验协议 | 样本字段、预处理、标签权限、数据划分和评测协议 |
| 精读 | 5. 数学机制与训练 | 核心目标、公式、监督信号、参数冻结与更新 |
| 精读 | 6. 精确执行与双轮推演 | 执行顺序、状态与缓存，以及明确标注的玩具数值推演 |
| 可选 | 7. 实验、审稿与科研迁移 | 主结果、消融、负面证据、公平性、复现与研究启发 |

### 论文图像辅助脚本

- `crop_pdf_asset.py`：渲染用户指定的 PDF 页面，或按相对坐标裁剪指定区域。
- `make_figure_card.py`：在已核验的原图外添加标题和简短导读，并检查原图像素未被改动。
- 脚本不会自动识别 Figure/Table、判断图表含义或把图片插入聊天。论文理解、联网核验和对话讲解由 ChatGPT 或其他宿主平台及其可用工具完成。

v0.5.3 起，讲解论文图表时优先尝试在对话中真实显示已核验的裁图；只有用户需要保存文件或内嵌显示失败时才提供下载链接。`sandbox:/mnt/data/...` 是文件下载回退，不能称为预览，也不保证会在右侧栏打开。插件没有控制 ChatGPT 右侧图片预览栏的接口。

## 在 ChatGPT 中使用

### 个人账号：在 ChatGPT 网页中创建并安装

目前 `paper-reading` **尚未上架 ChatGPT 公共插件目录**，所以不能通过搜索插件名称直接一键安装。可以先在 ChatGPT 网页新建对话，把仓库链接和请求发给它，让 ChatGPT 识别项目并给出安装引导：

```text
https://github.com/zms618/academic-skills

帮我安装这个论文阅读插件，并引导我完成安装。
```

这条消息是安装引导的开始，**不代表插件已经安装**。普通聊天通常不能直接修改账号里的插件列表；如果它无法从链接读取仓库或没有安装权限，请按下面的 Plugin Creator 流程继续。需要源文件时，可下载并上传 [`SKILL.md`](https://raw.githubusercontent.com/zms618/academic-skills/main/skills/paper-reading/SKILL.md)。

1. 在浏览器打开 [ChatGPT 网页版](https://chatgpt.com/)，从侧边栏进入 **Plugins**，在插件目录中找到并安装 **Plugin Creator**（若该入口对你的账号和工作区开放）。
2. 开始新对话并提及 `@plugin-creator`。
3. 下载并上传本项目的 [`SKILL.md`](https://raw.githubusercontent.com/zms618/academic-skills/main/skills/paper-reading/SKILL.md)，或在创建对话中提供公开的 [GitHub 源码](https://github.com/zms618/academic-skills/tree/main/skills/paper-reading)。让 Plugin Creator 以这个文件作为主要行为规范，插件名称使用 **论文带读 / paper-reading**，保留七站顺序、阶段边界和读者确认，不要把它改成一次性摘要器。
4. 可将以下说明发给 Plugin Creator：

   > 请根据我附上的 `SKILL.md` 和这个公开仓库创建名为“论文带读（paper-reading）”的 ChatGPT 个人插件：https://github.com/zms618/academic-skills 。以 `skills/paper-reading/SKILL.md` 为核心规范，完整保留七站式论文阅读流程、泛读与精读边界、原文图表讲解、数学公式推导和用户确认机制。支持中文学术论文精读，每次只推进一个阶段；优先依据原论文图表、caption 和原始数据讲解，不虚构实验结论。不需要额外 API Key 或第三方服务。若当前工具不能直接安装到我的账号，请明确告诉我需要在界面完成的最后一步，不要声称已经安装。

5. 按 Plugin Creator 的提示检查并安装。ChatGPT 创建的本地插件可能自动安装而不显示单独的安装卡；安装后可在新对话的 **Plugins** 选择器中选择“论文带读”，或使用 `@` 提及它。
6. 上传论文 PDF，先试用下面的示例提示。确认回答确实按站推进、图表说明和原文相符，再继续精读。

主要阅读流程由 Skill 说明提供，不需要本地安装 Python。PDF 裁图脚本是可选辅助；只有在宿主提供可运行脚本的环境时才能执行，不能假设 ChatGPT 网页会直接运行仓库中的 Python 文件。

如果找不到 **Plugins** 或 **Plugin Creator**，通常表示当前账号、计划、地区或工作区策略没有开放相应功能；请查看工作区权限或使用当前账号可用的 Skills 入口。官方安装与可用范围说明见 [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt)。

### 工作区管理员：上传或从 GitHub 同步

部分工作区允许管理员在 **Admin Console → Plugins → Add** 上传受支持格式的插件 ZIP，也支持管理员从 GitHub 导入插件 marketplace。两种方式都需要相应管理员权限和兼容的插件包。普通 GitHub 仓库压缩包不一定就是 ChatGPT 可直接上传的插件 ZIP；本仓库目前主要提供源码和 Skill，不应把克隆/下载 ZIP 当成已验证的一键安装包。具体权限与路径以 [OpenAI 官方说明](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) 为准。

### 示例提示

在 ChatGPT 对话中选择“论文带读”并上传论文 PDF 后，可以这样开始：

> 帮我读这篇论文。先进入第一站，用通俗语言说明研究问题和动机，并核验官方代码开源状态。按七站框架先完成前三站泛读，每次只讲一站；优先结合论文原图。第三站结束时停下来问我是否进入第四站精读。

**用量说明：** 使用 ChatGPT 插件不需要为本项目单独部署论文问答模型或填写 OpenAI API Key；这不等于模型调用没有用量。阅读论文仍由 ChatGPT 中选用的模型处理，消息、文件上传及工具使用受账号计划、模型和工作区额度限制。插件不会绕过这些限制。可用额度会随计划和产品政策变化，参见 [ChatGPT 模型与使用限制](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt)。

之后可以回复“继续”，或问“详细解释 Figure 3”。也可以要求“从第五站开始讲公式”或“直接评估实验”。每站结束时，若当前宿主提供真实可用的后续提问控件，可以点击进入下一站；不支持时仍以“继续”作为确认，插件不会自动跳站。能否读取上传附件、联网核验代码和显示原图，取决于当前 ChatGPT 账号、所选模型、客户端与可用工具。

## 其他兼容方式

仓库同时保留 Codex 插件清单和通用插件元数据。若在支持 Codex 插件包的环境使用，可按该环境的插件流程加载仓库；若使用的平台只支持手动添加 Skill，可将 `skills/paper-reading/` 加入其 Skills 配置，并保留 `scripts/` 目录。不同宿主的安装入口和本地文件工具支持并不相同。

## 本地运行 PDF 脚本

只有在需要运行图像脚本时才需安装 Python 依赖。需要 Python 3.10 或更新版本：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

PDF 图像脚本依赖 PyMuPDF 和 Pillow。图文卡需要系统中有可读取的中日韩字体，也可用 `--font` 指定字体；仓库不分发字体文件。

页码从 1 开始。先检查整页和论文 caption，再按相对坐标 `left top right bottom`（0–1）裁切：

```bash
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --output output/page-3.png
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --rect 0.49 0.12 0.95 0.49 --dpi 220 --output output/figure-3.png
python skills/paper-reading/scripts/make_figure_card.py output/figure-3.png --output output/figure-3-card.png --title "Figure 3 · 模型总体流程" --intro "请先观察输入经过哪些模块，再沿箭头追踪最终输出。"
```

裁图工具只处理用户指定页面和区域，不会自动定位图表。图文卡只保证单张图片内部的导读和原图顺序；聊天客户端仍可能调整图片在回复中的位置。

## 目录结构

```text
academic-skills/
├── .codex-plugin/plugin.json        # Codex 插件元数据
├── plugin.json                      # 通用插件清单
├── skills/paper-reading/
│   ├── SKILL.md                     # 七站阅读框架与教学规范
│   └── scripts/                     # 用户指定的 PDF 图像辅助脚本
├── docs/images/                     # 阅读效果示例图
├── tests/                           # 清单、阅读框架与脚本测试
├── .github/workflows/check.yml
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 版本与检查

当前插件版本为 **v0.5.3**。版本记录见 [`CHANGELOG.md`](CHANGELOG.md)。本地检查：

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

GitHub Actions 会在 push 和 pull request 时运行检查。

## 能力边界与隐私

- 本仓库不是独立论文阅读应用，不包含 OCR 服务、论文问答模型、自动图表定位器或聊天客户端。
- Skill 提供 AI 助手的阅读流程与行为规范；论文解析、网络检索、图片展示和跨轮上下文依赖 ChatGPT 或其他宿主平台及其工具。
- Python 脚本只执行本地 PDF 页面渲染、用户指定区域裁剪和图文卡生成；它们不判断论文内容是否正确，也不替代人工核对图表和 caption。
- 不要提交未获分发许可的论文 PDF、数据集、访问密钥、令牌、私人聊天或个人文件。第三方依赖遵循各自的许可证。
- `sandbox:` 文件链接可能被宿主显示为下载附件；是否提供内嵌预览或点击放大由客户端决定。不要把下载入口宣传为侧栏预览。

## License

本仓库采用 MIT License，详见 [`LICENSE`](LICENSE)。第三方依赖仍遵循各自许可证。

---

### English

**academic-skills** is an extensible open-source collection for research-oriented AI skills and plugins. Its first project, [`paper-reading`](skills/paper-reading/), is designed primarily for **ChatGPT**, while retaining compatibility paths for Codex and other hosts. More research skills and plugins will be added over time.

`paper-reading` provides a seven-stage workflow: three intuitive overview stages, three technical deep-reading stages, and an optional evidence and research-transfer stage. Readers can stop after the overview or continue into details. It also includes two local PDF image utilities. The framework in `skills/paper-reading/SKILL.md` is preserved.

The screenshot above is an example of a Transformer explanation; its attention diagram is an explanatory schematic, not an original figure from the paper. Since v0.5.3, the workflow prefers displaying verified paper crops inline. A `sandbox:` link is only a download fallback and does not guarantee a right-side preview. One-click next-stage controls are used only when the host actually supports them; otherwise readers can explicitly reply “continue.”

For ChatGPT Web, a convenient first step is to paste `https://github.com/zms618/academic-skills` into a new chat and ask for installation help. This starts the guidance; it does not install the plugin by itself. Continue with Plugin Creator and confirm installation in the interface. If the source cannot be read from the link, provide [`SKILL.md`](https://raw.githubusercontent.com/zms618/academic-skills/main/skills/paper-reading/SKILL.md). The repository is not currently listed in ChatGPT’s public plugin directory. Plugin access depends on account, plan, region, workspace, role, and client. A skills-only plugin does not require an external app connection or a separately configured OpenAI API key, but ChatGPT model, file, and tool usage remains subject to the account’s applicable limits. See the [official plugin guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) and [ChatGPT model limits](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt).

The repository is not a standalone paper-reading application. PDF interpretation, web research, image display, and conversation continuity depend on the host platform and its tools. The Python scripts only render or crop user-selected PDF regions and create guide cards that preserve the original image pixels.

See the Chinese documentation above for detailed workflow, setup, examples, limitations, and release notes.
