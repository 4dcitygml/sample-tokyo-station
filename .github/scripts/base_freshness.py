# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Tell a proposer when main moved on after the PR was created.

Trusted job (pull_request_target and push to main). PR code is neither checked out
nor executed; only GitHub API SHA comparison and comment updates are performed.
"""
import os

import github_api as gh
import texts

MARKER = "<!-- citygml-base-freshness -->"
# The marker and the status line are read by the hub; the text is in the city's language.
ACTIVE = MARKER + "\n<!-- status:active -->\n"
RESOLVED = MARKER + "\n<!-- status:resolved -->\n"


def update_pr(repo, number, text):
    pr = gh.checked(f"/repos/{repo}/pulls/{number}")
    if pr.get("draft"):
        return
    # Compare with the base branch as it is now: the PR's base.sha is the base the PR was
    # created or last updated on, so main having moved since does not show in it.
    code, compare = gh.api(f"/repos/{repo}/compare/{pr['base']['ref']}...{pr['head']['sha']}")
    if code != 200:
        print(f"PR #{number}: could not fetch the comparison with the latest version; will recheck next time")
        return
    behind = compare.get("behind_by")
    if not isinstance(behind, int) or behind < 0:
        print(f"PR #{number}: comparison result unknown; will recheck next time")
        return
    existing = gh.find_comment(gh.bot_comments(repo, number), MARKER)
    if behind > 0:
        gh.upsert_comment(repo, number, ACTIVE + text['freshness_active'].format(behind=behind), existing)
        print(f"PR #{number}: advised merging in the latest version")
    elif existing:
        gh.upsert_comment(repo, number, RESOLVED + text['freshness_resolved'], existing)
        print(f"PR #{number}: confirmed consistency with the latest version")


def run():
    repo = os.environ["GITHUB_REPOSITORY"]
    text = texts.language(gh.city_language(repo))
    # Every run checks every open PR: the repository's queue keeps one pending run, so the
    # run that survives covers the PR events whose runs it replaced.
    for pr in gh.open_heads(repo)[0]:
        update_pr(repo, pr["number"], text)


if __name__ == "__main__":
    run()
