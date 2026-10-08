# academic-skills · Research Skills Collection

[简体中文](README.md) | **English**

An evolving open-source collection of AI skills and plugins for academic research. Each project keeps its own usage guide and resources; this root README introduces the collection as a whole.

## Available projects

### [paper-reading](skills/paper-reading/README.en.md)

A guided paper-reading experience for ChatGPT and other AI assistants, helping readers move from research motivation and method architecture to equations, experiments, and evidence. See the [project documentation](skills/paper-reading/README.en.md) for features, the seven-stage workflow, installation, screenshots, and optional local PDF utilities.

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
