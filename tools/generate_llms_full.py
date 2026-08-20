#!/usr/bin/env python3
"""Regenerate llms-full.txt: the Halo and Frame docs concatenated for LLMs.

Run from the repo root after editing any halo/ or frame/ page:

    python3 tools/generate_llms_full.py

The output is committed (Jekyll serves it as a static file at
/llms-full.txt). Pages are ordered by nav_order within each section and
YAML front matter is replaced by a source-URL header.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["halo", "frame"]
SITE = "https://docs.brilliant.xyz"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
    return fields


def main() -> int:
    out = [
        "# Brilliant Labs documentation — Halo and Frame (single file for LLMs)",
        "",
        "Generated from the Markdown sources of https://docs.brilliant.xyz/",
        "(sections: " + ", ".join(SECTIONS) + "). Index: /llms.txt",
        "",
    ]
    for section in SECTIONS:
        pages = []
        for md in (ROOT / section).glob("*.md"):
            text = md.read_text()
            fm = parse_front_matter(text)
            try:
                order = float(fm.get("nav_order", 999))
            except ValueError:
                order = 999
            # depth in the nav tree, so parents precede their children
            depth = ("parent" in fm) + ("grand_parent" in fm)
            pages.append(((depth, order), md, fm, text))
        if not pages:
            print(f"error: no pages found under {section}/", file=sys.stderr)
            return 1
        for order, md, fm, text in sorted(pages, key=lambda p: (p[0], p[1].name)):
            body = FRONT_MATTER.sub("", text).strip()
            title = fm.get("title", md.stem)
            out += [
                "",
                "=" * 72,
                f"PAGE: {title} ({SITE}/{section}/{md.stem}/)",
                f"DESCRIPTION: {fm.get('description', '')}",
                "=" * 72,
                "",
                body,
                "",
            ]
    (ROOT / "llms-full.txt").write_text("\n".join(out) + "\n")
    size = (ROOT / "llms-full.txt").stat().st_size
    print(f"wrote llms-full.txt ({size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
