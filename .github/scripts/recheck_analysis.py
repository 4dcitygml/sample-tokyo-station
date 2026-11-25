# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Re-run the read-only PR analysis when the proposer or a maintainer asks for it from the hub.

Trusted job (issue_comment). PR code is neither checked out nor executed here; the
request only re-runs the latest analysis run of the PR's head, whose poster then
publishes the report again.
"""
import os

import github_api as gh
import texts
from operator_explanation import latest_run

MAINTAINER = ("OWNER", "MEMBER", "COLLABORATOR")


def reply(repo, number, key):
    text = texts.language(gh.city_language(repo))[key]
    gh.checked(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": text})


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    event = gh.event()
    number = event["issue"]["number"]
    comment = event["comment"]
    pr = gh.checked(f"/repos/{repo}/pulls/{number}")
    if pr["state"] != "open":
        print("PR is closed; nothing to re-inspect")
        return
    if comment["user"]["login"] != pr["user"]["login"] and comment.get("author_association") not in MAINTAINER:
        reply(repo, number, "recheck_not_allowed")
        return
    try:
        latest = latest_run(gh.api, repo, pr)
    except RuntimeError:
        reply(repo, number, "recheck_no_record")
        return
    if latest.get("status") != "completed":
        reply(repo, number, "recheck_running")
        return
    gh.checked(f"/repos/{repo}/actions/runs/{latest['id']}/rerun", "POST")
    reply(repo, number, "recheck_started")


if __name__ == "__main__":
    run()
