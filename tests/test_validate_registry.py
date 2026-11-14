import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_registry.py"
SCHEMA = ROOT / "registry" / "apps.schema.json"


def app(app_id="argocd", status="reserved"):
    return {
        "id": app_id,
        "repository": f"https://github.com/7K-Hiroba/{app_id}",
        "maintainers": [f"@7K-Hiroba/{app_id}-maintainers"],
        "status": status,
        "dashboardUidPrefix": f"{app_id}-",
        "grafanaFolderSegment": app_id,
    }


def document(apps=None):
    return {"schemaVersion": 1, "apps": apps if apps is not None else [app()]}


class RegistryValidationTests(unittest.TestCase):
    def run_validator(self, current, base="not-json"):
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "apps.json"
            if isinstance(current, str):
                registry.write_text(current, encoding="utf-8")
            else:
                registry.write_text(json.dumps(current), encoding="utf-8")
            command = [
                sys.executable,
                str(SCRIPT),
                "--registry",
                str(registry),
                "--schema",
                str(SCHEMA),
            ]
            if base != "not-json":
                base_path = Path(directory) / "base.json"
                base_path.write_text(json.dumps(base), encoding="utf-8")
                command.extend(["--base-revision", str(base_path)])
            return subprocess.run(command, capture_output=True, text=True, check=False)

    def assert_valid(self, current, base="not-json"):
        result = self.run_validator(current, base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_invalid(self, current, base="not-json", expected=""):
        result = self.run_validator(current, base)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        if expected:
            self.assertIn(expected, result.stdout + result.stderr)

    def test_valid_single_reservation(self):
        self.assert_valid(document())

    def test_valid_five_reservation_repository_fixture(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--registry",
                str(ROOT / "registry" / "apps.json"),
                "--schema",
                str(SCHEMA),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_json_and_schema(self):
        self.assert_invalid("{not-json", expected="JSON")
        changed = document()
        changed["apps"][0]["unexpected"] = True
        self.assert_invalid(changed, expected="unexpected")

    def test_uppercase_and_trailing_hyphen_ids(self):
        for app_id in ["ArgoCD", "argocd-"]:
            with self.subTest(app_id=app_id):
                self.assert_invalid(document([app(app_id)]), expected="id")

    def test_duplicate_and_near_duplicate_ids(self):
        for second_id in ["argocd", "Argocd"]:
            with self.subTest(second_id=second_id):
                self.assert_invalid(document([app(), app(second_id)]), expected="id")

    def test_duplicate_repository(self):
        other = app("monitoring")
        other["repository"] = "https://github.com/7K-Hiroba/argocd"
        self.assert_invalid(document([app(), other]), expected="repository")

    def test_invalid_and_duplicate_maintainers(self):
        invalid = app()
        invalid["maintainers"] = ["@7K-Hiroba/UPPER"]
        self.assert_invalid(document([invalid]), expected="maintainers")
        duplicate = app()
        duplicate["maintainers"].append(duplicate["maintainers"][0])
        self.assert_invalid(document([duplicate]), expected="maintainers")

    def test_prefix_folder_and_repository_mismatch(self):
        for field, value in [
            ("dashboardUidPrefix", "wrong-"),
            ("grafanaFolderSegment", "argo/cd"),
            ("repository", "https://github.com/7K-Hiroba/wrong"),
        ]:
            with self.subTest(field=field):
                changed = app()
                changed[field] = value
                self.assert_invalid(document([changed]), expected=field)

    def test_activation_requires_all_fields(self):
        changed = app(status="active")
        del changed["dashboardUidPrefix"]
        self.assert_invalid(document([changed]), expected="dashboardUidPrefix")

    def test_deleted_active_id(self):
        base = document([app(status="active")])
        self.assert_invalid(document([]), base, expected="active")

    def test_deleted_deprecated_tombstone(self):
        base = document([app(status="deprecated")])
        self.assert_invalid(document([]), base, expected="deprecated")

    def test_old_id_reuse(self):
        base = document([app(status="deprecated")])
        self.assert_invalid(document(), base, expected="deprecated")

    def test_unpaired_rename(self):
        base = document([app(status="active")])
        self.assert_invalid(document([app("argocd-next", status="active")]), base, expected="active")

    def test_silent_repository_prefix_and_folder_edits(self):
        base = document()
        for field, value in [
            ("repository", "https://github.com/7K-Hiroba/argocd-next"),
            ("dashboardUidPrefix", "argocd-next-"),
            ("grafanaFolderSegment", "argocd-next"),
        ]:
            with self.subTest(field=field):
                changed = document()
                changed["apps"][0][field] = value
                self.assert_invalid(changed, base, expected=field)

    def test_migration_cycle(self):
        first = app("argocd", status="deprecated")
        first["replacedBy"] = "monitoring"
        second = app("monitoring", status="deprecated")
        second["replacedBy"] = "argocd"
        self.assert_invalid(document([first, second]), expected="migration")

    def test_unpaired_migration(self):
        old = app(status="deprecated")
        old["replacedBy"] = "argocd-next"
        self.assert_invalid(document([old]), expected="migration")

    def test_valid_paired_migration(self):
        base = document([app(status="active")])
        old = app(status="deprecated")
        old["replacedBy"] = "argocd-next"
        new = app("argocd-next")
        new["migratedFrom"] = "argocd"
        self.assert_valid(document([old, new]), base)

    def test_valid_reserved_to_active_transition(self):
        base = document()
        self.assert_valid(document([app(status="active")]), base)

    def test_invalid_status_transition(self):
        base = document([app(status="active")])
        self.assert_invalid(document(), base, expected="transition")

    def test_initial_base_without_registry_allows_first_addition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Registry Tests"], cwd=root, check=True)
            (root / "README.md").write_text("initial\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "initial"], cwd=root, check=True)
            registry = root / "registry" / "apps.json"
            registry.parent.mkdir()
            registry.write_text(json.dumps(document()), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--registry",
                    str(registry),
                    "--schema",
                    str(SCHEMA),
                    "--base-revision",
                    "HEAD",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
