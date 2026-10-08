from pathlib import Path
import importlib.util
import subprocess,sys
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SKILL=(ROOT/'skills/paper-reading/SKILL.md').read_text(encoding='utf-8')
CROP=ROOT/'skills/paper-reading/scripts/crop_pdf_asset.py'
spec=importlib.util.spec_from_file_location('crop_pdf_asset', CROP)
crop=importlib.util.module_from_spec(spec)
spec.loader.exec_module(crop)

def test_per_figure_verified_download_rule():
    for x in ['图片预览与文件下载严格区分','不能再声称点击沙盒文件链接会预览','右侧栏','只有用户主动要保存','下载 Figure X 原图 PNG']:
        assert x in SKILL

def test_download_link_is_limited_to_verified_sandbox_root(tmp_path):
    sandbox=tmp_path/'sandbox'
    image=sandbox/'nested dir'/'figure 1.png'
    image.parent.mkdir(parents=True)
    Image.new('RGB',(160,100),'white').save(image)
    with Image.open(image) as im: im.verify()
    assert crop.verified_download_link(image,sandbox) == 'sandbox:/mnt/data/nested%20dir/figure%201.png'
    assert crop.verified_download_link(tmp_path/'outside.png',sandbox) is None

def test_outside_sandbox_does_not_emit_false_link(tmp_path):
    pdf=tmp_path/'t.pdf'
    d=fitz.open();d.new_page(width=300,height=300);d.save(pdf);d.close()
    p=subprocess.run([sys.executable,str(CROP),str(pdf),'--page','1','--output',str(tmp_path/'f.png')],check=True,text=True,capture_output=True)
    assert 'Verified original PDF crop:' in p.stdout
    assert 'sandbox:/mnt/data/' not in p.stdout
