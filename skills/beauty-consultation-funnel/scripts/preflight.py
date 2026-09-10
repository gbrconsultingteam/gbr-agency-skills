#!/usr/bin/env python3
"""Pre-launch checks for a funnel repo.

Catches the mechanical failures that are easy to miss and expensive to ship:
leftover placeholders, a CTA that goes nowhere, invented-looking reviews, and
images heavy enough to hurt on mobile data.

It cannot judge whether the copy is any good, whether the reviews are genuine,
or whether the seam looks right — walk references/launch-checklist.md for those.

Usage:
    python preflight.py /path/to/client-repo
"""

import argparse
import os
import re
import sys

BLOCKERS = []
WARNINGS = []


def blocker(msg):
    BLOCKERS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def check_configs(repo):
    cfg_dir = os.path.join(repo, "src", "config")
    if not os.path.isdir(cfg_dir):
        blocker(f"no src/config directory in {repo}")
        return

    for name in sorted(os.listdir(cfg_dir)):
        if not name.endswith(".ts"):
            continue
        path = os.path.join(cfg_dir, name)
        src = read(path) or ""

        todos = len(re.findall(r"\bTODO\b", src))
        if todos:
            blocker(f"{name}: {todos} TODO placeholder(s) left")

        # A live page needs somewhere to send people.
        for const in ("BOOKING_URL", "ENROLL_URL"):
            m = re.search(rf"export const {const}[^=]*=\s*(null|\"([^\"]*)\")", src)
            if m and m.group(1) == "null":
                blocker(f"{name}: {const} is null - every CTA renders disabled")

        # Reviews: empty is fine (section hides). Non-empty needs a human to
        # confirm they are real, so flag for eyeballing rather than passing.
        m = re.search(r"export const REVIEWS[^=]*=\s*\[", src)
        if m:
            tail = src[m.end():]
            depth, end = 1, None
            for i, ch in enumerate(tail):
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            body = tail[:end] if end else ""
            count = body.count("name:")
            if count:
                warn(f"{name}: {count} review(s) present — confirm every one is "
                     f"real and copied verbatim from the client's own profile")
            if re.search(r"placeholder\s*:\s*true", body):
                blocker(f"{name}: reviews marked placeholder:true — these are "
                        f"invented and must not be published")
            if re.search(r"sample copy|\[Client Name\]|\[Paste", body, re.I):
                blocker(f"{name}: reviews contain sample/placeholder text")

        # Alt text
        alts = re.findall(r"alt:\s*\"([^\"]*)\"", src)
        for alt in alts:
            if not alt.strip() or alt.strip().upper().startswith("TODO"):
                blocker(f"{name}: gallery image missing real alt text")
                break


def check_images(repo):
    img_dir = os.path.join(repo, "public", "images")
    if not os.path.isdir(img_dir):
        warn("no public/images directory")
        return
    for name in sorted(os.listdir(img_dir)):
        path = os.path.join(img_dir, name)
        if not os.path.isfile(path):
            continue
        kb = os.path.getsize(path) / 1024
        if kb > 250:
            warn(f"{name} is {kb:.0f} KB - over the ~250 KB budget for mobile")

    # Template placeholders cannot be detected reliably: their "REPLACE ME"
    # caption is rasterised into the pixels, not stored as text. Eyeball the
    # gallery and hero on the rendered page instead.


def check_routes(repo):
    routes = os.path.join(repo, "src", "routes")
    index = read(os.path.join(routes, "index.tsx"))
    if index and "redirect" not in index:
        warn("/ does not redirect - expected it to send visitors to /consultation")

    training_route = os.path.join(routes, "training-consultation.tsx")
    training_cfg = os.path.join(repo, "src", "config", "training.ts")
    if os.path.exists(training_route) and not os.path.exists(training_cfg):
        blocker("training route exists but its config does not")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    a = ap.parse_args()

    if not os.path.isdir(a.repo):
        sys.exit(f"not a directory: {a.repo}")

    check_configs(a.repo)
    check_images(a.repo)
    check_routes(a.repo)

    print()
    if BLOCKERS:
        print(f"BLOCKING ({len(BLOCKERS)})")
        for b in BLOCKERS:
            print(f"  x {b}")
        print()
    if WARNINGS:
        print(f"CHECK BY HAND ({len(WARNINGS)})")
        for w in WARNINGS:
            print(f"  ? {w}")
        print()

    if not BLOCKERS and not WARNINGS:
        print("No mechanical problems found.")
    print("Still to verify by hand: the seam, mobile fit, contrast, the copy,")
    print("and that the booking link actually reaches a scheduler.")
    print("See references/launch-checklist.md")

    sys.exit(1 if BLOCKERS else 0)


if __name__ == "__main__":
    main()
