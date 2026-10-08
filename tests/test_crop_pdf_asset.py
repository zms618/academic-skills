import json
import subprocess
import sys
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/paper-reading/scripts/crop_pdf_asset.py'


def test_manifest():
    data = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    assert data['name'] == 'paper-reading'
    assert data['version'] == '0.5.3'
    assert (ROOT / 'skills/paper-reading/SKILL.md').is_file()


def test_pdf_crop(tmp_path):
    doc = fitz.open()
    page = doc.new_page(width=600, height=800)
    page.insert_text((100, 100), 'Figure 1: Example', fontsize=24)
    pdf = tmp_path / 'synthetic.pdf'
    doc.save(pdf)
    doc.close()
    out = tmp_path / 'figure.png'
    result = subprocess.run([
        sys.executable, str(SCRIPT), str(pdf), '--page', '1',
        '--rect', '0.1', '0.05', '0.8', '0.4', '--dpi', '150', '--output', str(out),
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    with Image.open(out) as im:
        assert im.format == 'PNG'
        assert im.width > 150


def test_invalid_page(tmp_path):
    doc = fitz.open()
    doc.new_page()
    pdf = tmp_path / 'one-page.pdf'
    doc.save(pdf)
    doc.close()
    result = subprocess.run([
        sys.executable, str(SCRIPT), str(pdf), '--page', '2', '--output', str(tmp_path / 'x.png'),
    ], capture_output=True, text=True)
    assert result.returncode != 0
    assert 'page must be in 1..1' in result.stderr


def test_code_status_guidance():
    skill = (ROOT / 'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
    assert '代码已开源' in skill
    assert '代码未开源' in skill
    assert '代码开源状态未确认' in skill
    assert '第三方复现' in skill
    assert '学科定位与路由' in skill
    assert '研究问题与动机' in skill


def test_stage2_design_guide():
    skill = (ROOT / 'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
    section = skill.split('## 第二站专门规范')[1].split('## 第三站专门规范')[0]
    for k in ['架构与关键设计', '模块—输入—输出—作用—来源/创新归属', '已有 Backbone / 现成模块', '必要性与替代方案']:
        assert k in section
    assert '非公式的整条样本运行留给第三站' in section


def test_stage3_then_stage5_math_rendering_spec():
    skill = (ROOT / 'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
    third = skill.split('## 第三站专门规范')[1].split('## 第四站专门规范')[0]
    fifth = skill.split('## 第五站专门规范')[1].split('## 第六站专门规范')[0]
    assert '不靠公式' in third
    assert '输入 → 第一次处理' in third
    assert '数学目标' in fifth and '参数更新' in fifth
    assert '伪标签确认偏差' in fifth
    assert '数学排版' in skill
    assert '不得把公式直接写进' in skill
    assert 'Unicode 公式代码块' not in skill
    assert '\\frac' in skill  # example intended for rendering, never showing markup as code


def test_stage4_data_protocol_spec():
    skill = (ROOT / 'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
    section = skill.split('## 第四站专门规范')[1].split('## 第五站专门规范')[0]
    for k in ['WHAT DATA + WHICH PROTOCOL', '单样本解析卡', '实验协议卡', '论文真实样本', '训练/验证/测试与域划分协议卡', '仅最终评测']:
        assert k in section
    assert '第三站泛读示例衔接' in section
