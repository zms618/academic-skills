# 不烧心 academic-skills

**面向学生党的 ChatGPT 网页端科研插件合集：不耗 Codex 专用额度，用着不烧心。**

**简体中文** | [English](README.en.md)

## 项目初衷

作者自己也是学生，理解 token 和 API 调用成本会给经费有限的学生带来负担。传统科研 Skills 通常需要在 Codex、Claude Code 等客户端中使用；如果把日常读论文、找研究 Idea 等繁琐工作都放在那里，专用额度和费用可能让学生难以长期承担。

因此，我搜集并整理了这些面向 **ChatGPT 网页端**的科研插件。学生可以通过网页版 ChatGPT 的 **Plugin Creator** 创建属于自己的插件，然后直接在 ChatGPT 对话中使用，**不消耗 Codex 或 Claude 专用额度，也无需额外配置 API Token**。

这里的“免 token”指无需额外配置或支付 API Token，也不消耗 Codex / Claude 专用额度；插件直接在 ChatGPT 网页端的对话中使用。

## 本项目的插件

这些插件安装并使用于 ChatGPT 网页端。插件内部由 Skill 规范和配套资源驱动；每个项目的 README 都提供了使用 Plugin Creator 创建个人插件的教程。

> **使用方式：在 ChatGPT 网页端创建并安装个人插件 → 在 ChatGPT 对话中选择插件并使用。**

## ChatGPT 网页端科研插件

以下是本项目目前收录的两个**可在 ChatGPT 网页端创建并使用的插件**。点击卡片进入插件说明和安装教程。

| 🧩 ChatGPT 网页端插件 · 论文阅读 | 🔬 ChatGPT 网页端插件 · 科研选题 |
| --- | --- |
| **[📄 论文带读 · paper-reading](skills/paper-reading/README.md)**<br><br>在 ChatGPT 对话中边读讲解、边对照论文原图；支持七阶段泛读与精读流程。<br><br>**[查看介绍与 ChatGPT 安装教程 →](skills/paper-reading/README.md#在-chatgpt-网页端创建和安装)** | **[🧪 科研创新点发现与验证 · Research Idea Discovery](skills/research-idea-discovery/README.md)**<br><br>从论文和失败现象中寻找研究机会，并审查可行性、研究动机、机制新颖性与验证证据。<br><br>**[查看介绍与 ChatGPT 安装教程 →](skills/research-idea-discovery/README.md#在-chatgpt-网页端创建和安装插件)** |

### 论文带读：在 ChatGPT 中对照原文图表

![ChatGPT 中边读论文讲解、边对照论文原图的示例](docs/images/chatgpt-side-by-side-paper-figure.png)

插件行为规范：[`paper-reading/SKILL.md`](skills/paper-reading/SKILL.md) · [`Research Idea Discovery 主 Skill`](skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md)

## 🙏 致谢与灵感来源

- **paper-reading** 的设计受到 [kelip-paper-reading](https://github.com/skJack/kelip-paper-reading) 启发。
- **Research Idea Discovery** 的设计受到 [ResearchStudio](https://github.com/microsoft/ResearchStudio)、[CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills)、[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)、[RW Research Skill](https://github.com/ozrwayne/rw-research-skill)、[TaShan Research Skills](https://github.com/TashanGKD/tashan-research-skills)、[AI Night-Scientist](https://github.com/microsoft/ai_night_scientist) 和 [PatSnap Skills](https://github.com/patsnap/skills) 启发。

以上致谢表示设计与工作流灵感，不代表官方合作、背书或源码整合；实际复用的代码、文档和模板仍须遵守各自许可证。详细说明见各项目 README。

## 仓库结构

```text
academic-skills/
├── skills/
│   ├── paper-reading/
│   │   ├── README.md       # 论文带读的详细介绍与安装指南
│   │   ├── README.en.md    # English documentation
│   │   ├── SKILL.md        # 助手行为规范
│   │   └── scripts/        # 可选 PDF 图像辅助脚本
│   └── research-idea-discovery/
│       ├── README.md       # 项目介绍与 ChatGPT 使用指南
│       ├── README.en.md    # English project guide
│       ├── skills/         # 主 Skill、辅助角色与参考规范
│       └── scripts/        # 可选本地研究工作流工具
├── docs/images/            # 项目演示截图
├── tests/
├── .github/workflows/
├── README.md               # 科研技能集总览（中文默认）
├── README.en.md            # Collection overview in English
└── LICENSE
```

## 开发与许可

运行仓库总览与 paper-reading 检查：

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

运行 Research Idea Discovery 自带的测试：

```bash
cd skills/research-idea-discovery
python -m unittest discover -s tests -v
```

本仓库采用 MIT License，详见 [`LICENSE`](LICENSE)。
