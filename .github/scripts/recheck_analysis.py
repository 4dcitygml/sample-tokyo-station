# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Re-run the read-only PR analysis when the proposer or a maintainer asks for it from the hub.

Trusted job (issue_comment). PR code is neither checked out nor executed here; the
request only re-runs an existing analysis run or re-dispatches a trusted workflow.
"""
import os

import github_api as gh
import texts
from operator_explanation import latest_run

MAINTAINER = ("OWNER", "MEMBER", "COLLABORATOR")
RETRY = {"<!-- citygml-retry-workflow:pr-comment.yml -->": "pr-comment.yml",
         "<!-- citygml-retry-workflow:review-report.yml -->": "review-report.yml"}


def has_artifact(repo, run):
    """Whether the analysis run still holds the artifact the poster publishes (kept 3 days)."""
    listing = gh.checked(f"/repos/{repo}/actions/runs/{run['id']}/artifacts")
    return any(a.get("name") == "pr-comments" and not a.get("expired") for a in listing.get("artifacts", []))


def reply(repo, number, key):
    text = texts.language(gh.city_language(repo))[key]
    gh.checked(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": text})


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    event = gh.event()
    number = event["issue"]["number"]
    default_branch = event["repository"]["default_branch"]
    comment = event["comment"]
    pr = gh.checked(f"/repos/{repo}/pulls/{number}")
    if pr["state"] != "open":
        print("PR is closed; nothing to re-inspect")
        return
    if comment["user"]["login"] != pr["user"]["login"] and comment.get("author_association") not in MAINTAINER:
        reply(repo, number, "recheck_not_allowed")
        return
    workflow = next((w for mark, w in RETRY.items() if mark in comment.get("body", "")), "pr-analysis.yml")
    if workflow == "review-report.yml":
        gh.checked(f"/repos/{repo}/actions/workflows/{workflow}/dispatches", "POST", {"ref": default_branch})
        return
    try:
        latest = latest_run(gh.api, repo, pr)
    except RuntimeError:
        reply(repo, number, "recheck_no_record")
        return
    if latest.get("status") != "completed":
        reply(repo, number, "recheck_running")
        return
    if workflow == "pr-comment.yml" and has_artifact(repo, latest):
        gh.checked(f"/repos/{repo}/actions/workflows/{workflow}/dispatches", "POST",
                {"ref": default_branch, "inputs": {"analysis_run_id": str(latest["id"])}})
    else:
        # A fresh analysis also republishes: its artifact is new and the poster follows it.
        gh.checked(f"/repos/{repo}/actions/runs/{latest['id']}/rerun", "POST")
    reply(repo, number, "recheck_started")


if __name__ == "__main__":
    run()
