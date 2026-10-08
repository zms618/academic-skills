from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=(ROOT/'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
README=(ROOT/'README.md').read_text(encoding='utf-8')

def test_no_false_preview_claim():
    assert '不能再声称点击沙盒文件链接会预览' in SKILL
    assert '右侧栏' in SKILL
    assert '下载 Figure X 原图 PNG' in SKILL
    assert '只有用户主动要保存' in SKILL

def test_readme_explains_client_limit():
    assert '右侧图片预览栏' in README
    assert '下载附件' in README
