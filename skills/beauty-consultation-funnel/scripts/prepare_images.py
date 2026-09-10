#!/usr/bin/env python3
"""Crop, resize and optimise funnel images, and build the hero slice.

Client photos arrive as 5-8 MB camera JPEGs or PNG exports. Shipping those to a
page that is mostly opened on mobile data is the single easiest performance
mistake to make, so everything here is re-encoded to a sane size.

Usage:
    # desktop hero: square, 1400px
    python prepare_images.py hero.png --out public/images/svc-hero-desktop.jpg --kind hero-desktop

    # mobile hero: 1200 wide, cropped to leave a small margin above the subject,
    # plus the 1px slice the copy panel uses
    python prepare_images.py hero-tall.png --out public/images/svc-hero-mobile.jpg --kind hero-mobile

    # gallery: square, 1000px
    python prepare_images.py shot.jpg --out public/images/svc-gallery-1.jpg --kind gallery

Needs Pillow:  pip install pillow
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")

SPECS = {
    "hero-desktop": {"width": 1400, "square": True},
    "hero-mobile": {"width": 1200, "square": False},
    "gallery": {"width": 1000, "square": True},
}

HEADROOM = 60  # px of backdrop to keep above the subject, at the output width


def luminance(px):
    r, g, b = px[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def find_subject_top(img):
    """First row containing something clearly darker than the backdrop."""
    w, h = img.size
    px = img.load()
    for y in range(0, h, 2):
        if any(luminance(px[x, y]) < 120 for x in range(0, w, 4)):
            return y
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kind", required=True, choices=SPECS)
    ap.add_argument("--quality", type=int, default=86)
    ap.add_argument("--no-slice", action="store_true",
                    help="skip the 1px slice for a flat backdrop")
    a = ap.parse_args()

    spec = SPECS[a.kind]
    img = Image.open(a.source).convert("RGB")
    w, h = img.size
    print(f"source {w}x{h}")

    if a.kind == "hero-mobile":
        # Keep only a small margin above the subject. The copy panel supplies
        # the rest of the vertical space, and it is a roughly fixed height at
        # any screen width while the photo scales — so headroom baked into the
        # image looks right on one phone and wrong on the next.
        subject = find_subject_top(img)
        margin_src = int(HEADROOM * (w / spec["width"]))
        crop_top = max(0, subject - margin_src)
        if crop_top:
            img = img.crop((0, crop_top, w, h))
            print(f"cropped {crop_top}px off the top "
                  f"(subject at {subject}, keeping ~{HEADROOM}px at output scale)")

    if spec["square"]:
        side = min(img.size)
        left = (img.width - side) // 2
        top = img.height - side  # favour the lower part; heads stay in frame
        img = img.crop((left, max(0, top), left + side, max(0, top) + side))

    out_w = spec["width"]
    out_h = round(img.height * out_w / img.width)
    img = img.resize((out_w, out_h), Image.LANCZOS)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    img.save(a.out, "JPEG", quality=a.quality, optimize=True, progressive=True)
    kb = os.path.getsize(a.out) / 1024
    print(f"wrote {a.out}  {out_w}x{out_h}  {kb:.0f} KB")
    if kb > 250:
        print("  over the ~250 KB budget - try --quality 80")

    if a.kind == "hero-mobile" and not a.no_slice:
        px = img.load()
        row = [px[x, 0] for x in range(out_w)]

        # A seam appears when the backdrop drifts from one side of the frame to
        # the other: match a flat colour to the left and the right end shows a
        # band. Compare the two ends rather than min/max across the row, since
        # one outlier pixel is not drift.
        tenth = max(1, out_w // 10)
        lmean = sum(luminance(p) for p in row[:tenth]) / tenth
        rmean = sum(luminance(p) for p in row[-tenth:]) / tenth
        drift = abs(lmean - rmean)

        if drift <= 4:
            n = len(row)
            r = sum(p[0] for p in row) // n
            g = sum(p[1] for p in row) // n
            b = sum(p[2] for p in row) // n
            print(f"\nbackdrop is flat (drift {drift:.0f}); no slice needed.")
            print(f'  PANEL_GROUND = "#{r:02X}{g:02X}{b:02X}"')
            print("  HERO_IMAGE_MOBILE_TOP = null")
        else:
            slice_path = os.path.splitext(a.out)[0] + "-top.png"
            sl = Image.new("RGB", (out_w, 1))
            sl.putdata(row)
            sl.save(slice_path, "PNG", optimize=True)
            print(f"\nbackdrop drifts (drift {drift:.0f}); wrote {slice_path}")
            print("  point HERO_IMAGE_MOBILE_TOP at it - a flat colour would")
            print("  show a seam at one end of the join.")


if __name__ == "__main__":
    main()
