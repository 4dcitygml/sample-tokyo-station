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
from collections import Counter
from pathlib import Path

import operator_explanation as contract
from operator_explanation import bot, context, latest_run


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


# --- pull requests ---------------------------------------------------------------

def open_heads(repo):
    """Open PRs and how many of them share each head commit."""
    prs = pages(f"/repos/{repo}/pulls?state=open")
    return prs, Counter(pr["head"]["sha"] for pr in prs)


def same_pr(repo, pr):
    """The PR fetched again, and whether its review context is still the one given."""
    current = checked(f"/repos/{repo}/pulls/{pr['number']}")
    return current, context(current) == context(pr)


def is_latest(repo, pr, run):
    """Whether `run` is the latest analysis (id and attempt) of the PR's current head."""
    latest = latest_run(api, repo, pr)
    return (latest["id"], attempt(latest)) == (run["id"], attempt(run))


# --- comments --------------------------------------------------------------------

def bot_comments(repo, number):
    """Every comment the Actions bot left on the PR, oldest first."""
    return [c for c in pages(f"/repos/{repo}/issues/{number}/comments") if bot(c)]


def find_comment(comments, marker, containing=""):
    """The first comment that starts with `marker` (and carries `containing`), or None."""
    return next((c for c in comments
                 if str(c.get("body") or "").startswith(marker) and containing in str(c.get("body") or "")), None)


def upsert_comment(repo, number, body, existing):
    """Replace one earlier bot comment with `body`, or post `body` as a new one."""
    if existing:
        checked(f"/repos/{repo}/issues/comments/{existing['id']}", "PATCH", {"body": body})
    else:
        checked(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": body})
    return bool(existing)


# --- the ci-report check run ------------------------------------------------------

def open_check(repo, sha, **fields):
    """Start the `ci-report` check on a head commit; both trusted jobs report through it.

    One check run per head: an existing `ci-report` is reopened and updated in place,
    so the PR shows one row whose state is always the latest verdict. Creating a new
    run each time left earlier verdicts visible in other check suites.
    """
    listing = checked(f"/repos/{repo}/commits/{sha}/check-runs?check_name=ci-report&filter=all&per_page=100")
    mine = [c for c in listing.get("check_runs", []) if (c.get("app") or {}).get("slug") == "github-actions"]
    if mine:
        check = max(mine, key=lambda c: int(c["id"]))
        checked(f"/repos/{repo}/check-runs/{check['id']}", "PATCH", {"status": "in_progress", **fields})
        return check
    return checked(f"/repos/{repo}/check-runs", "POST",
                   {"name": "ci-report", "head_sha": sha, "status": "in_progress", **fields})


def close_check(repo, check, success, title, summary, **fields):
    checked(f"/repos/{repo}/check-runs/{check['id']}", "PATCH", {
        "status": "completed", "conclusion": "success" if success else "failure",
        "output": {"title": title, "summary": summary}, **fields,
    })
