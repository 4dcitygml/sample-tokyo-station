# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Trusted default-branch job. Reads GitHub data only; never executes PR code."""
import os

import github_api as gh
import texts
from operator_explanation import evaluate

# A pull request that changes CI (anything under .github/, the tools pin included) runs its
# own analysis workflow, so a green analysis proves nothing about it. It needs the
# maintainer's `tooling` label, set after reading the change, before the report can count.
WORKFLOW_LABEL = "tooling"
# The ci-report title for each reason of a red check; any other reason is "waiting".
TITLES = {"fix": "check_fix", "system": "check_system", "workflow-change": "check_workflow_change"}


def changes_workflows(repo, pr):
    if WORKFLOW_LABEL in {label["name"] for label in pr.get("labels", [])}:
        return False
    files = gh.pages(f"/repos/{repo}/pulls/{pr['number']}/files")
    return any(name.startswith(".github/")
               for f in files for name in (f.get("filename", ""), f.get("previous_filename") or ""))


def named(prs):
    """The open PRs the triggering event names: one PR for a PR event, every open PR for a
    push or a manual run. (After a report, the poster verifies its PR itself.)"""
    event = gh.event() if os.environ.get("GITHUB_EVENT_PATH") else {}
    if "pull_request" in event:
        return [pr for pr in prs if pr["number"] == event["pull_request"]["number"]]
    return prs


def verify(repo, pr, heads):
    """Write the PR head's ci-report: the one place that judges it, called by review-report.yml
    and by the poster right after it published a report. True when the verdict was written."""
    number, sha = pr["number"], pr["head"]["sha"]
    check = gh.open_check(repo, sha, external_id=f"pr:{number}")
    try:
        result = evaluate(gh.api, repo, pr)
        # Checks attach to commits, not PRs. Never share a successful gate
        # between two PRs that happen to have the same head commit.
        if heads[sha] != 1:
            result = {"valid": False, "reason": "duplicate-head"}
        elif changes_workflows(repo, pr):
            result = {"valid": False, "reason": "workflow-change"}
        current, same = gh.same_pr(repo, pr)
        if not same or current["state"] != "open":
            result = {"valid": False, "reason": "head-changed"}
        valid = result["valid"]
        # The title names the reason in the city's language; the summary keeps the reason code.
        text = texts.language(gh.city_language(repo))
        title = text["check_current" if valid else TITLES.get(result["reason"], "check_waiting")]
        gh.close_check(repo, check, valid, title,
                       f"PR #{number}, head {sha}. Result: {result['reason']}. "
                       + (f"The PR changes files under .github/, so its own analysis workflow ran: a maintainer "
                          f"reads the change and sets the `{WORKFLOW_LABEL}` label before the report counts. "
                          if result["reason"] == "workflow-change" else "")
                       + "Reviewers use the shared report and GitHub Approve. Approval counts are configured in GitHub.",
                       external_id=result.get("reportId", "none"))
        return True
    except Exception:
        # Record the failure. If even that API call fails, the error propagates and the
        # check stays in progress: a missing result must never be promoted to success.
        gh.close_check(repo, check, False, "Report verification unavailable", "Retry the trusted workflow.")
        return False


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    prs, heads = gh.open_heads(repo)
    errors = [pr["number"] for pr in named(prs) if not verify(repo, pr, heads)]
    if errors:
        raise RuntimeError(f"Report verification unavailable for PRs {errors}")


if __name__ == "__main__":
    run()
