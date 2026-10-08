# academic-skills · 科研技能集

**简体中文** | [English](README.en.md)

一个持续扩展的开源科研技能集合，收录面向学术研究的 AI skills 与插件。每个项目在自己的目录中维护使用说明和相关资源；本仓库根目录用于介绍整个集合。

## 当前收录

### [paper-reading · 论文带读](skills/paper-reading/README.md)

> **无需 Codex 专用额度或额外 API Key，就能在 ChatGPT 对话中边读讲解、边对照论文原图。** ChatGPT 自身的套餐和使用限制仍然适用；并排查看取决于客户端支持。

![ChatGPT 中边读论文讲解、边对照论文原图的示例](docs/images/chatgpt-side-by-side-paper-figure.png)

详细功能、七站式阅读流程、安装说明、更多截图和本地 PDF 辅助脚本见[项目说明](skills/paper-reading/README.md)。

核心行为规范位于 [`skills/paper-reading/SKILL.md`](skills/paper-reading/SKILL.md)。

## 仓库结构

```text
academic-skills/
├── skills/
│   └── paper-reading/
│       ├── README.md       # 论文带读的详细介绍与安装指南
│       ├── README.en.md    # English documentation
│       ├── SKILL.md        # 助手行为规范
│       └── scripts/        # 可选 PDF 图像辅助脚本
├── docs/images/            # 项目演示截图
├── tests/
├── .github/workflows/
├── README.md               # 科研技能集总览（中文默认）
├── README.en.md            # Collection overview in English
└── LICENSE
```

## 开发与许可

运行仓库检查：

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

本仓库采用 MIT License，详见 [`LICENSE`](LICENSE)。
