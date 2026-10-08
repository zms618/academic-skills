# academic-skills · Research Skills Collection

[简体中文](README.md) | **English**

An extensible open-source collection of AI skills and plugins for academic research. The first project is [`paper-reading`](skills/paper-reading/), a paper-reading plugin designed primarily for **ChatGPT**, with compatibility paths for Codex and other hosts. More research skills and plugins will be added over time.

`academic-skills` is a collection rather than a single plugin. Each skill or plugin is maintained in its own directory with its documentation, scripts, and version information.

## Current project: paper-reading

> **A visual, interactive paper-learning tool for ChatGPT conversations. No Codex task or separate API key is required, and there is no need to deploy a local model. Follow the paper from its research motivation to the details of its methods.**

The goal is not to produce a quick summary that makes it seem as though the paper has been read. It helps readers build their own understanding of the problem, method, and evidence.

### Why paper-reading

- **Use it in ChatGPT conversations:** No Codex programming task is needed. Reading is still subject to ChatGPT account, model, file-upload, and tool limits.
- **No separate API key or model deployment:** It uses the model capabilities available in ChatGPT and requires no separate paper QA service.
- **Build intuition before going deeper:** The seven-stage workflow starts with motivation, architecture, and a worked example. Readers can stop after the first three stages or continue into data protocols, equations, training, and implementation.
- **Learn alongside the original paper figures:** Explanations refer to original figures and captions. Side-by-side viewing depends on the host's PDF and image tools; repository scripts do not automatically detect every figure or table.
- **The reader controls each step:** Use a real next-stage control if the host provides one; otherwise reply “continue.” The workflow does not skip stages on its own.

### Core experience: follow the explanation alongside an original paper figure

The screenshot below shows a staged explanation of the Transformer architecture on the left and the paper's original Figure 1 on the right. Readers can follow the modules, arrows, and explanation together. Side-by-side viewing depends on the ChatGPT client. The paper figure appears only as part of a user-provided demonstration; this repository does not redistribute the paper PDF or figure.

