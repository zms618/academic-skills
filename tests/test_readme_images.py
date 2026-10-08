from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / 'skills/paper-reading/README.md').read_text(encoding='utf-8')
README_EN = (ROOT / 'skills/paper-reading/README.en.md').read_text(encoding='utf-8')

EXAMPLE_IMAGES = (
    'docs/images/plugin-creator-paper-reading-created.png',
    'docs/images/chatgpt-side-by-side-paper-figure.png',
    'docs/images/chatgpt-plugin-picker.png',
    'docs/images/chatgpt-paper-reading-analysis.png',
    'docs/images/chatgpt-paper-reading-stage1.png',
    'docs/images/self-attention-reading-example.png',
)


def test_readme_examples_are_preserved_and_exist():
    for relative_path in EXAMPLE_IMAGES:
        assert f'](../../{relative_path})' in README
        assert f'](../../{relative_path})' in README_EN
        assert (ROOT / relative_path).is_file()


def test_readme_documents_verified_plugin_creator_install_prompt():
    assert '提示词已在 ChatGPT 网页端成功创建' in README
    assert '请根据以下 GitHub 仓库创建并安装一个名为「论文带读（paper-reading）」' in README
    assert '保存到个人插件列表' in README


def test_root_readmes_are_collection_overviews():
    root_zh = (ROOT / 'README.md').read_text(encoding='utf-8')
    root_en = (ROOT / 'README.en.md').read_text(encoding='utf-8')
    assert root_zh.startswith('# academic-skills · 科研技能集')
    assert '**简体中文** | [English](README.en.md)' in root_zh
    assert '[简体中文](README.md) | **English**' in root_en
    assert 'skills/paper-reading/README.md' in root_zh
    assert 'skills/paper-reading/README.en.md' in root_en
    assert '## 在 ChatGPT 网页端创建和安装' not in root_zh
    assert '## Create and install it on ChatGPT Web' not in root_en


def test_plugin_documentation_is_bilingual_and_repository_maintained():
    plugin_readme = (ROOT / 'skills/paper-reading/README.md').read_text(encoding='utf-8')
    plugin_readme_en = (ROOT / 'skills/paper-reading/README.en.md').read_text(encoding='utf-8')
    assert '[English](README.en.md)' in plugin_readme
    assert '[简体中文](README.md)' in plugin_readme_en
    assert 'Plugin Creator' in plugin_readme_en
    assert 'skills/paper-reading/README.md' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
