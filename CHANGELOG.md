# Release notes

## Unreleased

### Documentation

- Clarify that `academic-skills` is an extensible collection for multiple research skills and plugins, with `paper-reading` as its first project.
- Make ChatGPT the primary use case for `paper-reading`, while retaining Codex compatibility and documenting platform and account limits.
- Clarify that using the ChatGPT host avoids a separately configured API key for this skill, but does not bypass ChatGPT model or tool usage limits.

## v0.5.0 — 2026-10-08

### Added

- A seven-stage paper-reading guide with a clear boundary between the first three overview stages and the subsequent deep-reading stages.
- An optional seventh stage for evidence review, reviewer-style analysis, and research transfer.
- `crop_pdf_asset.py` for rendering a full PDF page or a user-selected crop.
- `make_figure_card.py` for adding a short reading guide around an unchanged, verified figure crop, with a pixel-preservation check.
- Plugin manifests, dependency declarations, automated checks, and usage documentation.

### Notes

- The plugin is named `paper-reading`; its client-facing display name is **论文带读**.
- The reading framework is preserved from the supplied v0.5.0 source. This release organizes the plugin under the `academic-skills` repository and aligns its package name, skill path, metadata, and documentation.
- The plugin provides instructions and two image utilities. PDF interpretation, web verification, image rendering in chat, and conversation continuity depend on the host AI client and its tools.
- No user papers, datasets, chat logs, credentials, or model weights are included.
