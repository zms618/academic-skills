import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'skills/research-idea-discovery'


def test_research_idea_discovery_is_listed_in_both_collection_overviews():
    zh = (ROOT / 'README.md').read_text(encoding='utf-8')
    en = (ROOT / 'README.en.md').read_text(encoding='utf-8')
    assert 'skills/research-idea-discovery/README.md' in zh
    assert 'skills/research-idea-discovery/README.en.md' in en
    assert '不消耗 Codex 专用额度' in zh
    assert 'Codex-specific task quota' in en
    assert '从产生科研想法，到验证科研价值' in zh
    assert 'From idea generation to defensible research' in en
    assert '**本项目的 Skills 面向 ChatGPT 网页版使用，不消耗 Codex 专用额度。**' in zh


def test_plugin_manifests_and_primary_skill_are_present():
    plugin = json.loads((PROJECT / 'plugin.json').read_text(encoding='utf-8'))
    codex = json.loads((PROJECT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert plugin['name'] == codex['name'] == 'research-idea-discovery'
    assert plugin['version'] == codex['version'] == '2.7.1'
    assert (PROJECT / 'skills/research-idea-discovery/SKILL.md').is_file()
    assert '[English](README.en.md)' in (PROJECT / 'README.md').read_text(encoding='utf-8')
    assert '[简体中文](README.md)' in (PROJECT / 'README.en.md').read_text(encoding='utf-8')


def test_project_documentation_local_links_resolve():
    docs = [
        ROOT / 'README.md',
        ROOT / 'README.en.md',
        ROOT / 'skills/research-idea-discovery/README.md',
        ROOT / 'skills/research-idea-discovery/README.en.md',
    ]
    for doc in docs:
        text = doc.read_text(encoding='utf-8')
        links = re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text)
        for target in links:
            target = target.split('#', 1)[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            assert (doc.parent / target).exists(), f'{doc.relative_to(ROOT)} -> {target}'


def test_both_projects_credit_their_inspiration_sources():
    idea_zh = (PROJECT / 'README.md').read_text(encoding='utf-8')
    idea_en = (PROJECT / 'README.en.md').read_text(encoding='utf-8')
    paper_zh = (ROOT / 'skills/paper-reading/README.md').read_text(encoding='utf-8')
    paper_en = (ROOT / 'skills/paper-reading/README.en.md').read_text(encoding='utf-8')
    for source in (
        'ResearchStudio', 'CCFA-Skills', 'Auto-claude-code-research-in-sleep',
        'rw-research-skill', 'tashan-research-skills', 'ai_night_scientist', 'patsnap/skills',
    ):
        assert source in idea_zh
        assert source in idea_en
    assert 'kelip-paper-reading' in paper_zh
    assert 'kelip-paper-reading' in paper_en
    assert '不代表官方合作、背书' in idea_zh
    assert 'do not imply official collaboration, endorsement' in idea_en


def test_each_plugin_has_a_chatgpt_web_installation_tutorial():
    paper_zh = (ROOT / 'skills/paper-reading/README.md').read_text(encoding='utf-8')
    paper_en = (ROOT / 'skills/paper-reading/README.en.md').read_text(encoding='utf-8')
    idea_zh = (PROJECT / 'README.md').read_text(encoding='utf-8')
    idea_en = (PROJECT / 'README.en.md').read_text(encoding='utf-8')
    assert '## 在 ChatGPT 网页端创建和安装' in paper_zh
    assert '## Create and install it on ChatGPT Web' in paper_en
    assert '## 在 ChatGPT 网页端创建和安装插件' in idea_zh
    assert '## Create and install this plugin in ChatGPT Web' in idea_en
