<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Review settings

All reviewers read the same CI report and use GitHub Approve. The city chooses
eligible reviewers and may change the required approval count whenever its
staffing or contracts change. An authorized administrator records the change
date, old/new count and reason in an issue or the operations record. GitHub's
ruleset audit trail records the setting change; the explanatory record supplies
its operational context. Treat existing open PRs as subject to current settings.

Use the intended number of participating reviewers as the starting point for the
required count. Exclude the PR author, who cannot approve their own proposal.
Accounts with write access are not automatically the intended review group.
One account counts once even if it covers several responsibilities. Arrange
coverage or revise the requirement if the available reviewers change.

A count of two does not require one employee and one supervisor. If a particular
team's participation must be enforced, configure that condition separately,
using the city's GitHub rules and Code Owners. Multiple simultaneous rulesets
and classic protection combine; reducing one setting may leave a stricter rule
in effect elsewhere. Keep applicable data/report checks enabled.

A city repository that takes contributions changes its default branch only
through pull requests: its ruleset has an empty bypass list, administrators
included, so a lowered count or a failing check is never worked around by a
direct push or an override merge. Change the ruleset instead, and record why.

## In the hub

GitHub enforces the required approvals. The hub shows each reviewer whether they
already approved and whether changes were requested; it does not read the
required count and does not show how many approvals remain. The PR page on GitHub
shows whether the approvals, checks and other conditions are met.

## Deployment

This is a local change pending release, city pin updates and a GitHub pilot.
Required machine checks are `analyze` and `ci-report`, issued by GitHub Actions.
Remove the prototype `operator-explanation` requirement and its two workflows;
ship `review-report.yml` and `check_review_report.py` with the current publisher.
The shared Python helper retains its historical filename for portable package
compatibility, but no longer verifies human confirmation records.

Test required counts 1/2/3/4, rule changes while PRs remain open, withdrawal of
reviews and permission changes on GitHub. The hub does not modify GitHub approval
settings on the user's behalf. Keep the city's own permission and release policy.
