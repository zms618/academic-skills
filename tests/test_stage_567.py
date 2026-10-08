from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT/'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')


def test_manifest_versions_match():
    a=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
    b=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert a['version']==b['version']=='0.6.0'


def test_stage5_training_and_rendered_math():
    fifth=SKILL.split('## 第五站专门规范')[1].split('## 第六站专门规范')[0]
    for s in ['总目标', '数学约束', '训练阶段', '参数更新', '参数冻结', '数值手算', '论文没有说明']:
        assert s in fifth
    assert '数学排版' in SKILL


def test_stage6_execution_two_round_and_real_shapes():
    sixth=SKILL.split('## 第六站专门规范')[1].split('## 可选第七站专门规范')[0]
    for s in ['信息流状态表', '训练/预测/适应', '缓存复用', '测试时适应路径', 'stateless', 't=0', 't=1', '不能虚构梯度', '【玩具示例】']:
        assert s in sixth
    assert '第六站 A' in sixth and '第六站 B' in sixth


def test_stage7_negative_results_and_fairness():
    seventh=SKILL.split('## 可选第七站专门规范')[1].split('## 七站的正式教学顺序')[0]
    for s in ['Main Results Table','Ablation','负面','百分点','相对百分比','可复现性','审稿人四级创新判断']:
        assert s in seventh


def test_stage_gating_and_math():
    assert '只有再次说“继续/进入精读”' in SKILL
    assert '泛读已经完成' in SKILL
    assert '数学排版显示' in SKILL
    assert '原论文' in SKILL
