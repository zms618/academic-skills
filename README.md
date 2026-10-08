# academic-skills · 科研技能集

**简体中文** | [English](README.en.md)

一个持续扩展的开源科研技能集合，收录面向学术研究的 AI skills 与插件。每个项目在自己的目录中维护使用说明和相关资源；本仓库根目录用于介绍整个集合。

## 当前收录

### [paper-reading · 论文带读](skills/paper-reading/README.md)

帮助读者在 ChatGPT 等 AI 助手中循序渐进地理解论文，从研究动机、方法架构到公式、实验和证据。详细功能、七站式阅读流程、安装说明、示例截图和本地 PDF 辅助脚本见[项目说明](skills/paper-reading/README.md)。

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
