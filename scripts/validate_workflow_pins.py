#!/usr/bin/env python3
"""Require immutable, human-annotated GitHub Action and workflow references."""

import argparse
import re
import sys
from pathlib import Path

USES = re.compile(r"(?:^|\s)-?\s*uses:\s*[\"']?([^\"'\s#]+)")
SHA = re.compile(r"^[0-9a-f]{40}$")


def validate_directory(directory: Path):
    errors = []
    workflows = sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml"))
    if not workflows:
        return [f"{directory}: no workflow files found"]
    for workflow in workflows:
        for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
            match = USES.search(line)
            if not match:
                continue
            reference = match.group(1)
            if reference.startswith("./"):
                continue
            revision = reference.rsplit("@", 1)[-1] if "@" in reference else ""
            if not SHA.fullmatch(revision):
                errors.append(f"{workflow}:{number}: uses: {reference} is not pinned to a full 40-hex SHA")
            comment = line.split("#", 1)[1].strip() if "#" in line else ""
            if not comment:
                errors.append(f"{workflow}:{number}: uses: {reference} needs a human-readable version comment")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_dir", type=Path)
    args = parser.parse_args()
    errors = validate_directory(args.workflow_dir)
    for error in errors:
        print(error)
    if errors:
        return 1
    print(f"Workflow pins valid: {args.workflow_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
