#!/usr/bin/env python3
"""Run all linters and formatters."""

import subprocess
import sys


def run_command(cmd: list[str], description: str) -> bool:
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"\n❌ {description} failed!")
        return False
    print(f"\n✅ {description} passed!")
    return True


def main() -> int:
    checks = [
        (
            ["python", "-m", "black", "--check", "app/", "tests/", "scripts/"],
            "Black (code formatting)",
        ),
        (
            ["python", "-m", "isort", "--check-only", "app/", "tests/", "scripts/"],
            "isort (import sorting)",
        ),
        (["python", "-m", "flake8", "app/", "tests/", "scripts/"], "Flake8 (linting)"),
    ]

    failed = []
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            failed.append(desc)

    print("\n" + "=" * 60)
    if failed:
        print(f"❌ Failed checks: {', '.join(failed)}")
        return 1
    print("✅ All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
