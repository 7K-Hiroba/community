import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_workflow_pins.py"
FULL_SHA = "11bd71901bbe5b1630ceea73d27597364c9af683"


class WorkflowPinTests(unittest.TestCase):
    def run_validator(self, content: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as directory:
            workflow = Path(directory) / "ci.yml"
            workflow.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), directory],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_accepts_full_sha_and_local_references(self):
        result = self.run_validator(
            "jobs:\n"
            "  test:\n"
            "    steps:\n"
            f"      - uses: actions/checkout@{FULL_SHA} # v4.2.2\n"
            f'      - "uses": actions/checkout@{FULL_SHA} # v4.2.2\n'
            f"      - uses : actions/checkout@{FULL_SHA} # v4.2.2\n"
            f"      - {{uses: actions/checkout@{FULL_SHA}}} # v4.2.2\n"
            "      - uses: ./.github/workflows/local.yml\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_branch_tag_short_sha_and_missing_comment(self):
        cases = {
            "branch": f"actions/checkout@main # {FULL_SHA}",
            "tag": "actions/checkout@v4 # v4",
            "short SHA": f"actions/checkout@{FULL_SHA[:8]} # v4",
            "missing version comment": f"actions/checkout@{FULL_SHA}",
        }
        for name, reference in cases.items():
            with self.subTest(name=name):
                result = self.run_validator(f"steps:\n  - uses: {reference}\n")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("uses:", result.stdout + result.stderr)

    def test_rejects_unpinned_alternate_yaml_key_styles(self):
        cases = {
            "flow mapping": "steps:\n  - {uses: actions/checkout@v4}\n",
            "quoted key": 'steps:\n  - "uses": actions/checkout@v4\n',
            "spaced key": "steps:\n  - uses : actions/checkout@v4\n",
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                result = self.run_validator(content)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("uses:", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
