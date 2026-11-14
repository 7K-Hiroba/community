import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CiConfigurationTests(unittest.TestCase):
    def test_whitespace_check_uses_fetched_base_and_committed_diff(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn("git diff --check origin/main...HEAD", workflow)


if __name__ == "__main__":
    unittest.main()
