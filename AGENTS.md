# Repository maintenance instructions

- `academic-skills` is a collection for multiple research skills and plugins. Do not replace the root README with a README from an individual plugin release archive.
- Keep the current plugin identifier `paper-reading` and its location at `skills/paper-reading/` when synchronizing future releases.
- The screenshots under `docs/images/` are repository-maintained examples and may not be included in later plugin ZIP files. Preserve them when updating source from a ZIP, and keep every README image reference valid. Keep `chatgpt-side-by-side-paper-figure.png` as the lead demonstration of reading while comparing the explanation with the paper's original figure.
- Preserve accurate captions: the Self-Attention diagram in `self-attention-reading-example.png` is an explanatory schematic, while paper figures in screenshots are shown only as part of the user-provided ChatGPT demonstration.
- Keep ChatGPT installation guidance explicit about account/tool limitations; do not claim that a public GitHub repository is already installed or listed in the public plugin directory.
- After changes, run `python -m pytest -q` and `git diff --check`.
