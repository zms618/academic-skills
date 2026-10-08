from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
SKILL=(ROOT/'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')

def test_one_click_nav_and_explicit_consent():
    assert '## 每站结尾的「一键进入下一站」交互' in SKILL
    assert 'GenUI.issueNewTurn' in SKILL
    assert 'button onClick' in SKILL
    assert '点击本身就是读者的明确确认' in SKILL
    assert '在点击前不自动推进' in SKILL

def test_mapped_stages_and_fallback():
    for x in ['进入第二站', '进入第三站', '开始精读', '进入第五站', '进入第六站', '进入第七站', '第七站已是终点', '继续第六站', 'FollowUp', '回复继续即可']:
        assert x in SKILL

def test_version_stays_consistent():
    a=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
    b=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert a['version']==b['version']=='0.6.0'
    assert a['extensions']['com.openai']['interface']['displayName']=='论文带读'

def test_keeps_depth_split_and_image_rules():
    for x in ['第一至第三站', '原论文', 'make_figure_card.py', '第五站数学与训练', '第六站', '【玩具示例】']:
        assert x in SKILL
