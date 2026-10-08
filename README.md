# academic-skills · 科研技能集

**简体中文** | [English](README.en.md)

一个持续扩展的开源科研插件集合，面向 ChatGPT 网页版使用。每个插件由 Skill 规范及其配套资源驱动，并在自己的目录中提供 ChatGPT 安装教程和项目说明；本仓库根目录介绍整个集合。

> **本项目的 Skills 面向 ChatGPT 网页版使用，不消耗 Codex 专用额度。**

## 当前收录

### [paper-reading · 论文带读](skills/paper-reading/README.md)

> **无需 Codex 专用额度或额外 API Key，就能在 ChatGPT 对话中边读讲解、边对照论文原图。** ChatGPT 自身的套餐和使用限制仍然适用；并排查看取决于客户端支持。

![ChatGPT 中边读论文讲解、边对照论文原图的示例](docs/images/chatgpt-side-by-side-paper-figure.png)

详细功能、七站式阅读流程、安装说明、更多截图和本地 PDF 辅助脚本见[项目说明](skills/paper-reading/README.md)。

核心行为规范位于 [`skills/paper-reading/SKILL.md`](skills/paper-reading/SKILL.md)。

### [Research Idea Discovery · 科研创新点发现与验证](skills/research-idea-discovery/README.md)

**从产生科研想法，到验证科研价值：让每一个创新点经受可行性、动机、机制与证据的多重检验。** 它从论文和失败现象中寻找研究机会，再审查数据可行性、危险近邻、机制必要性和最小决定性实验；证据不足时允许建议调整、继续调研或停止。

详细能力、ChatGPT 网页版安装说明和能力边界见[项目说明](skills/research-idea-discovery/README.md)。

主 Skill：[`skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md`](skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md)。

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
