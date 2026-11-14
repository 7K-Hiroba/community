#!/usr/bin/env python3
"""Validate the Hiroba app registry, migrations, and base-revision transitions."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

IMMUTABLE_FIELDS = ["repository", "dashboardUidPrefix", "grafanaFolderSegment"]
MIGRATION_LINK_FIELDS = ["replacedBy", "migratedFrom"]
ALLOWED_TRANSITIONS = {
    ("reserved", "reserved"),
    ("reserved", "active"),
    ("reserved", "deprecated"),
    ("active", "active"),
    ("active", "deprecated"),
    ("deprecated", "deprecated"),
}


def load_json_text(text: str, source: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"{source}: invalid JSON at line {error.lineno} column {error.colno}: {error.msg}") from error


def load_json_file(path: Path):
    return load_json_text(path.read_text(encoding="utf-8"), str(path))


def load_base_revision(revision: str):
    result = subprocess.run(
        ["git", "show", f"{revision}:registry/apps.json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.strip()
        missing_markers = [
            f"path 'registry/apps.json' does not exist in '{revision}'",
            f"path 'registry/apps.json' exists on disk, but not in '{revision}'",
        ]
        if any(marker in detail for marker in missing_markers):
            return {"schemaVersion": 1, "apps": []}
        raise ValueError(f"cannot read base revision {revision}: {detail}")
    return load_json_text(result.stdout, revision)


def path_text(path):
    parts = list(path)
    if not parts:
        return "registry"
    output = str(parts[0])
    for part in parts[1:]:
        output += f"[{part}]" if isinstance(part, int) else f".{part}"
    return output


def validate_schema(document, schema):
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
        errors.append(f"{path_text(error.path)}: {error.message}")
    return errors


def validate_semantics(document):
    errors = []
    apps = document.get("apps", [])
    by_id = {}
    repositories = {}
    for index, entry in enumerate(apps):
        prefix = f"apps[{index}]"
        app_id = entry.get("id", "")
        folded = app_id.casefold()
        if folded in by_id:
            errors.append(f"{prefix}.id: duplicate or near-duplicate id {app_id}")
        by_id[folded] = entry
        repository = entry.get("repository", "")
        expected_repository = f"https://github.com/7K-Hiroba/{app_id}"
        if repository != expected_repository:
            errors.append(f"{prefix}.repository: must equal {expected_repository}")
        folded_repository = repository.casefold()
        if folded_repository in repositories:
            errors.append(f"{prefix}.repository: duplicate repository {repository}")
        repositories[folded_repository] = app_id
        maintainers = entry.get("maintainers", [])
        folded_maintainers = [handle.casefold() for handle in maintainers]
        if len(set(folded_maintainers)) != len(folded_maintainers):
            errors.append(f"{prefix}.maintainers: duplicate maintainer handle")
        if entry.get("dashboardUidPrefix") != f"{app_id}-":
            errors.append(f"{prefix}.dashboardUidPrefix: must equal {app_id}-")
        if entry.get("grafanaFolderSegment") != app_id:
            errors.append(f"{prefix}.grafanaFolderSegment: must equal {app_id}")
        status = entry.get("status")
        if "replacedBy" in entry and status != "deprecated":
            errors.append(f"{prefix}: migration replacedBy is valid only on a deprecated entry")
        if "migratedFrom" in entry and status == "deprecated":
            errors.append(f"{prefix}: migration migratedFrom is not valid on a deprecated entry")

    for index, entry in enumerate(apps):
        prefix = f"apps[{index}]"
        app_id = entry.get("id", "")
        replacement_id = entry.get("replacedBy")
        old_id = entry.get("migratedFrom")
        if replacement_id:
            replacement = by_id.get(replacement_id.casefold())
            if not replacement:
                errors.append(f"{prefix}: migration replacement {replacement_id} does not exist")
            elif replacement.get("status") == "deprecated":
                errors.append(f"{prefix}: migration replacement must not be deprecated or cyclic")
            elif replacement.get("migratedFrom") != app_id:
                errors.append(f"{prefix}: migration must be paired with {replacement_id}.migratedFrom={app_id}")
        if old_id:
            old = by_id.get(old_id.casefold())
            if not old:
                errors.append(f"{prefix}: migration source {old_id} does not exist")
            elif old.get("status") != "deprecated" or old.get("replacedBy") != app_id:
                errors.append(f"{prefix}: migration must be paired with deprecated {old_id}.replacedBy={app_id}")
    return errors


def validate_base(document, base):
    errors = []
    current = {entry.get("id", "").casefold(): entry for entry in document.get("apps", [])}
    previous = {entry.get("id", "").casefold(): entry for entry in base.get("apps", [])}
    for app_id, old in previous.items():
        if app_id not in current and old.get("status") in {"active", "deprecated"}:
            errors.append(f"apps[{app_id}]: {old.get('status')} entry cannot be deleted or renamed")
    for app_id, old in previous.items():
        if app_id not in current:
            continue
        new = current[app_id]
        old_status = old.get("status")
        new_status = new.get("status")
        if (old_status, new_status) not in ALLOWED_TRANSITIONS:
            errors.append(f"apps[{app_id}].status: invalid {old_status} to {new_status} status transition or old-ID reuse")
        if "migratedFrom" in new and "migratedFrom" not in old:
            errors.append(f"apps[{app_id}].migratedFrom: migration replacement must be a new entry")
        for field in IMMUTABLE_FIELDS:
            if old.get(field) != new.get(field):
                errors.append(f"apps[{app_id}].{field}: silent identity change is forbidden")
        for field in MIGRATION_LINK_FIELDS:
            if field in old and old[field] != new.get(field):
                errors.append(
                    f"apps[{app_id}].{field}: established migration link cannot be removed or retargeted"
                )
    return errors


def validate(document, schema, base=None):
    errors = validate_schema(document, schema)
    if errors:
        return errors
    errors.extend(validate_semantics(document))
    if base is not None:
        base_errors = validate_schema(base, schema)
        if base_errors:
            return [f"base revision: {error}" for error in base_errors]
        errors.extend(validate_base(document, base))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    base_source = parser.add_mutually_exclusive_group()
    base_source.add_argument("--base-file", type=Path)
    base_source.add_argument("--base-revision")
    args = parser.parse_args()
    try:
        document = load_json_file(args.registry)
        schema = load_json_file(args.schema)
        jsonschema.Draft202012Validator.check_schema(schema)
        if args.base_file:
            base = load_json_file(args.base_file)
        elif args.base_revision:
            base = load_base_revision(args.base_revision)
        else:
            base = None
        errors = validate(document, schema, base)
    except (OSError, ValueError, jsonschema.SchemaError) as error:
        print(str(error))
        return 1
    for error in errors:
        print(error)
    if errors:
        return 1
    base_input = args.base_revision or args.base_file
    suffix = f" against {base_input}" if base_input else ""
    print(f"Registry valid{suffix}: {args.registry}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
