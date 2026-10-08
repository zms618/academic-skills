# 论文带读 · paper-reading

**简体中文** | [English](README.en.md) | [科研技能集总览](../../README.md)

`paper-reading` 是一款面向 ChatGPT 网页版的论文带读个人插件，由 Skill 规范驱动。它通过分阶段讲解帮助读者真正理解论文，而不只是生成一份摘要。核心流程和行为规范见 [`SKILL.md`](SKILL.md)。

> **这是安装在 ChatGPT 网页端使用的个人插件，不消耗 Codex 专用额度。** 下方提供从 Plugin Creator 创建到在新对话中选择插件的完整教程。

## 特点

- **在 ChatGPT 对话中使用**：不必启动 Codex 编程任务；论文阅读仍受 ChatGPT 账号、模型、文件上传和工具限制。
- **无需另配 API Key 或部署模型**：使用宿主当前可用的模型能力；这不代表模型调用没有用量限制。
- **先泛读，再按需精读**：先理解研究动机、方法架构和样本运行，再决定是否继续看数据协议、数学机制与实现。
- **按论证作用覆盖原图表**：为 Figure、Table、Algorithm 和 Teaser 建立语义图谱，按阶段记录必要证据并检查是否讲全；多张必要图表可在同一阶段分段讲解。
- **准确区分方法图类型**：先判断论文是否有真正的整体架构图，区分架构图、流程图和算法伪代码；没有架构图时会明确说明。
- **结合论文原图学习**：讲解尽量依据论文图表和 caption；并排展示能力取决于 ChatGPT 客户端及其文件、图像工具。
- **读者控制进度**：一次推进一个阶段；前三站结束后可停下，也可确认继续。

目标是帮助读者建立对研究问题、方法和证据的理解，不替读者声称“已经读完”。论文报告、代码核验和推断应明确区分；来源未提供的信息不得编造。

## 七站阅读流程

| 深度 | 站点 | 内容 |
| --- | --- | --- |
| 泛读 | 1. 研究问题与动机 | 任务背景、已有方法局限、研究假设和论文信息核验 |
| 泛读 | 2. 核心方法与架构 | 结合原图梳理输入、模块、输出与设计选择 |
| 泛读，可在此停止 | 3. 方法如何工作 | 跟踪一个样本从输入到输出 |
| 精读 | 4. 数据与实验协议 | 样本、预处理、标签权限、数据划分和评测协议 |
| 精读 | 5. 数学机制与训练 | 目标函数、公式、监督信号和参数更新 |
| 精读 | 6. 精确执行与双轮推演 | 执行顺序、状态、缓存和明确标记的玩具数值推演 |
| 可选 | 7. 实验、审稿与科研迁移 | 结果、消融、负面证据、公平性、复现与研究启发 |

每次只推进一个阶段。用户回复“继续”作为进入下一阶段的确认；如果宿主提供真实可用的交互控件，也可以使用。插件不会自动跳站。

## 对照论文原图阅读

主要使用体验是边看分步讲解、边对照论文原图。以下截图展示了 ChatGPT 中的讲解与原始 Figure 1 并排阅读；该演示图来自用户提供的界面截图，本仓库不分发论文 PDF 或论文图表。

![在 ChatGPT 中阅读 Transformer 时，左侧是分步讲解，右侧并排查看论文原始 Figure 1](../../docs/images/chatgpt-side-by-side-paper-figure.png)

其他网页端示例展示插件选择、上传 PDF、生成分析卡和开始第一站。Self-Attention 连线图只是解释性示意图，**不是论文原图**。

![ChatGPT 网页插件选择器中的论文带读](../../docs/images/chatgpt-plugin-picker.png)

![论文带读分析 Attention Is All You Need 论文并展示 Transformer 架构图](../../docs/images/chatgpt-paper-reading-analysis.png)

![论文带读第一站讲解 Transformer 的研究动机](../../docs/images/chatgpt-paper-reading-stage1.png)

![用示意图解释 Transformer Self-Attention 的全局连接](../../docs/images/self-attention-reading-example.png)

插件会优先尝试在对话中真实显示已核验的论文裁图。`sandbox:/mnt/data/...` 仅作为文件下载回退，可能显示为下载附件，不保证打开右侧预览；插件没有控制 ChatGPT 右侧图片预览栏的接口。

## 在 ChatGPT 网页端创建和安装

`paper-reading` 尚未上架 ChatGPT 公共插件目录。可以通过 **Plugin Creator** 创建并安装为个人插件。下面的提示词已在 ChatGPT 网页端成功创建插件并保存到个人插件列表：

