"""Pytest integration for adversarial security and quality review."""

import subprocess
import sys
from pathlib import Path


def test_adversarial_security_and_quality():
    """Runs adversarial_review.py and asserts return code 0."""
    repo_root = Path(__file__).resolve().parent.parent
    script_path = repo_root / "adversarial_review.py"

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    assert result.returncode == 0, f"Adversarial review failed:\n{result.stderr or result.stdout}"
