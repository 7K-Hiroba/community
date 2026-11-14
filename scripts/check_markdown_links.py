#!/usr/bin/env python3
"""Validate repository-relative Markdown links and GitHub-style anchors offline."""

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

INLINE_LINK = re.compile(
    r"!?\[(?P<text>[^\]]*)\]\(\s*(?:<(?P<angle>[^>]+)>|(?P<bare>[^)\s]+))"
    r"(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
REFERENCE_LINK = re.compile(r"!?\[(?P<text>[^\]]*)\]\[(?P<label>[^\]]*)\]")
REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[(?P<label>[^\]]+)\]:\s*(?:<(?P<angle>[^>]+)>|(?P<bare>\S+))"
)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")


def normalize_reference(label: str) -> str:
    return " ".join(label.split()).casefold()


def slugify(text: str) -> str:
    text = INLINE_LINK.sub(lambda match: match.group("text"), text)
    text = REFERENCE_LINK.sub(lambda match: match.group("text"), text)
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


def reference_definitions(lines):
    definitions = {}
    for line in lines:
        match = REFERENCE_DEFINITION.match(line)
        if not match:
            continue
        label = normalize_reference(match.group("label"))
        destination = match.group("angle") or match.group("bare")
        definitions.setdefault(label, destination)
    return definitions


def validate_destination(source: Path, number: int, destination: str, anchor_cache):
    destination = destination.strip()
    if destination.startswith(("https://", "http://", "mailto:", "tel:")):
        return None
    if destination.startswith("#"):
        target = source
        anchor = destination[1:]
    else:
        path_part, separator, anchor = destination.partition("#")
        target = (source.parent / unquote(path_part)).resolve()
        if not separator:
            anchor = ""
    if not target.exists():
        return f"{source}:{number}: missing local link target {destination}"
    if target.is_dir():
        target = target / "README.md"
        if not target.exists():
            return None
    if anchor and target.suffix.lower() == ".md":
        if target not in anchor_cache:
            anchor_cache[target] = anchors_for(target)
        if unquote(anchor).lower() not in anchor_cache[target]:
            return f"{source}:{number}: missing anchor {destination}"
    return None


def validate_links(root: Path):
    errors = []
    files = sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)
    anchor_cache = {}
    for source in files:
        lines = source.read_text(encoding="utf-8").splitlines()
        definitions = reference_definitions(lines)
        for number, line in enumerate(lines, 1):
            for match in INLINE_LINK.finditer(line):
                destination = match.group("angle") or match.group("bare")
                error = validate_destination(source, number, destination, anchor_cache)
                if error:
                    errors.append(error)
            for match in REFERENCE_LINK.finditer(line):
                label = match.group("label") or match.group("text")
                destination = definitions.get(normalize_reference(label))
                if destination is None:
                    continue
                error = validate_destination(source, number, destination, anchor_cache)
                if error:
                    errors.append(error)
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
