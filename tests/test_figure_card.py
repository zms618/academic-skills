import importlib.util
from pathlib import Path
from PIL import Image, ImageDraw
import re
import pytest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'skills/paper-reading/scripts/make_figure_card.py'
spec = importlib.util.spec_from_file_location('card', FILE)
card = importlib.util.module_from_spec(spec)
spec.loader.exec_module(card)
FONT_CANDIDATES = (
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    'C:/Windows/Fonts/arial.ttf',
)
FONT = next((Path(path) for path in FONT_CANDIDATES if Path(path).is_file()), None)


def test_unmodified_pixel_region_and_header(tmp_path, capsys):
    if FONT is None:
        pytest.skip('A system TrueType font is required for rendering the test card.')
    src = tmp_path / 'original.png'
    img = Image.new('RGB', (440, 200), '#cdef12')
    d = ImageDraw.Draw(img)
    d.rectangle((35, 48, 270, 150), fill='#1166cc')
    d.text((100, 60), 'Figure 1', fill='white')
    img.save(src)
    dest = tmp_path / 'card.png'
    card.create_card(src, dest, 'Figure 1 · Motivation', 'Follow the arrows from the input to the prediction.', FONT)
    output = capsys.readouterr().out
    assert 'Verified unmodified original image region' in output
    m = re.search(r'x=(\d+), y=(\d+), width=(\d+), height=(\d+)', output)
    x, y, w, h = map(int, m.groups())
    assert y > 60 and w == 440 and h == 200
    with Image.open(dest) as composite, Image.open(src) as original:
        assert composite.height > original.height
        assert composite.crop((x,y,x+w,y+h)).tobytes() == original.tobytes()
        assert composite.getpixel((x+100,y-5)) == (255,255,255)
        assert composite.crop((0,0,composite.width,y)).getbbox()  # intro area exists


def test_missing_figure_and_guardrails(tmp_path):
    src = tmp_path / 'original.png'
    Image.new('RGB',(200,100),'white').save(src)
    try:
        card.create_card(src,tmp_path/'card.png','Figure 1', 'a'*261)
    except ValueError as e:
        assert 'short' in str(e)
    else:
        raise AssertionError('Long intro must be rejected')
    assert 'Figure 1' in FILE.read_text('utf-8')


def test_instruction_requires_intro_before_image_call():
    rules = (ROOT/'skills/paper-reading/SKILL.md').read_text('utf-8')
    for phrase in ('导读**必须在发起图片显示工具调用之前', '导读在上、原图在下', 'make_figure_card.py', '原始 Figure/Table 像素区域'):
        assert phrase in rules
