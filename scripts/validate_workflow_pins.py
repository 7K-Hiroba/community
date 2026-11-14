#!/usr/bin/env python3
"""Require immutable, human-annotated GitHub Action and workflow references."""

import argparse
import re
import sys
from pathlib import Path

import yaml

SHA = re.compile(r"^[0-9a-f]{40}$")


def iter_uses(node, seen=None):
    """Yield uses value nodes from composed YAML without constructing objects."""
    if node is None:
        return
    if seen is None:
        seen = set()
    if id(node) in seen:
        return
    seen.add(id(node))
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            if isinstance(key, yaml.ScalarNode) and key.value == "uses":
                yield value
            yield from iter_uses(value, seen)
    elif isinstance(node, yaml.SequenceNode):
        for item in node.value:
            yield from iter_uses(item, seen)


def validate_directory(directory: Path):
    errors = []
    workflows = sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml"))
    if not workflows:
        return [f"{directory}: no workflow files found"]
    for workflow in workflows:
        content = workflow.read_text(encoding="utf-8")
        try:
            document = yaml.compose(content, Loader=yaml.SafeLoader)
        except yaml.YAMLError as error:
            errors.append(f"{workflow}: invalid YAML: {error}")
            continue
        lines = content.splitlines()
        for value in iter_uses(document):
            number = value.start_mark.line + 1
            if not isinstance(value, yaml.ScalarNode):
                errors.append(f"{workflow}:{number}: uses: reference must be a scalar")
                continue
            reference = value.value
            if reference.startswith("./"):
                continue
            revision = reference.rsplit("@", 1)[-1] if "@" in reference else ""
            if not SHA.fullmatch(revision):
                errors.append(f"{workflow}:{number}: uses: {reference} is not pinned to a full 40-hex SHA")
            line = lines[number - 1]
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
