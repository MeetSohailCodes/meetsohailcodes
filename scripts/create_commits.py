#!/usr/bin/env python3
"""Create git commits with specified dates by appending non-empty lines to README.md.

Usage:
  python scripts/create_commits.py            # use default dates
  python scripts/create_commits.py --date 2026-05-13T12:00:00 --date 2026-03-09T12:00:00

Defaults are the dates you requested (assumed year 2026 where ambiguous).
"""
import argparse
import subprocess
import os
from datetime import datetime

DEFAULT_DATES = [
    "2026-05-13T12:00:00",
    "2026-05-07T12:00:00",
    "2026-03-31T12:00:00",
    "2026-03-22T12:00:00",
    "2026-03-24T12:00:00",
    "2026-03-19T12:00:00",
    "2026-03-09T12:00:00",
]


def commit_for_date(date_iso: str, readme_path: str = "README.md"):
    # Append a non-empty, human-friendly line so comments aren't empty
    try:
        dt = datetime.fromisoformat(date_iso)
        display = dt.date().isoformat()
    except Exception:
        display = date_iso

    line = f"Remembering {display} — I miss this day."
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_iso
    env["GIT_COMMITTER_DATE"] = date_iso

    subprocess.run(["git", "add", readme_path], check=True, env=env)
    subprocess.run([
        "git",
        "commit",
        "-m",
        f"Add memory line for {display}",
    ], check=True, env=env)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", "-d", action="append", help="ISO date(s) to use for commits")
    p.add_argument("--file", "-f", default="README.md", help="File to append to (default README.md)")
    args = p.parse_args()

    dates = args.date or DEFAULT_DATES

    for d in dates:
        print(f"Creating commit dated {d} -> appending to {args.file}")
        commit_for_date(d, readme_path=args.file)


if __name__ == "__main__":
    main()
