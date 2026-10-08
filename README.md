# academic-skills · 科研技能集

这是一个持续扩展的开源科研技能仓库，用来整理面向学术研究的 AI skills 与插件。当前收录的第一个项目是 [`paper-reading`](skills/paper-reading/)：一款以 **ChatGPT** 为主要使用场景、同时保留 Codex 等兼容路径的论文带读插件。后续科研技能会继续加入本仓库。

`academic-skills` 是项目集合，不是单一插件的别名；每个 skill/plugin 会在自己的目录中维护说明、脚本和版本信息。

## 当前项目：paper-reading · 论文带读

**核心目标：在 ChatGPT 里带着读者逐步读懂论文。** 插件提供七站式阅读流程和两个 PDF 图像辅助脚本：前三站建立直觉、理解架构并跟踪一个样本如何经过方法得到输出；之后可继续深入数据协议、数学与训练、精确执行，以及可选的实验审视与研究迁移。

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

## 在 ChatGPT 中使用

本项目优先面向 ChatGPT。可以在 ChatGPT 中通过 **Plugins → Plugin Creator** 创建自己的插件，并将本仓库的 `skills/paper-reading/SKILL.md`、配套 `scripts/` 和 README 作为构建与测试依据；创建后先用一篇论文验证流程，再安装或分享。只含 Skill 的插件不需要连接外部服务。当前 GitHub 仓库是源码与发布信息来源；它本身不代表该插件已上架 ChatGPT 公共目录，也不保证每个账号都能看到相同入口。

组织工作区若使用管理员管理的插件，可以由有权限的管理员上传支持的插件 ZIP，或配置从 GitHub 导入插件 marketplace。具体入口和可用方式取决于账号计划、地区、工作区策略、角色和客户端；ChatGPT 官方说明见[插件说明](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt)。

**用量说明：** 使用 ChatGPT 插件不需要为本项目单独部署论文问答模型或填写 OpenAI API Key；这不等于模型调用没有用量。阅读论文仍由 ChatGPT 中选用的模型处理，消息、文件上传及工具使用受账号计划、模型和工作区额度限制。插件不会绕过这些限制。可用额度会随计划和产品政策变化，参见 [ChatGPT 模型与使用限制](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt)。

### 示例提示

在 ChatGPT 对话中安装或选择插件并上传论文 PDF 后，可以这样开始：

> 帮我读这篇论文。先进入第一站，用通俗语言说明研究问题和动机，并核验官方代码开源状态。按七站框架先完成前三站泛读，每次只讲一站；优先结合论文原图。第三站结束时停下来问我是否进入第四站精读。

之后可以回复“继续”，或问“详细解释 Figure 3”。也可以要求“从第五站开始讲公式”或“直接评估实验”。能否读取上传附件、联网核验代码和显示原图，取决于当前 ChatGPT 账号、所选模型、客户端与可用工具。

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
├── tests/                           # 清单、阅读框架与脚本测试
├── .github/workflows/check.yml
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 版本与检查

当前插件版本为 **v0.5.0**。版本记录见 [`CHANGELOG.md`](CHANGELOG.md)。本地检查：

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

## License

本仓库采用 MIT License，详见 [`LICENSE`](LICENSE)。第三方依赖仍遵循各自许可证。

---

### English

**academic-skills** is an extensible open-source collection for research-oriented AI skills and plugins. Its first project, [`paper-reading`](skills/paper-reading/), is designed primarily for **ChatGPT**, while retaining compatibility paths for Codex and other hosts. More research skills and plugins will be added over time.

`paper-reading` provides a seven-stage workflow: three intuitive overview stages, three technical deep-reading stages, and an optional evidence and research-transfer stage. Readers can stop after the overview or continue into details. It also includes two local PDF image utilities. The framework in `skills/paper-reading/SKILL.md` is preserved.

In ChatGPT, use Plugin Creator to build a plugin from the skill source and its supporting scripts, then test it with a paper before installing or sharing it. The public GitHub repository is the source for the project; it does not mean the plugin is listed in ChatGPT’s public directory or available to every account. Plugin access depends on account, plan, region, workspace, role, and client. A skills-only plugin does not require an external app connection or a separately configured OpenAI API key, but ChatGPT model, file, and tool usage remains subject to the account’s applicable limits. See the [official plugin guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) and [ChatGPT model limits](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt).

The repository is not a standalone paper-reading application. PDF interpretation, web research, image display, and conversation continuity depend on the host platform and its tools. The Python scripts only render or crop user-selected PDF regions and create guide cards that preserve the original image pixels.

See the Chinese documentation above for detailed workflow, setup, examples, limitations, and release notes.
