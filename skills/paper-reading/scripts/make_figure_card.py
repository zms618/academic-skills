#!/usr/bin/env python3
"""Bind a short reading guide above an UNCHANGED, already verified original PDF figure.

This only addresses visual ordering *inside one image*: UI clients may move the
whole image output above preceding paragraphs, which this script cannot control.

Usage:
  python make_figure_card.py Figure1.png --output Figure1-card.png \
    --title 'Figure 1 · 为什么过去的方法会失败？' \
    --intro '这张图对比不同条件下的性能，请先观察左侧基线与右侧失败情况。'

The region containing the figure is pasted at full resolution with identical
pixels; axes, legends, labels, and source data are not edited in any way.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf',
    '/System/Library/Fonts/PingFang.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/simhei.ttf',
]


def get_font(font_arg, size):
    candidates = ([str(font_arg)] if font_arg else []) + FONT_CANDIDATES
    for candidate in candidates:
        if Path(candidate).is_file():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    raise RuntimeError('No readable CJK font found. Pass --font /path/to/CJK-font.ttf (font is NOT bundled).')


def wrap_text(draw, text, font, max_width):
    """Wrap mixed Chinese and western text by rendered pixel width."""
    rows = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            rows.append('')
            continue
        current = ''
        for ch in paragraph:
            candidate = current + ch
            if current and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
                rows.append(current)
                current = ch
            else:
                current = candidate
        if current:
            rows.append(current)
    return rows


def create_card(input_path, output_path, title, intro, font_arg=None):
    if not title.strip() or not intro.strip():
        raise ValueError('--title and --intro must be non-empty and grounded in the verified paper figure')
    if len(intro) > 260:
        raise ValueError('Keep the image-card reading guide short (at most 260 characters).')
    with Image.open(input_path) as handle:
        handle.load()
        original = handle.copy()
    if original.mode not in ('RGB', 'RGBA'):
        # Fully faithful per-pixel preservation is easier for PDF crops with alpha=False.
        raise ValueError('Require an RGB/RGBA PDF crop. Re-render the PDF page with alpha=False.')
    padding = 32
    width, fig_height = original.size
    canvas_width = width + padding * 2
    header_font = get_font(font_arg, 26)
    body_font = get_font(font_arg, 20)
    work = Image.new(original.mode, (canvas_width, 100), 'white')
    draw = ImageDraw.Draw(work)
    title_rows = wrap_text(draw, title.strip(), header_font, width)
    intro_rows = wrap_text(draw, intro.strip(), body_font, width)
    title_height = 37 * len(title_rows)
    intro_height = 29 * len(intro_rows)
    fig_y = padding + title_height + 10 + intro_height + 24
    height = fig_y + fig_height + padding
    final = Image.new(original.mode, (canvas_width, height), 'white')
    draw = ImageDraw.Draw(final)
    y = padding
    for line in title_rows:
        draw.text((padding, y), line, fill='#151515', font=header_font)
        y += 37
    y += 10
    for line in intro_rows:
        draw.text((padding, y), line, fill='#303030', font=body_font)
        y += 29
    # Paste WITHOUT a mask; the original pixel values are preserved exactly.
    final.paste(original, (padding, fig_y))
    if final.crop((padding, fig_y, padding + width, fig_y + fig_height)).tobytes() != original.tobytes():
        raise RuntimeError('Image pixel preservation check failed')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, format='PNG')
    with Image.open(output_path) as verify:
        verify.load()
        if verify.size != final.size:
            raise RuntimeError('Output card cannot be verified')
    print(f'Verified unmodified original image region: x={padding}, y={fig_y}, width={width}, height={fig_height}')
    print(f'Image card: {output_path} ({canvas_width}x{height})')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path, help='verified RGB/RGBA PNG crop from the original PDF')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--intro', required=True)
    ap.add_argument('--font', type=Path)
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error(f'Original PDF figure not found: {args.input}')
    create_card(args.input, args.output, args.title, args.intro, args.font)

if __name__ == '__main__':
    main()
