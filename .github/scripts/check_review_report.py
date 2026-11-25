# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Trusted default-branch job. Reads GitHub data only; never executes PR code."""
import os

import github_api as gh
import texts
from operator_explanation import check_result, currency, read_check

# A pull request that changes CI (anything under .github/, the tools pin included) runs its
# own analysis workflow, so a green analysis proves nothing about it. It needs the
# maintainer's `tooling` label, set after reading the change, before the report can count.
WORKFLOW_LABEL = "tooling"
# The ci-report title of a current report, by its state; workflow-change has its own; any
# other reason is "waiting".
TITLES = {"pass": "check_current", "fix": "check_fix", "system": "check_system"}


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


def title(repo, reason, report):
    """The check's title in the city's language."""
    key = (TITLES[report["state"]] if reason == "current"
           else "check_workflow_change" if reason == "workflow-change" else "check_waiting")
    return texts.language(gh.city_language(repo))[key]


def verify(repo, pr, report=None):
    """Write the PR head's ci-report: the one place that judges it, called by review-report.yml
    (report None: the head's own check carries it) and by the poster with the report it just
    published. True when the verdict was written."""
    check = gh.open_check(repo, pr["head"]["sha"])
    try:
        if report is None:
            report = read_check(check)[1]
            if report and (report.get("repo"), report.get("pr")) != (repo, pr["number"]):
                report = None
        live, reason = currency(gh.api, repo, pr, report)
        if reason not in ("head-changed", "duplicate-head") and changes_workflows(repo, live):
            reason = "workflow-change"
        result = check_result(reason, report)
        gh.close_check(repo, check, result, title(repo, result["reason"], report))
        return True
    except Exception:
        # Record the failure. If even that API call fails, the error propagates and the
        # check stays in progress: a missing result must never be promoted to success.
        gh.close_check(repo, check, check_result("unavailable", None), "Report verification unavailable")
        return False


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    errors = [pr["number"] for pr in named(gh.pages(f"/repos/{repo}/pulls?state=open")) if not verify(repo, pr)]
    if errors:
        raise RuntimeError(f"Report verification unavailable for PRs {errors}")


if __name__ == "__main__":
    run()