1. 打开 [ChatGPT 网页版](https://chatgpt.com/)，在新对话中选择或提及 **Plugin Creator**。
2. 将以下完整提示词发送给它：

   ```text
   请根据以下 GitHub 仓库创建并安装一个名为「论文带读（paper-reading）」的 ChatGPT 个人插件。

   https://github.com/zms618/no-heartburn-academic-skills

   以 skills/paper-reading/SKILL.md 为核心规范，完整保留七站式论文阅读流程、泛读与精读边界、原文图表讲解、数学公式推导和用户确认机制。

   支持中文学术论文精读，每次只推进一个阶段，优先引用论文原图及原始数据，不虚构实验结论。

   不需要额外 API Key 或第三方服务。完成后安装到我的个人插件列表。
   ```

3. 按界面提示完成创建和安装。成功后，个人插件列表中会出现“论文带读（paper-reading）”。

   ![Plugin Creator 成功创建并保存论文带读个人插件](../../docs/images/plugin-creator-paper-reading-created.png)

4. 新建对话，在插件选择器中选“论文带读”，上传论文 PDF。可以从第一站开始，也可以明确指定希望讨论的阶段。

如果 Plugin Creator 无法读取公开仓库，可下载并上传 [`SKILL.md`](https://raw.githubusercontent.com/zms618/no-heartburn-academic-skills/main/skills/paper-reading/SKILL.md)。创建入口受账号计划、地区和工作区权限影响；个人插件不会因此出现在公共插件目录中。官方说明见 [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt)。

### 示例开场提示

> 帮我读这篇论文。先进入第一站，用通俗语言说明研究问题和动机，并核验官方代码开源状态。按七站框架先完成前三站泛读，每次只讲一站；优先结合论文原图。第三站结束时停下来问我是否进入第四站精读。

ChatGPT 处理论文时仍受账号计划、模型、文件上传和工具额度限制；插件不会绕过这些限制。查看 [ChatGPT 模型与使用限制](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt)。

### 工作区管理员安装

部分工作区允许管理员从 **Admin Console → Plugins → Add** 上传受支持的插件 ZIP，或从 GitHub 导入 marketplace。需要相应权限和兼容包；普通 GitHub 源码 ZIP 不一定可直接上传。本仓库并未把普通克隆或下载 ZIP 验证为一键安装方式。具体以 [OpenAI 官方文档](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) 为准。

## 可选 PDF 图像脚本

主要阅读流程不需要本地 Python。仓库包含三个可选工具：

- `scripts/crop_pdf_asset.py`：渲染用户指定的 PDF 页面，或按相对坐标裁图。
- `scripts/make_figure_card.py`：给已核验的原图添加标题和简短导读，并检查原图像素未被改动。
- `scripts/check_figure_coverage.py`：检查人工核验的图表语义清单和当前站点记录是否覆盖必讲证据；它不自动解析 PDF，也不能验证客户端是否实际显示图片。

脚本不会自动识别图表、解释图表含义或把图片插入聊天。需要 Python 3.10+：

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

请从仓库根目录运行这些命令。

PDF 工具依赖 PyMuPDF 和 Pillow。图文卡需要支持中日韩字符的系统字体；可用 `--font` 指定，本仓库不分发字体。

页码从 1 开始。先检查整页和 caption，再用 0–1 范围的 `left top right bottom` 坐标裁图：

```bash
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --output output/page-3.png
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --rect 0.49 0.12 0.95 0.49 --dpi 220 --output output/figure-3.png
python skills/paper-reading/scripts/make_figure_card.py output/figure-3.png --output output/figure-3-card.png --title "Figure 3 · 模型总体流程" --intro "请沿箭头观察输入经过哪些模块并得到输出。"
```

## 能力边界与隐私

- 本项目不是独立论文阅读应用，不包含 OCR 服务、论文问答模型、自动图表定位器或聊天客户端。
- 论文解析、联网检索、图片显示和跨轮上下文依赖 ChatGPT 或其他宿主及其工具。
- Python 脚本只处理用户指定的 PDF 页面和区域，不判断科学结论是否正确。
- 不要提交未获分发许可的论文、数据集、密钥、令牌、私人聊天或个人文件。
- `sandbox:` 链接可能显示为下载附件；内嵌预览和点击放大由宿主客户端决定。

## 🙏 Acknowledgements & Inspirations

论文带读的设计受到 [kelip-paper-reading](https://github.com/skJack/kelip-paper-reading) 启发。感谢该项目作者分享相关工作。此处表示设计灵感来源，不代表官方合作、背书或源码整合；若实际复用其代码、文档或模板，仍需遵守其适用许可证。

当前版本为 **v0.6.0**，详见仓库根目录 [`CHANGELOG.md`](../../CHANGELOG.md)。仓库采用 MIT License，见 [`LICENSE`](../../LICENSE)。
