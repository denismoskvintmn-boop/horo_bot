#!/usr/bin/env python3
"""Format code with black and isort."""

import subprocess
import sys


def main() -> int:
    commands = [
        (["python", "-m", "black", "app/", "tests/", "scripts/"], "Black (formatting)"),
        (["python", "-m", "isort", "app/", "tests/", "scripts/"], "isort (import sorting)"),
    ]

    for cmd, desc in commands:
        print(f"\n{'='*60}")
        print(f"Running: {desc}")
        print("=" * 60)
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode != 0:
            print(f"\n❌ {desc} failed!")
            return 1
        print(f"\n✅ {desc} done!")

    print("\n✅ All formatting complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