![A staged Transformer explanation beside the paper's original Figure 1 in ChatGPT](docs/images/chatgpt-side-by-side-paper-figure.png)

### More ChatGPT Web examples

These screenshots show selecting paper-reading in ChatGPT Web, uploading a paper PDF, generating a paper analysis card, and starting the first stage. The Self-Attention diagram is an explanatory schematic, **not an original paper figure**.

**1. Select paper-reading in the chat interface**

![Selecting paper-reading in the ChatGPT Web plugin picker](docs/images/chatgpt-plugin-picker.png)

**2. Upload a PDF and generate an analysis card with a paper architecture figure**

![paper-reading analyzing Attention Is All You Need and showing the Transformer architecture](docs/images/chatgpt-paper-reading-analysis.png)

**3. Start stage one with the research motivation**

![The first stage explaining the motivation behind the Transformer](docs/images/chatgpt-paper-reading-stage1.png)

**4. Use a schematic to understand global connections in Self-Attention**

![An explanatory schematic of global connections in Transformer Self-Attention](docs/images/self-attention-reading-example.png)

The plugin includes a seven-stage reading workflow and two optional PDF image utilities. The first three stages build intuition, explain the architecture, and trace how an example passes through the method. The remaining stages cover data protocols, mathematics and training, precise execution, and optional evidence review and research transfer.

Readers may stop after the overview or continue into a deep read. Claims should distinguish what the paper reports, what has been verified in code, and what is an inference. Do not invent settings, numbers, or results that are not supported by the sources. The stage order and boundaries are defined in [`SKILL.md`](skills/paper-reading/SKILL.md) and remain unchanged by this repository-level documentation.

| Depth | Stage | Focus |
| --- | --- | --- |
| Overview | 1. Research question and motivation | Task context, limitations of prior methods, hypothesis, and paper metadata checks |
| Overview | 2. Core method and architecture | Inputs, modules, outputs, and design choices based on the original paper figure |
| Overview; stop here if desired | 3. How the method works | Trace one example from input to output |
| Deep read | 4. Data and experimental protocol | Sample fields, preprocessing, label access, data splits, and evaluation protocol |
| Deep read | 5. Mathematical mechanism and training | Objectives, equations, supervision, and parameter freezing or updates |
| Deep read | 6. Exact execution and two-pass walkthrough | Execution order, state, caches, and clearly labeled toy numerical walkthroughs |
| Optional | 7. Experiments, review, and research transfer | Main results, ablations, negative evidence, fairness, reproducibility, and research directions |

### PDF figure utilities

- `crop_pdf_asset.py` renders a user-selected PDF page or crops a region using relative coordinates.
- `make_figure_card.py` adds a title and short guide around a verified source figure and checks that the original image pixels remain unchanged.
- These scripts do not detect figures or tables, interpret their meaning, or insert images into a chat. Paper interpretation, web research, and conversation-based explanation are provided by ChatGPT or another host and its available tools.

Since v0.5.3, the workflow prefers showing a verified crop inline. A `sandbox:/mnt/data/...` link is only a file-download fallback and does not guarantee a right-side preview. The plugin cannot control ChatGPT's image-preview panel.

## Use it in ChatGPT

### Personal account: create and install it on ChatGPT Web

`paper-reading` is **not listed in ChatGPT's public plugin directory**. It can be created and installed as a personal plugin using **Plugin Creator**. The following prompt has been tested successfully in ChatGPT Web to create `论文带读（paper-reading）` and save it to the personal plugin list:

1. Open [ChatGPT](https://chatgpt.com/) and select or mention **Plugin Creator** in a new conversation.
2. Send it the following complete prompt (the verified prompt is in Chinese):

   ```text
   请根据以下 GitHub 仓库创建并安装一个名为「论文带读（paper-reading）」的 ChatGPT 个人插件。

   https://github.com/zms618/academic-skills

   以 skills/paper-reading/SKILL.md 为核心规范，完整保留七站式论文阅读流程、泛读与精读边界、原文图表讲解、数学公式推导和用户确认机制。

   支持中文学术论文精读，每次只推进一个阶段，优先引用论文原图及原始数据，不虚构实验结论。

   不需要额外 API Key 或第三方服务。完成后安装到我的个人插件列表。
   ```

3. Follow Plugin Creator's interface to finish setup. When successful, the “论文带读（paper-reading）” personal plugin card appears. The screenshot below shows a successful creation.

   ![Plugin Creator successfully created and saved the personal paper-reading plugin](docs/images/plugin-creator-paper-reading-created.png)

4. Start a new ChatGPT conversation, select “论文带读” in the plugin picker, and upload a paper PDF. If Plugin Creator cannot read the public repository, download and upload this project's [`SKILL.md`](https://raw.githubusercontent.com/zms618/academic-skills/main/skills/paper-reading/SKILL.md).

Plugin creation and installation depend on account plan, region, and workspace permissions. A personal plugin is not thereby added to ChatGPT's public directory. See the [official Plugins in ChatGPT guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

The main reading workflow does not require local Python installation. PDF cropping is optional and can run only in a host environment that supports executing the scripts; do not assume ChatGPT Web directly runs repository Python files.

If **Plugins** or **Plugin Creator** is unavailable, the current account, plan, region, or workspace policy may not provide access. Check workspace permissions or use a Skills entry point available to your account. See the [official guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

### Workspace administrators: upload or sync from GitHub

Some workspaces allow administrators to upload supported plugin ZIPs through **Admin Console → Plugins → Add** or import a plugin marketplace from GitHub. These options require the appropriate administrator permissions and a compatible plugin package. A regular GitHub source archive may not be a directly uploadable ChatGPT plugin ZIP. This repository provides source code and a Skill; cloning or downloading a ZIP is not a verified one-click installation method. See [OpenAI's official documentation](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) for current access and setup details.

### Example prompt

After selecting “论文带读” and uploading a PDF, you can begin with:

> Help me read this paper. Start at stage one: explain the research problem and motivation in accessible language, and verify whether official code is available. Follow the seven-stage framework, covering only one stage at a time. Complete the first three overview stages, prioritize the original paper figures, and then pause to ask whether I want to continue to stage four.

**Usage limits:** This project does not require deploying a separate paper QA model or entering an OpenAI API key. That does not mean model use is unlimited. ChatGPT processes the paper, and messages, uploads, and tools remain subject to the limits of the account, selected model, and workspace. The plugin does not bypass those limits. See [ChatGPT model and usage limits](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt).

You can reply “continue,” ask “explain Figure 3 in detail,” start at stage five to discuss equations, or request an evaluation of the experiments. If the host offers a working next-stage control, it can be used; otherwise, “continue” is the confirmation. The plugin will not skip stages automatically. Reading uploaded files, checking code online, and displaying figures depend on the ChatGPT account, selected model, client, and available tools.

## Other compatible hosts

The repository also retains a Codex plugin manifest and generic plugin metadata. In environments that support Codex plugin packages, follow that environment's plugin installation process. Hosts that support manual Skill installation can use `skills/paper-reading/` and retain the `scripts/` directory. Installation routes and local file access vary by host.

## Run the PDF utilities locally

Python is needed only if you want to run the image utilities. Python 3.10 or newer is required:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The PDF utilities depend on PyMuPDF and Pillow. Figure cards require a system font that supports CJK characters; use `--font` to specify one if needed. Font files are not distributed in this repository.

Page numbers start at 1. Inspect the full page and caption first, then crop with relative `left top right bottom` coordinates in the 0–1 range:

```bash
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --output output/page-3.png
python skills/paper-reading/scripts/crop_pdf_asset.py paper.pdf --page 3 --rect 0.49 0.12 0.95 0.49 --dpi 220 --output output/figure-3.png
python skills/paper-reading/scripts/make_figure_card.py output/figure-3.png --output output/figure-3-card.png --title "Figure 3 · Overall method" --intro "Trace the modules from input to output along the arrows."
```

The crop tool processes only the page and region selected by the user; it does not locate figures automatically. A figure card preserves the source image within the card, but the chat client may still rearrange images in its response.

## Repository layout

```text
academic-skills/
├── .codex-plugin/plugin.json        # Codex plugin metadata
├── plugin.json                      # Generic plugin manifest
├── skills/paper-reading/
│   ├── SKILL.md                     # Seven-stage reading workflow and guidance
│   └── scripts/                     # User-directed PDF image utilities
├── docs/images/                     # Reading and installation examples
├── tests/                           # Manifest, workflow, and script tests
├── .github/workflows/check.yml
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## Version and checks

The current plugin version is **v0.5.3**. See [`CHANGELOG.md`](CHANGELOG.md) for release history. Run local checks with:

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

GitHub Actions runs checks on pushes and pull requests.

## Scope and privacy

- This repository is not a standalone paper-reading application. It does not include an OCR service, paper QA model, automatic figure locator, or chat client.
- The Skill defines the AI assistant's reading workflow. Paper parsing, web research, image display, and cross-turn context depend on ChatGPT or another host and its tools.
- Python scripts render PDF pages, crop user-selected regions, and create figure cards. They do not determine whether a scientific interpretation is correct or replace checking the paper and caption.
- Do not commit papers without redistribution rights, datasets, access keys, tokens, private chats, or personal files. Third-party dependencies retain their own licenses.
- A `sandbox:` link may appear as a downloadable attachment. Inline preview and click-to-zoom behavior are controlled by the host client.

## License

This repository is licensed under the MIT License; see [`LICENSE`](LICENSE). Third-party dependencies remain under their respective licenses.
