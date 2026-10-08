# academic-skills · Research Skills Collection

[简体中文](README.md) | **English**

An evolving open-source collection of AI skills and plugins for academic research. Each project keeps its own usage guide and resources; this root README introduces the collection as a whole.

## Available projects

### [paper-reading](skills/paper-reading/README.en.md)

> **Read with ChatGPT without using Codex-specific task quota or configuring a separate API key, while following explanations alongside the paper's original figures.** ChatGPT account and plan limits still apply, and side-by-side viewing depends on client support.

![Following a paper explanation alongside its original figure in ChatGPT](docs/images/chatgpt-side-by-side-paper-figure.png)

The [project documentation](skills/paper-reading/README.en.md) covers features, the seven-stage workflow, installation, more screenshots, and optional local PDF utilities.

The core assistant instructions are in [`skills/paper-reading/SKILL.md`](skills/paper-reading/SKILL.md).

## Repository layout

```text
academic-skills/
├── skills/
│   └── paper-reading/
│       ├── README.md       # Detailed project and installation guide (Chinese)
│       ├── README.en.md    # Detailed project and installation guide (English)
│       ├── SKILL.md        # Assistant behavior specification
│       └── scripts/        # Optional PDF image utilities
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

This repository is licensed under the MIT License; see [`LICENSE`](LICENSE).
