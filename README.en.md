# academic-skills · Research Skills Collection

[简体中文](README.md) | **English**

An evolving open-source collection of AI skills and plugins for academic research. Each project keeps its own usage guide and resources; this root README introduces the collection as a whole.

> **These Skills are designed for ChatGPT Web. They do not require starting a Codex coding task or use Codex-specific task quota.** ChatGPT model, message, and tool usage remains subject to account and plan limits.

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
