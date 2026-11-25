# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""The one GitHub REST client of the trusted-side scripts, and the few records they share.

Scripts call these through the module (`gh.checked(...)`, `gh.pages(...)`) so that one
patched `api` serves every script in tests.
"""
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import operator_explanation as contract
from operator_explanation import bot


def api(path, method="GET", payload=None):
    request = urllib.request.Request(
        "https://api.github.com" + path, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                 "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return response.status, (json.loads(body) if body else {})   # 204: no body
    except urllib.error.HTTPError as error:
        return error.code, {}


def pages(path):
    """Every record of a paged GitHub listing (the contract's reader over this client)."""
    return contract.pages(api, path)


def event():
    """The payload of the event that started this job."""
    return json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())


def checked(path, method="GET", payload=None):
    code, data = api(path, method, payload)
    if code not in (200, 201, 204):
        raise RuntimeError(f"GitHub API failed: HTTP {code}")
    return data


def city_language(repo):
    """The city's language: `lang` in 4dcitygml.json on the default branch; `en` when absent."""
    code, data = api(f"/repos/{repo}/contents/4dcitygml.json")
    if code != 200:
        return "en"
    try:
        return json.loads(base64.b64decode(data.get("content") or "")).get("lang") or "en"
    except (ValueError, TypeError, AttributeError):
        return "en"


def attempt(run):
    return run.get("run_attempt", 1)


# --- comments --------------------------------------------------------------------

def bot_comments(repo, number):
    """Every comment the Actions bot left on the PR, oldest first."""
    return [c for c in pages(f"/repos/{repo}/issues/{number}/comments") if bot(c)]


def find_comment(comments, marker):
    """The first comment that starts with `marker`, or None."""
    return next((c for c in comments if str(c.get("body") or "").startswith(marker)), None)


def upsert_comment(repo, number, body, existing):
    """Replace one earlier bot comment with `body`, or post `body` as a new one."""
    if existing:
        checked(f"/repos/{repo}/issues/comments/{existing['id']}", "PATCH", {"body": body})
    else:
        checked(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": body})
    return bool(existing)


# --- the ci-report check run ------------------------------------------------------

def open_check(repo, sha):
    """Start the `ci-report` check on a head commit; both trusted jobs report through it.

    One check run per head: an existing `ci-report` is reopened and updated in place,
    so the PR shows one row whose state is always the latest verdict. Creating a new
    run each time left earlier verdicts visible in other check suites.
    """
    check = contract.report_check(api, repo, sha)
    if check:
        checked(f"/repos/{repo}/check-runs/{check['id']}", "PATCH", {"status": "in_progress"})
        return check
    return checked(f"/repos/{repo}/check-runs", "POST", {"name": "ci-report", "head_sha": sha, "status": "in_progress"})


def close_check(repo, check, result, title):
    """Complete the check with a verdict of the contract's check_result and its localized title."""
    checked(f"/repos/{repo}/check-runs/{check['id']}", "PATCH", {
        "status": "completed", "conclusion": result["conclusion"], "external_id": result["external_id"],
        "output": {"title": title, "summary": result["summary"], "text": result["text"]},
    })
