#!/usr/bin/env python3
"""Validate repository-relative Markdown links and GitHub-style anchors offline."""

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~\[\]]", "", text).strip().lower()
    text = unicodedata.normalize("NFKC", text)
    text = "".join(character for character in text if character.isalnum() or character in " -_")
    return re.sub(r"\s", "-", text)


def anchors_for(path: Path):
    anchors = set()
    counts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING.match(line)
        if not match:
            continue
        base = slugify(match.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def validate_links(root: Path):
    errors = []
    files = sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)
    anchor_cache = {}
    for source in files:
        for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            for match in LINK.finditer(line):
                destination = match.group(1).strip()
                if destination.startswith(("https://", "http://", "mailto:", "tel:")):
                    continue
                if destination.startswith("#"):
                    target = source
                    anchor = destination[1:]
                else:
                    path_part, separator, anchor = destination.partition("#")
                    target = (source.parent / unquote(path_part)).resolve()
                    if not separator:
                        anchor = ""
                if not target.exists():
                    errors.append(f"{source}:{number}: missing local link target {destination}")
                    continue
                if target.is_dir():
                    target = target / "README.md"
                    if not target.exists():
                        continue
                if anchor and target.suffix.lower() == ".md":
                    if target not in anchor_cache:
                        anchor_cache[target] = anchors_for(target)
                    if unquote(anchor).lower() not in anchor_cache[target]:
                        errors.append(f"{source}:{number}: missing anchor {destination}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate_links(root)
    for error in errors:
        print(error)
    if errors:
        return 1
    print(f"Markdown links valid: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
