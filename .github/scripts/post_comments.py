# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Trusted posting side of the two-workflow scheme: the detail comments, then the report.

Runs on the default branch with pull-requests:write after pr-analysis.yml (untrusted,
read-only) uploaded its artifact. The artifact is data: Markdown and JSON are read, never
executed, and every name, size and comment marker is fixed here, so untrusted artifact
data cannot select another bot comment to overwrite.
"""
import json
import os
import sys
from pathlib import Path

import check_review_report
import github_api as gh
import publish_review_report
from operator_explanation import currency

OUT = Path("out")
ANALYSIS_WORKFLOW = ".github/workflows/pr-analysis.yml"
# Artifact file -> the fixed marker its comment starts with. Files not listed here are
# dropped with a warning: a newer analysis workflow (from a PR branch) may upload files
# this trusted side (from main) does not know yet, and a CI change must land trusted
# side first without a red run in between (operator handbook 6.7).
MARKERS = {
    "commit-scope.md": "<!-- citygml-commit-scope -->",
    "preview.md": "<!-- cesium-building-preview -->",
    "summary.md": "<!-- citygml-change-summary -->",
    "lint.md": "<!-- citygml-reviewability-lint -->",
    "citygml_lint.md": "<!-- citygml-quality-lint -->",
    "plausibility_lint.md": "<!-- plausibility-lint -->",
    "val3dity.md": "<!-- val3dity-topology-gate -->",
    "metadata.md": "<!-- citygml-metadata -->",
    "reproduction.md": "<!-- citygml-bulk-reproduction -->",
    "commit.md": "<!-- citygml-suggested-commit -->",
    # The list of all checks and the auto-resubmission state (active/resolved) also update the same comments.
    "inspection.md": "<!-- citygml-automatic-inspection -->",
    "resubmission.md": "<!-- citygml-auto-resubmission -->",
}
DATA_FILES = ("inspection.json", "pr.txt")      # read by this side and by the report publisher
ARTIFACT_LIMIT = 4194304                        # bytes; larger files are never posted
COMMENT_LIMIT = 60000                           # bytes; GitHub rejects bodies over 65,536 characters
TRUNCATED = ("\n<sub>⚠️ Truncated to fit the GitHub comment size limit; "
             "the full report is in the pr-comments artifact of the analysis run (kept for 3 days).</sub>\n")


def fail(message):
    print(f"::error::{message}")
    sys.exit(1)


def analysis_run(repo, run_id):
    """The completed PR analysis run whose artifact is being posted; refused otherwise."""
    if not run_id.isdigit() or run_id.startswith("0"):
        fail("Invalid analysis run id.")
    run = gh.checked(f"/repos/{repo}/actions/runs/{run_id}")
    # A cancelled run (superseded by a newer one, or stopped by a person) has no result to publish.
    if (run.get("event") != "pull_request" or run.get("path", "").split("@")[0] != ANALYSIS_WORKFLOW
            or run.get("status") != "completed" or run.get("conclusion") == "cancelled"):
        fail("Not a completed PR analysis run")
    return run


def pr_number():
    if not (OUT / "pr.txt").is_file():
        fail("The analysis artifact carries no pr.txt.")
    number = (OUT / "pr.txt").read_text().strip()
    if not number.isdigit() or number.startswith("0"):
        fail("Invalid PR number in the analysis artifact.")
    return int(number)


def matching_pr(repo, number, run):
    """The PR number carried by the artifact is accepted only after its head SHA and head
    repository match the analysis run and the current GitHub API record."""
    pr = gh.checked(f"/repos/{repo}/pulls/{number}")
    if (pr.get("state") != "open" or pr["head"]["sha"] != run["head_sha"]
            or (pr["head"].get("repo") or {}).get("full_name") != run["head_repository"]["full_name"]):
        fail("Artifact metadata does not match the open PR that triggered this workflow run.")
    return pr


def truncated(data):
    """The leading part of an oversize Markdown body: whole lines only, a dangling code
    fence closed, and a pointer at the full report in the artifact."""
    lines = data[:COMMENT_LIMIT].split(b"\n")
    if data[:COMMENT_LIMIT].endswith(b"\n"):
        lines.pop()                      # the split left an empty tail after the final newline
    kept = b"".join(line + b"\n" for line in lines[:-1])
    if sum(line.startswith(b"```") for line in kept.split(b"\n")) % 2:
        kept += b"```\n"
    return kept + TRUNCATED.encode()


def accepted_files():
    """Artifact files this side knows, sized and truncated for posting; the rest removed."""
    if any(p.is_symlink() for p in OUT.rglob("*")):
        fail("Symlinks are not accepted in the analysis artifact.")
    files = {}
    for path in sorted(p for p in OUT.rglob("*") if p.is_file()):
        name = path.relative_to(OUT).as_posix()
        if name not in MARKERS and name not in DATA_FILES:
            print(f"::warning::Ignoring an artifact file this poster does not know: {path}")
            path.unlink()
            continue
        size = path.stat().st_size
        if size == 0:
            # An empty body is no comment (an analyzer step that could not write its report);
            # skip it so the other comments and the report are still published.
            print(f"::warning::Skipping an empty artifact file: {path}")
            path.unlink()
            continue
        if size > ARTIFACT_LIMIT:
            fail(f"Artifact file is too large to post safely: {path}")
        if name in MARKERS and size > COMMENT_LIMIT:
            # Bulk PRs (source baselines, annual source updates) legitimately produce long
            # reports; keep the leading part and point at the artifact instead of failing.
            path.write_bytes(truncated(path.read_bytes()))
            print(f"truncated for posting: {path} ({size} bytes)")
        files[name] = path
    return files


def post(repo, number, files, comments):
    """Upsert each comment independently by its fixed marker (mutually non-destructive)."""
    for name, marker in MARKERS.items():
        if name not in files:
            continue
        body = files[name].read_bytes().decode(errors="replace")
        if body.split("\n", 1)[0] != marker:
            fail(f"Unexpected comment marker in {files[name]}")
        existing = gh.find_comment(comments, marker)
        updated = gh.upsert_comment(repo, number, body, existing)
        print(f"updated: {files[name]} (comment {existing['id']})" if updated else f"created: {files[name]}")


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    analysis = analysis_run(repo, os.environ["ANALYSIS_RUN"])
    number = pr_number()
    pr = matching_pr(repo, number, analysis)
    files = accepted_files()
    inspection = json.loads((OUT / "inspection.json").read_text())
    # The one judgement of the contract (A10): is this run's inspection the current report of
    # the PR as GitHub holds it now?
    pr, reason = currency(gh.api, repo, pr, {"context": inspection.get("context") or {"head": None},
                                             "runId": analysis["id"], "runAttempt": gh.attempt(analysis)})
    if reason == "report-stale":
        # The event an analysis reads can carry an older PR than GitHub holds by the time it
        # is posted (a PR reopened after main moved gets a new base). Run the analysis once
        # more; a second stale result fails as before.
        if gh.attempt(analysis) == 1:
            gh.checked(f"/repos/{repo}/actions/runs/{analysis['id']}/rerun", "POST")
            print("The inspection describes an older state of the PR; the analysis runs again.")
            return
        fail("Inspection context is stale")
    if reason != "current":
        # report-pending: a newer analysis of the same head supersedes this one; posting would
        # overwrite its comments with older results. duplicate-head: checks attach to commits,
        # not PRs, so nothing is posted. head-changed: the PR moved on.
        fail({"report-pending": "Superseded run",
              "duplicate-head": "Multiple open PRs share this head; checks cannot distinguish them"}.get(reason, reason))
    comments = gh.bot_comments(repo, number)
    post(repo, number, files, comments)
    report = publish_review_report.publish(repo, pr, analysis, comments)
    # The PR's ci-report judges the report just published (the same check as review-report.yml).
    if not check_review_report.verify(repo, pr, report):
        fail("Report verification unavailable")


if __name__ == "__main__":
    run()
