# academic-skills · Research Skills Collection

[简体中文](README.md) | **English**

An evolving open-source collection of research plugins for ChatGPT Web. Each plugin is driven by Skill instructions and supporting resources, and has its own ChatGPT installation guide and project documentation. This root README introduces the collection as a whole.

> **The plugins in this collection are used in ChatGPT Web and do not consume Codex-specific task quota.**

## Available projects

### [paper-reading](skills/paper-reading/README.en.md)

> **Read with ChatGPT without using Codex-specific task quota or configuring a separate API key, while following explanations alongside the paper's original figures.** ChatGPT account and plan limits still apply, and side-by-side viewing depends on client support.

![Following a paper explanation alongside its original figure in ChatGPT](docs/images/chatgpt-side-by-side-paper-figure.png)

The [project documentation](skills/paper-reading/README.en.md) covers features, the seven-stage workflow, installation, more screenshots, and optional local PDF utilities.

The core assistant instructions are in [`skills/paper-reading/SKILL.md`](skills/paper-reading/SKILL.md).

### [Research Idea Discovery](skills/research-idea-discovery/README.en.md)

**From idea generation to defensible research: put each idea through feasibility, motivation, mechanism, and evidence checks.** Discover opportunities from papers and failure cases, then examine data feasibility, dangerous near neighbors, mechanism necessity, and minimum decisive experiments. When evidence is insufficient, the workflow can recommend revising, researching further, or stopping.

See the [project guide](skills/research-idea-discovery/README.en.md) for detailed capabilities, ChatGPT Web installation, and limitations.

Primary Skill: [`skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md`](skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md).

## 🙏 Acknowledgements & Inspirations

- **paper-reading** was inspired by [kelip-paper-reading](https://github.com/skJack/kelip-paper-reading).
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
