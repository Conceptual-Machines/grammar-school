#!/usr/bin/env python3
"""Script to update version across all files."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def update_version(new_version: str) -> None:
    """Update version in all relevant files."""
    files_to_update = [
        ("VERSION", new_version),
        ("python/pyproject.toml", f'version = "{new_version}"'),
        ("python/grammar_school/version.py", f'__version__ = "{new_version}"'),
        ("go/gs/version.go", f'const Version = "{new_version}"'),
    ]

    for file_path, new_content in files_to_update:
        file = ROOT / file_path
        if not file.exists():
            print(f"Warning: {file_path} not found, skipping")
            continue

        content = file.read_text()

        if file_path == "VERSION":
            file.write_text(new_version + "\n")
        elif file_path == "python/pyproject.toml":
            content = re.sub(r'^version = ".*"', f'version = "{new_version}"', content, flags=re.MULTILINE)
            file.write_text(content)
        elif file_path == "python/grammar_school/version.py":
            content = re.sub(r'^__version__ = ".*"', f'__version__ = "{new_version}"', content, flags=re.MULTILINE)
            file.write_text(content)
        elif file_path == "go/gs/version.go":
            content = re.sub(r'const Version = ".*"', f'const Version = "{new_version}"', content)
            content = re.sub(r'Version: ".*",', f'Version: "{new_version}",', content)
            file.write_text(content)

        print(f"Updated {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/update_version.py <version>")
        print("Example: python scripts/update_version.py 0.2.0")
        sys.exit(1)

    version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"Error: Invalid version format: {version}")
        print("Version must be in format: MAJOR.MINOR.PATCH (e.g., 0.2.0)")
        sys.exit(1)

    update_version(version)
    print(f"\nVersion updated to {version}")
