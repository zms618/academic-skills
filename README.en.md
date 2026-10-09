# No Heartburn Academic Skills

**A collection of research plugins for students, made to use in ChatGPT Web without consuming Codex-specific quota. Research with less worry.**

[简体中文](README.md) | **English**

## Why this project exists

I am a student too, and I know that tokens and API calls can be expensive for students with limited budgets. Traditional research Skills often run in clients such as Codex or Claude Code. Using those dedicated quotas for routine work like reading papers and exploring research ideas can make these tasks difficult to sustain.

That is why I collected and organized these research plugins for **ChatGPT Web**. Students can use ChatGPT's **Plugin Creator** to create their own personal plugins, then use them directly in ChatGPT conversations—**without consuming Codex or Claude-specific quota and without configuring a separate API token**.

Here, “token-free” means no separately configured or paid API token and no Codex / Claude-specific quota; the plugins are used directly in ChatGPT Web conversations.

## Plugins in this collection

These plugins are installed and used in ChatGPT Web. Each is powered by Skill instructions and supporting resources, and each project README includes a tutorial for creating a personal plugin with Plugin Creator.

> **How to use:** create and install the personal plugin in ChatGPT Web, then select it in a ChatGPT conversation.

## ChatGPT Web Research Plugins

This collection currently includes two research plugins you can create and use in ChatGPT Web:

### 🧩 ChatGPT Web Plugin 01 · [paper-reading](skills/paper-reading/README.en.md)

**Understand papers and practice scientific thinking.** Read explanations alongside original figures in ChatGPT, then learn to question assumptions, examine evidence, and design falsification experiments.

![Following a paper explanation alongside its original figure in ChatGPT](docs/images/chatgpt-side-by-side-paper-figure.png)

Install it in ChatGPT Web: see the [paper-reading plugin guide and installation tutorial](skills/paper-reading/README.en.md#create-and-install-it-on-chatgpt-web). Core instructions: [`paper-reading/SKILL.md`](skills/paper-reading/SKILL.md).

### 🔬 ChatGPT Web Plugin 02 · [Research Idea Discovery](skills/research-idea-discovery/README.en.md)

**Discover research opportunities from papers and failure cases**, examine feasibility, motivation, mechanism-level novelty, and evidence, then produce an evidence-labeled mentor-style research decision report.

Install it in ChatGPT Web: see the [Research Idea Discovery plugin guide and installation tutorial](skills/research-idea-discovery/README.en.md#create-and-install-this-plugin-in-chatgpt-web). Primary Skill: [`Research Idea Discovery`](skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md).

## 🙏 Acknowledgements & Inspirations

- **paper-reading** was inspired by [kelip-paper-reading](https://github.com/skJack/kelip-paper-reading) and [Research Starter Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit), whose authors share useful paper-reading and research-workflow resources.
- **Research Idea Discovery** was inspired by [ResearchStudio](https://github.com/microsoft/ResearchStudio), [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills), [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep), [RW Research Skill](https://github.com/ozrwayne/rw-research-skill), [TaShan Research Skills](https://github.com/TashanGKD/tashan-research-skills), [AI Night-Scientist](https://github.com/microsoft/ai_night_scientist), and [PatSnap Skills](https://github.com/patsnap/skills).

These acknowledgements refer to design and workflow inspiration; they do not imply official collaboration, endorsement, or source-code integration. Any code, documentation, or templates actually reused remain subject to their respective licenses. See each project's README for details.

## Repository layout

```text
academic-skills/
├── skills/
│   ├── paper-reading/
│   │   ├── README.md       # Detailed project and installation guide (Chinese)
│   │   ├── README.en.md    # Detailed project and installation guide (English)
│   │   ├── SKILL.md        # Assistant behavior specification
│   │   └── scripts/        # Optional PDF image utilities
│   └── research-idea-discovery/
│       ├── README.md       # Project overview and ChatGPT usage guide
│       ├── README.en.md    # English project guide
│       ├── skills/         # Primary Skill, role Skills, and references
│       └── scripts/        # Optional local research workflow tools
├── docs/images/            # Project demonstration screenshots
├── tests/
├── .github/workflows/
├── README.md               # Collection overview (Chinese by default)
├── README.en.md            # Collection overview in English
└── LICENSE
```

## Development and license

Run repository checks with:

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

Run the Research Idea Discovery test suite separately:

```bash
cd skills/research-idea-discovery
python -m unittest discover -s tests -v
```

This repository is licensed under the MIT License; see [`LICENSE`](LICENSE).
