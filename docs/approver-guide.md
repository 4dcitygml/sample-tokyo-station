<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Reviewer's guide

City staff and authorized contractors use the same CI report and GitHub Approve.
There is no separate operator confirmation stage. The city determines who can
review and how many approvals are needed, and can change the count over time.

For the full process, read the [processing flow for city staff](processing-flow.md).

## 1. What you confirm

Read the generated change, evidence, checks, impact and recommendation. Check
that the evidence supports the proposed change and that any exception or lifecycle
relationship is justified. CI performs mechanical checks; it does not establish
real-world facts or make the city's adoption decision. Do not rewrite its report.

## 2. Where and how

Read the common report on the PR in GitHub, together with the comparison views.
The hub shows the inspection rows and the checks of each PR and offers Approve and
Request changes; on GitHub, use Files changed → Review changes.
You cannot approve your own PR. One account contributes one approval, even if
that person covers several responsibilities or approves repeatedly.

The hub shows whether you already approved and whether changes were requested;
it does not show how many approvals remain. GitHub enforces the required count.
[Review settings](review-settings.md) explain the difference between counts and
role-specific requirements.

## 3. What the rules check

`analyze` checks the data and `ci-report` verifies current machine evidence.
GitHub enforces the configured approval count, optional Code Owners, stale-review
and last-push requirements, unresolved conversations and other merge conditions.
Reaching the numeric count does not by itself make a PR mergeable; the PR page on
GitHub shows which conditions are still open.

Approvals are ordinary GitHub records. A push may invalidate them according to
the city's configured rules; a CI rerun alone does not automatically dismiss them.
City-data PRs use merge commits to preserve their building commits.

## 4. Notifications and Draft

Draft is the proposer's work-in-progress state. CI also runs on Drafts. The
proposer marks a Draft Ready when requesting review. GitHub's review requests
and Code Owner settings determine notifications.

## 5. When something needs correction

Use Request changes and explain the issue. The proposer fixes it and CI reruns.
Review the new results and Approve if satisfactory. Requests, approvals and
releases remain separate records. An operations contact can handle questions,
merges and releases without being a mandatory first reviewer.

## 6. For the administrator

Maintain team membership and required counts as personnel and contracts change.
Record the change date, old/new count and reason. Plan for enough eligible
reviewers excluding each PR's author, and arrange absence coverage. Roles can be
combined in one account; this never makes one person count twice.
