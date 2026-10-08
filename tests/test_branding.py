from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_public_display_name_and_stable_internal_identifier():
    a = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    b = json.loads((ROOT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert a['version'] == b['version'] == '0.5.3'
    assert a['name'] == b['name'] == 'paper-reading'
    assert a['extensions']['com.openai']['interface']['displayName'] == '论文带读'
    assert b['interface']['displayName'] == '论文带读'
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert readme.splitlines()[0].startswith('# academic-skills')
    assert '## 当前收录' in readme
    assert '[paper-reading · 论文带读](skills/paper-reading/README.md)' in readme

def test_reading_flow_unchanged():
    skill = (ROOT / 'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
    assert skill.startswith('---\n')
    assert '# 论文带读：' in skill
    for stage in ('第一站', '第二站', '第三站', '第四站', '第五站', '第六站', '第七站'):
        assert stage in skill
    for required in ('代码开源状态', '原论文', '数学排版显示', 't=0', 't=1', '可选第七站'):
        assert required in skill
