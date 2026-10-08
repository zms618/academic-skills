# paper-reading · 论文带读

`paper-reading` 是 [`academic-skills`](https://github.com/zms618/academic-skills) 仓库中的一个 Codex 风格研究论文阅读插件。它提供一套面向 AI 助手的七站式教学规范，以及两个可独立运行的 PDF 图像辅助脚本。

> **核心思路：先泛读看懂方法，再按需精读。** 前三站帮助读者理解研究问题、核心架构和一条样本如何经过方法得到输出；第四至第六站深入数据、数学训练和精确执行；第七站按需审视实验与研究价值。七站顺序和阶段边界见 [`SKILL.md`](skills/paper-reading/SKILL.md)，本次开源只调整插件名称和发布文档，不改动该阅读框架。

## 功能概览

| 阅读层次 | 站点 | 重点 |
| --- | --- | --- |
| **泛读** | 1. 研究问题与动机 | 任务背景、旧方法局限、研究假设和论文信息核验 |
| **泛读** | 2. 核心方法与架构 | 对照原论文架构图，梳理输入、模块、输出和设计选择 |
| **泛读，可在此停止** | 3. 方法如何工作 | 用一条样本讲清从输入到输出的运行直觉，不先堆公式 |
| **精读** | 4. 数据与实验协议 | 真实样本字段、预处理、标签权限、划分和评测协议 |
| **精读** | 5. 数学机制与训练 | 解释核心目标、公式、监督信号以及参数冻结和更新 |
| **精读** | 6. 精确执行与双轮推演 | 追踪执行顺序、状态与缓存，并用明确标注的玩具数值推演 |
| **可选** | 7. 实验、审稿与科研迁移 | 检查主结果、消融、负面证据、公平性、复现和研究启发 |

每站由读者决定是否继续。结论需要区分论文明确报告、代码核验和合理推测；论文没有提供的数字、维度、设置或结果不得补造。

### 原图与 PDF 工具

- `crop_pdf_asset.py`：按 PDF 页码渲染整页，或按页面相对坐标裁剪指定区域。
- `make_figure_card.py`：在已核验的原始图像外增加标题和简短导读，并检查卡片中的原图像素区域与输入完全相同。
- AI 助手的论文理解、图表定位和对话讲解由运行插件的平台、模型和工具完成。脚本不会自动识别 Figure/Table，也不会把图片插入聊天。

## 安装与使用

### 将插件加入支持的平台

克隆仓库：

```bash
git clone https://github.com/zms618/academic-skills.git
cd academic-skills
```

在支持 Codex 插件包的客户端中，按该客户端的插件安装流程从克隆目录加载插件；其插件元数据位于 `.codex-plugin/plugin.json`，通用清单位于 `plugin.json`。若使用的平台只支持手动添加 Skill，请将整个 `skills/paper-reading/` 目录加入平台的 Skills 配置，并保留其中的 `scripts/` 文件夹。

不同客户端的安装入口、文件访问能力和图像输出方式各不相同；不能据此假设任意 ChatGPT 客户端都支持从 GitHub 一键安装或完整调用本地工具。

### 推荐的泛读提示

在客户端上传论文 PDF 后，可以这样开始：

> 帮我读这篇论文。先进入第一站，用通俗语言说明研究问题和动机，并核验官方代码开源状态。按七站框架先完成前三站泛读，每次只讲一站；优先结合论文原图。第三站结束时停下来问我是否进入第四站精读。

之后可回复“继续”，或直接提问“详细解释 Figure 3”。也可以明确要求“从第五站开始讲公式”或“直接评估实验”。能否持续读取已上传附件、联网核验代码、显示原始图片，取决于客户端与当前运行工具。

### 安装 PDF 脚本依赖

需要单独运行图像脚本时，使用 Python 3.10 或更新版本：

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

仅使用插件提示与 Skill 说明时，无需安装 Python 依赖。PDF 脚本依赖 PyMuPDF 和 Pillow；图文卡需要系统中存在可读取的中日韩字体，也可用 `--font` 指定字体文件。字体不随仓库分发。

## PDF 图像脚本示例

页码从 1 开始。先渲染页面检查图表位置，再按已核验区域裁切；坐标顺序是 `left top right bottom`，取值范围为 0–1：

```bash
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --output output/page-3.png
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --rect 0.49 0.12 0.95 0.49 --dpi 220 --output output/figure-3.png
```

为原图添加导读卡：

```bash
python skills/paper-reading/scripts/make_figure_card.py output/figure-3.png --output output/figure-3-card.png --title "Figure 3 · 模型总体流程" --intro "请先观察输入经过哪些模块，再沿箭头追踪最终输出。"
```

裁图工具只渲染用户指定的页面和区域，不会自动定位图表。请先检查整页和论文 caption，不能把示例坐标直接套用到其他论文。图文卡只保证单张图片内部的导读和原图顺序；聊天客户端仍可能调整整张图片在回复中的位置。

## 项目结构

```text
academic-skills/
├── .codex-plugin/plugin.json        # Codex 风格插件元数据
├── plugin.json                      # 通用插件清单
├── skills/paper-reading/
│   ├── SKILL.md                     # 七站阅读框架与教学规范
│   └── scripts/
│       ├── crop_pdf_asset.py
│       └── make_figure_card.py
├── tests/                           # 清单、阅读框架与脚本测试
├── .github/workflows/check.yml
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 版本与开发检查

当前版本为 **v0.5.0**。版本说明见 [`CHANGELOG.md`](CHANGELOG.md)。本地检查：

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

GitHub Actions 会在 push 和 pull request 时运行同一组检查。

## 能力边界与隐私

- 本仓库不是独立论文阅读应用，不包含 OCR 服务、论文问答模型、自动图表定位器或聊天客户端。
- Skill 文件描述 AI 助手应如何开展阅读；论文解析、联网查证、图片展示和跨轮记忆能力由所用平台及其工具决定，不能由提示文本保证。
- PDF 裁剪和图文卡是本仓库实际提供的 Python 功能；它们不判断论文内容是否正确，也不替代人工核对图表与 caption。
- 不要把未获分发许可的论文 PDF、数据、密钥、访问令牌、私人聊天或个人文件提交到公开仓库。依赖库各自遵循其发布许可证。

## License

本仓库以 MIT License 发布，详见 [`LICENSE`](LICENSE)。第三方依赖仍遵循各自许可证。

---

### English

**paper-reading** is a Codex-style research paper reading plugin in the `academic-skills` repository. It provides a seven-stage reading guide—three stages for an intuitive overview, three for technical deep reading, and an optional evidence and reviewer analysis stage—plus two small PDF image utilities.

The guide does not make the repository a standalone paper-reading application. PDF understanding, web research, image display, and conversation continuity depend on the host AI platform and its available tools. The Python scripts only render or crop user-selected PDF regions and create a guide card that preserves the original image pixels.

See the Chinese documentation above for installation, examples, limitations, and the v0.5.0 release notes.
