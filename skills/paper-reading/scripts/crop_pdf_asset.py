#!/usr/bin/env python3
"""Crop an unchanged original PDF figure/table or full page for inline display.

Example:
  python crop_pdf_asset.py paper.pdf --page 3 --rect 0.49 0.12 0.95 0.49 \
      --dpi 220 --output Figure3.png

Rect is left/top/right/bottom as fractions of the PAGE dimensions; 1-based page.
Never invent a crop: inspect a full page first and read the paper caption.
"""
import argparse
from pathlib import Path
from urllib.parse import quote


def verified_download_link(output_path, sandbox_root=Path('/mnt/data')):
    """Build a sandbox link only for a path inside its root; caller verifies the file."""
    root = sandbox_root.resolve()
    resolved_file = Path(output_path).resolve()
    try:
        relative_file = resolved_file.relative_to(root)
    except ValueError:
        return None
    return f"sandbox:/mnt/data/{quote(relative_file.as_posix(), safe='/')}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--page", type=int, required=True, help="1-based PDF page index")
    ap.add_argument("--rect", nargs=4, type=float, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"), help="relative crop coords [0,1], omit for whole page")
    ap.add_argument("--dpi", type=int, default=220)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not args.pdf.is_file():
        ap.error(f"PDF not found: {args.pdf}")
    if args.dpi < 72 or args.dpi > 600:
        ap.error("dpi must be 72..600")

    import fitz
    from PIL import Image
    with fitz.open(str(args.pdf)) as doc:
        if not 1 <= args.page <= len(doc):
            ap.error(f"page must be in 1..{len(doc)}")
        page = doc[args.page - 1]
        clip = page.rect
        if args.rect is not None:
            l, t, r, b = args.rect
            if not (0 <= l < r <= 1 and 0 <= t < b <= 1):
                ap.error("require 0<=left<right<=1 and 0<=top<bottom<=1")
            clip = fitz.Rect(page.rect.x0 + l*page.rect.width,
                             page.rect.y0 + t*page.rect.height,
                             page.rect.x0 + r*page.rect.width,
                             page.rect.y0 + b*page.rect.height)
        pix = page.get_pixmap(matrix=fitz.Matrix(args.dpi/72, args.dpi/72), clip=clip, alpha=False)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(args.output))
    with Image.open(args.output) as img:
        img.verify()
    with Image.open(args.output) as img:
        width, height = img.size
    if width < 150 or height < 90:
        raise RuntimeError(f"Crop is too small: {width}x{height}; inspect coordinates/dpi")
    print(f"Verified original PDF crop: {args.output} ({width}x{height}), page={args.page}")
    # Only emit a DOWNLOAD fallback link for a verified image saved in the
    # ChatGPT sandbox. The caller still must display the original image.
    download_link = verified_download_link(args.output)
    if download_link:
        print(f"Verified download-only fallback link: [下载原论文裁剪原图]({download_link})")


if __name__ == "__main__":
    main()
