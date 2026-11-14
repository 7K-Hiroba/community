import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_markdown_links.py"


class MarkdownLinkTests(unittest.TestCase):
    def run_validator(self, files):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_valid_reference_angle_and_linked_heading_anchor(self):
        result = self.run_validator(
            {
                "README.md": (
                    "[inline](target.md#release-notes)\n"
                    "[reference][target]\n"
                    "[angle](<other file.md>)\n\n"
                    "[target]: target.md#release-notes\n"
                ),
                "target.md": "# [Release](https://example.invalid) notes\n",
                "other file.md": "# Other\n",
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_defined_reference_target(self):
        result = self.run_validator(
            {"README.md": "[broken][target]\n\n[target]: missing.md\n"}
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("missing.md", result.stdout + result.stderr)

    def test_missing_angle_target_with_space(self):
        result = self.run_validator({"README.md": "[broken](<missing file.md>)\n"})
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("missing file.md", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
