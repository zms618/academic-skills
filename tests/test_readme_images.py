from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / 'README.md').read_text(encoding='utf-8')

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
        assert f']({relative_path})' in README
        assert (ROOT / relative_path).is_file()


def test_readme_documents_verified_plugin_creator_install_prompt():
    assert '这条提示已在 ChatGPT 网页端成功创建' in README
    assert '请根据以下 GitHub 仓库创建并安装一个名为「论文带读（paper-reading）」' in README
    assert '保存到个人插件列表' in README


def test_readme_defaults_to_chinese_and_links_full_english_version():
    assert README.startswith('# academic-skills · 科研技能集')
    assert '**简体中文** | [English](README.en.md)' in README
    english_readme = (ROOT / 'README.en.md').read_text(encoding='utf-8')
    assert '[简体中文](README.md) | **English**' in english_readme
    assert '## Use it in ChatGPT' in english_readme
    assert 'Plugin Creator' in english_readme
