# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""The practice reset's reading of the city (manual-reset.yml; practice cities only).

    python3 .github/practice/practice_reset.py dirs    the data directories, one per line
    python3 .github/practice/practice_reset.py close   after the reset is merged: close the open
                                                       proposals that change nothing but them

Runs from a checkout of main. PR code is neither checked out nor executed.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import github_api as gh  # noqa: E402
import texts  # noqa: E402


def data_dirs():
    """data_dirs in 4dcitygml.json, plus provenance/ (the repository scope gate counts both as
    data); none when the city declares no data_dirs."""
    config = json.loads(Path("4dcitygml.json").read_text(encoding="utf-8"))
    dirs = [d.strip("/") for d in config.get("data_dirs") or [] if isinstance(d, str) and d.strip("/")]
    return list(dict.fromkeys(dirs + ["provenance"])) if dirs else []


def close(repo, dirs):
    """Close every open PR whose files (old names of renames included) all lie in `dirs`, with
    the note in the city's language: the merged reset replaced exactly those files."""
    note = texts.language(gh.city_language(repo))["reset_closed"]
    for pr in gh.pages(f"/repos/{repo}/pulls?state=open"):
        number = pr["number"]
        paths = [p for f in gh.pages(f"/repos/{repo}/pulls/{number}/files")
                 for p in (f["filename"], f.get("previous_filename")) if p]
        if not all(any(p.startswith(d + "/") for d in dirs) for p in paths):
            print(f"kept PR #{number}: it changes files outside the data directories")
            continue
        gh.checked(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": note})
        gh.checked(f"/repos/{repo}/pulls/{number}", "PATCH", {"state": "closed"})
        print(f"closed PR #{number}")


def run():
    dirs = data_dirs()
    if sys.argv[1] == "dirs":
        sys.stdout.write("".join(d + "\n" for d in dirs))
    elif dirs:
        close(os.environ["GITHUB_REPOSITORY"], dirs)


if __name__ == "__main__":
    run()
