# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Trusted default-branch job. Reads GitHub data only; never executes PR code."""
import json
import os
import urllib.error
import urllib.request
from collections import Counter

from operator_explanation import evaluate, pages, required, context


def api(path, method="GET", payload=None):
    request = urllib.request.Request(
        "https://api.github.com" + path, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                 "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, {}


def checked(path, method="GET", payload=None):
    code, data = api(path, method, payload)
    if code not in (200, 201):
        raise RuntimeError(f"GitHub API failed: HTTP {code}")
    return data


def open_heads(repo):
    """Open PRs and how many of them share each head commit."""
    prs = pages(api, f"/repos/{repo}/pulls?state=open")
    return prs, Counter(pr["head"]["sha"] for pr in prs)


def open_check(repo, sha, **fields):
    """Start the `ci-report` check on a head commit; both trusted jobs report through it."""
    return checked(f"/repos/{repo}/check-runs", "POST",
                   {"name": "ci-report", "head_sha": sha, "status": "in_progress", **fields})


def close_check(repo, check, success, title, summary, **fields):
    checked(f"/repos/{repo}/check-runs/{check['id']}", "PATCH", {
        "status": "completed", "conclusion": "success" if success else "failure",
        "output": {"title": title, "summary": summary}, **fields,
    })


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    if not required(repo):
        return
    prs, heads = open_heads(repo)
    errors = []
    for pr in prs:
        number, sha = pr["number"], pr["head"]["sha"]
        check = open_check(repo, sha, external_id=f"pr:{number}")
        try:
            result = evaluate(api, repo, pr)
            # Checks attach to commits, not PRs. Never share a successful gate
            # between two PRs that happen to have the same head commit.
            if heads[sha] != 1:
                result = {"valid": False, "reason": "duplicate-head"}
            current = checked(f"/repos/{repo}/pulls/{number}")
            if context(current) != context(pr) or current["state"] != "open":
                result = {"valid": False, "reason": "head-changed"}
            valid = result["valid"]
            close_check(repo, check, valid,
                        "Current CI report available" if valid else "Waiting for current CI report",
                        f"PR #{number}, head {sha}. Result: {result['reason']}. "
                        "Reviewers use the shared report and GitHub Approve. Approval counts are configured in GitHub.",
                        external_id=result.get("reportId", "none"))
        except Exception:
            # Record the failure and go on to the next PR. If even that API call
            # fails, the error propagates and the check stays in progress: a
            # missing result must never be promoted to success.
            errors.append(number)
            close_check(repo, check, False, "Report verification unavailable", "Retry the trusted workflow.")
    if errors:
        raise RuntimeError(f"Report verification unavailable for PRs {errors}")


if __name__ == "__main__":
    run()
