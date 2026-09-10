#!/usr/bin/env python3
"""Measure a hero photo's edges and report what to put in the config.

The mobile copy panel sits directly above the photo with nothing between them,
so it only reads as one section if the panel's colour matches the photo's top
edge. This script measures that edge and tells you whether a flat colour will
do, or whether the backdrop drifts enough to need the stretched 1px slice.

Usage:
    python measure_image.py hero-mobile.jpg
    python measure_image.py hero-mobile.jpg --desktop   # also report left edge

Needs Pillow:  pip install pillow
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")


def luminance(px):
    r, g, b = px[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mean_hex(pixels):
    n = len(pixels)
    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n
    return f"#{r:02X}{g:02X}{b:02X}", (r, g, b)


def measure(path, want_desktop):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    px = img.load()

    print(f"{path}  {w}x{h}")

    # --- top edge: what the mobile panel must match -------------------------
    top = [px[x, y] for y in range(min(4, h)) for x in range(0, w, 4)]
    top_hex, _ = mean_hex(top)

    row = [px[x, 2 if h > 2 else 0] for x in range(0, w, 4)]

    # What causes a visible seam is the backdrop drifting from one side of the
    # frame to the other: match a flat colour to the left and the right end
    # shows a band. So compare the two ends, rather than min/max across the
    # row - a single outlier pixel is not a drift.
    tenth = max(1, len(row) // 10)
    left_hex, left_rgb = mean_hex(row[:tenth])
    right_hex, right_rgb = mean_hex(row[-tenth:])
    drift = abs(luminance(left_rgb) - luminance(right_rgb))

    print()
    print(f"  top edge mean      {top_hex}")
    print(f"  left vs right      {left_hex} .. {right_hex}  (drift {drift:.0f})")

    if drift <= 4:
        print()
        print("  FLAT backdrop. A single colour matches it.")
        print(f'    PANEL_GROUND = "{top_hex}"')
        print("    HERO_IMAGE_MOBILE_TOP = null")
    else:
        print()
        print("  DRIFTING backdrop. No flat colour matches both ends -")
        print("  match the left and the right edge shows a seam.")
        print(f'    PANEL_GROUND = "{top_hex}"   (fallback only)')
        print("    HERO_IMAGE_MOBILE_TOP = the generated slice")
        print("  Generate it with prepare_images.py, which slices this photo's")
        print("  own top row and stretches it behind the panel.")

    # --- where the subject starts, for cropping -----------------------------
    first = None
    for y in range(0, h, 2):
        if any(luminance(px[x, y]) < 120 for x in range(0, w, 4)):
            first = y
            break
    if first is not None:
        print()
        print(f"  subject starts at row {first} ({first / h * 100:.1f}% down)")
        if first > h * 0.12:
            print("  More headroom than needed. Crop so ~45-90px of backdrop")
            print("  remains above the subject; the copy panel supplies the rest.")

    # --- left edge: what the desktop ground must match ----------------------
    if want_desktop:
        band = min(h, int(h * 0.35)) or 1
        left = [px[x, y] for y in range(0, band, 4) for x in range(0, min(24, w))]
        lhex, _ = mean_hex(left)
        print()
        print(f"  left edge (top {band}px)   {lhex}")
        print(f"    HERO_GROUND = \"{lhex}\"")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--desktop", action="store_true",
                    help="also report the left edge, for HERO_GROUND")
    a = ap.parse_args()
    measure(a.image, a.desktop)


if __name__ == "__main__":
    main()
