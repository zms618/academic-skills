from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT/'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')

def test_version_name_and_manifest_routing():
    a = json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
    b = json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert a['version'] == b['version'] == '0.6.0'
    assert a['extensions']['com.openai']['interface']['displayName'] == '论文带读'
    assert b['interface']['displayName'] == '论文带读'
    assert '前三站' in a['extensions']['com.openai']['interface']['longDescription']

def test_late_formulas_and_stage_order():
    marks=['## 第二站专门规范','## 第三站专门规范','## 第四站专门规范','## 第五站专门规范','## 第六站专门规范','## 可选第七站专门规范']
    assert [SKILL.index(x) for x in marks] == sorted(SKILL.index(x) for x in marks)
    assert '第1–3站默认**不展示复杂公式' in SKILL
    assert '第五站数学与训练' in SKILL
    assert '泛读已经完成' in SKILL

def test_stage_three_has_complete_non_formula_walkthrough():
    s=SKILL.split('## 第三站专门规范')[1].split('## 第四站专门规范')[0]
    for x in ['输入 → 第一次处理', '效果快照', '读到这里已经完成泛读', '不能因为讲过架构模块就省略样本怎么运行', '不靠公式']:
        assert x in s

def test_deep_reading_preserves_reproducibility_and_figures():
    for s in ['代码未开源','代码开源状态未确认','make_figure_card.py','数学排版显示','t=0','t=1','信息流状态表','【玩具示例】','训练/预测/适应','原论文']:
        assert s in SKILL

def test_readme_explains_stop_point():
    s=(ROOT/'skills/paper-reading/README.md').read_text(encoding='utf-8')
    assert '可在此停止' in s and '精读' in s and '泛读' in s
