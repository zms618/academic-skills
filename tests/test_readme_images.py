from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / 'README.md').read_text(encoding='utf-8')

EXAMPLE_IMAGES = (
    'docs/images/chatgpt-plugin-picker.png',
    'docs/images/chatgpt-paper-reading-analysis.png',
    'docs/images/chatgpt-paper-reading-stage1.png',
    'docs/images/self-attention-reading-example.png',
)


def test_readme_examples_are_preserved_and_exist():
    for relative_path in EXAMPLE_IMAGES:
        assert f']({relative_path})' in README
        assert (ROOT / relative_path).is_file()
