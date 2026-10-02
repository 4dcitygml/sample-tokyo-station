<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Operator handbook

- For: members of the city's `operators` team — a contractor, or 4dcitygml
  while it acts as operator
- Contract: [Pull request operations](pr-operations.md) · The city's side:
  [Approver's guide](approver-guide.md) · Bulk submissions:
  [provenance, verification, and merge policy](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md)

The documents of this repository are maintained in English only; residents meet their own language in the editing tools and in the texts CI posts. The one exception is the data contribution policy, the consent text the pull request templates link: it has Japanese and German translations, and the English text governs.

This handbook covers preparing proposals, handling questions, merging approved
changes, releases and tool maintenance. These operational responsibilities do
not define a separate approval stage. If authorized as a reviewer, read the same
CI report as every other reviewer and use GitHub Approve. One person may combine
operational and city-review responsibilities in one account.

## 1. Making a PR by hand

The editing tools create one branch, one commit with a `Building:` trailer and
one PR per building, and satisfy everything below by construction. Use this
section when you make a PR without them.

### 1.1 Before starting

```text
[ ] Decided the starting point: an issue, an official source, a resident's proposal, or scheduled maintenance
[ ] Identified the target city, building ID, mesh, and change type
[ ] The evidence can be published, with no license / personal-information / privacy problems
[ ] No earlier open PR changes the same mesh GML
[ ] The boundary between this PR and other PRs is decided
```

PRs that change the same mesh GML are serialized: create the next PR from
main after the earlier one merges. Different meshes may proceed in parallel
only when shared schema migrations are done and no shared textures or XLinks
are touched.

### 1.2 Branch and commits

```text
[ ] Created the working branch (or fork) from the latest main at start time
[ ] The PR history is linear, with no merge commits inside the branch
[ ] Each normal-update commit changes exactly one buildingID
[ ] The same buildingID is not split across commits within the PR
[ ] Building commits are ordered by ascending building ID
[ ] Building:, Building-Added:, Building-Deleted: trailers match the actual change
[ ] Formatting-only diffs outside the target are removed with the minimal-diff version
```

Use GitHub Draft while the proposal is still being prepared; CI also runs on
Drafts. The proposer marks it Ready when ready to request review. The editing
tools use the standard PR flow. No operator confirmation automatically changes
the PR stage. The hub offers approval after the applicable checks and current
report succeed.

### 1.3 PR body

```text
[ ] Picked exactly one PR type
[ ] Wrote what changes, why, and on what evidence
[ ] Listed every target buildingID, or the manifest
[ ] Stated the allowed paths and what must not change
[ ] Linked related issues with Fixes #<number> or Refs #<number>
[ ] Added evidence URLs, document names, retrieval dates, editions, hashes
[ ] If shape, LOD, attributes, IDs, and lifecycle are mixed, explained why they cannot be separated
```

### 1.4 Before marking Ready for review

```text
[ ] All required checks are green on the head SHA of the final push (base freshness included)
[ ] Warnings and notices were read; where one is left as is, the reason is written in the PR
[ ] After a churn notice, the minimal-diff version was applied and rechecked
[ ] The current CI report is available for all reviewers (§3)
```

Churn handling currently stops at notification and generating the minimal-diff
version; apply it yourself until automatic application exists.

## 2. When one issue touches several buildings

The typical case: an issue arrives with one document (a survey, a published
list, a corrected register) that affects several buildings. There are exactly
two routes for ordinary corrections, and the count decides nothing:

- **One building, one PR.** Reproduce the finding for a building and open its
  PR (the editing tools do this in a few clicks). Ten buildings are ten PRs;
  each carries the same evidence link. The city approves each with one click
  from the hub's queue.
- **Reproducible, one bulk submission.** When the correction is a mapping
  ("value X in the document → attribute Y"), express it as data: the
  document as a material with its hash, a mapping table, and the command that
  applies it. That is a bulk submission — provenance manifest, accepted by
  reproduction, sampled by the city — whether it touches three buildings or
  three thousand (see the bulk-submission document; the kind that takes an
  arbitrary external dataset as material is pending in the tools).

A rebuild, split or merge instead follows the dedicated one-event route (§6.2).
It is reviewed as one real-world event involving old and new buildings.

A hand-made PR with unrelated building commits and no manifest is neither: it
cannot be reviewed by reproduction and is too large to be read as one change.
Do not open one; if you inherit one, split it per building.

Examples: 12 buildings from the city's shelter list, verified one by one → 12
PRs; the same list joined by script → one bulk submission; storeys of 5
buildings from a different document each → 5 PRs; one document correcting
storeys and the footprint of one building → one attribute PR and one geometry PR.

## 3. Reviewing the shared CI report

CI generates change, proposer-supplied evidence, check results, impact and
recommendation. It sends correction instructions automatically. Reviewers check
the common report and comparisons and use GitHub Approve or Request changes.
There is no separate human transcription, operator confirmation button, or
operator-explanation required check.

The machine report must match the current PR and CI run. Its generation or
delivery failure cannot be replaced by a handwritten result. `ci-report` is
judged in one place (`check_review_report.verify`): the poster calls it right after
it published a report, and `review-report.yml` on every PR update, push to `main` and
manual run; its summary names the reason: `current` (the report is valid and
passes), `fix` or `system` (a current report that asks the proposer for a fix, or
an incomplete run), `report-pending` (no report for the latest analysis yet),
`report-stale` (the PR changed after the report), `report-unavailable` (no readable
report), `workflow-change` (a `.github/` change without the `tooling` label),
`duplicate-head`, `head-changed`. `analyze` and
`ci-report` remain required checks; human approval requirements belong to GitHub.
A CI rerun does not itself dismiss human approvals. GitHub's configured stale
review, Code Owner and last-push rules decide whether approvals remain effective.

The city can change its required approval count over time; GitHub enforces it.
The hub shows each reviewer whether they approved, not how many approvals remain.
[Review settings](review-settings.md) describe the details.


## 4. Merge

The ruleset requires `analyze` and `ci-report` from GitHub Actions, the current
approval count, resolved conversations, and any additional conditions set by the city. You confirm only:

```text
[ ] "Create a merge commit" for city-data PRs (documentation and tooling PRs may squash)
[ ] The current machine report is available and GitHub reports the configured requirements as satisfied
```

No auto-merge. An emergency admin bypass is reserved for the city's owner,
with the reason recorded in an issue.

## 5. After merge

```text
[ ] Checks and the Pages history index on main succeeded
[ ] For annual updates, the release-plan state was updated
[ ] On anomalies, a revert PR was opened — history is never rewritten
```

No follow-up commits that write merged PR numbers or SHAs into a manifest;
the Pages index is regenerated from git history and GitHub.

## 6. PR types you handle day to day

The full table of types is in the contract (§3). The types below are yours;
`identity-correction`, `source-update`, `carry-forward`, `schema-update` and
`schema-migration` are bulk submissions made by the machine account and are
specified in the bulk-submission document.

### 6.1 `correction`

```text
[ ] There is a data-issue or publishable evidence
[ ] The PR has exactly one building commit with one Building: <building ID>
[ ] Texture replacement was done by adding new images + updating imageURI
[ ] After geometry changes, derived attributes (height, area, …) were checked for consistency
```

Overwriting an existing texture under the same name is forbidden in
principle. Only for legitimate exceptions (shared atlases etc.), after
checking every affected building, apply the `texture-override` label and let
the city approve.

### 6.2 `lifecycle`

One rebuild, split or merge is one PR with one dedicated commit. Multiple IDs
are expected: old A + B → new C can be one rebuilding event.

```text
[ ] The old/new relationship is supported by evidence; unresolved candidates stay in an issue
[ ] A single provenance/lifecycle/<event>.json records kind, oldIds, newIds, reason, confirmedOn and evidence
[ ] Change-Type: lifecycle and its SHA-256 Lifecycle-Manifest reference are recorded
[ ] Building-Deleted:, Building-Added: and Building: each match their actual change category
[ ] No unrelated building changes, other event records or other commits are included
[ ] CI's report describes the old/new relation and evidence; the city judges the actual relationship
```

CI validates the event record and its relationship to the data. It does not prove
that the declared buildings really belong to one event. A `lifecycle` label alone
is not evidence or approval. The normal applicable data checks still run.

See [event format, example and validation command](https://github.com/4dcitygml/tools/blob/main/docs/lifecycle-events.md).
This route needs the new tools release and a pilot test. The editing screens do
not yet create these events. If the relationship is unclear, retain an issue or
`lifecycle-review`; do not guess that a building was demolished or rebuilt.

### 6.3 `layout`

```text
[ ] Confirmed before the update that a stored GML would reach 50 MiB or more
[ ] Subdivided only the current mesh on pre-update main, by exactly one level
[ ] Recorded Change-Type: layout, with no building-ID trailer
[ ] Building count, ID set, semantic hash, Appearance, and XLink are unchanged
[ ] Envelope, XSD, and temporary re-aggregation checks pass
[ ] All files after subdivision are under 50 MiB, with no tracked file at 100 MiB or more
```

A once-subdivided mesh is never merged back to a coarser mesh. The current
tool supports one subdivision step.

### 6.4 `texture-gc`

```text
[ ] Every deletion candidate is unreferenced by all imageURIs on main
[ ] Zero new dangling references
[ ] The deletion list, count, and byte size are recorded in the PR body
[ ] No building GML, attributes, or geometry change in the same PR
```

### 6.5 `revert` and urgent fixes

Published mistakes are never hidden by force-push or tag replacement — they
are undone by a new PR.

```text
[ ] Decided whether to revert one building commit or the whole PR
[ ] Recorded the target commit or merge commit SHA
[ ] Wrote the reason, how it was found, and the affected buildings and releases
[ ] Ran the full normal checks on the reverted CityGML
[ ] Decided whether a patch release is needed if a published release is affected
```

Even under urgency, required checks and the city's approval are never
skipped. Respond by narrowing the scope and raising the priority.

### 6.6 `tooling` (updating the shared tools)

A `tooling` PR changes `CITYGML_TOOLS_REF` in `.github/workflows/` to the
immutable commit of a published `tools-v` release. That is the only tools
version a city pins: the editing tools on residents' computers (the `hub-v`
client) are not pinned by the city — their version comes from `4dcitygml/tools`
releases, and the hub offers each newer version to its user. CI verifies the
pin against the `tools-v` tags (Exchange Contract A11); any other change under
`.github/` needs the maintainer label `tooling`. Nothing changes until the
city merges the PR.

```text
[ ] The change touches only the CITYGML_TOOLS_REF lines in .github/workflows/ — no data, no documentation
[ ] CI's file-scope row passed (the new commit is a tools-v release; the tags API confirmed it)
[ ] The explanation summarizes the release notes and starts with "no data change"
[ ] If the release changes what CI expects from clients, min_hub in 4dcitygml.json was raised in the same PR
[ ] Squash-merged after the city's approval
```

### 6.7 Changing the CI workflows themselves: two PRs, trusted side first

The city's CI has two sides. The **analysis side** (`pr-analysis.yml`) runs
from the PR's own branch. The **trusted side** (`pr-comment.yml`,
`review-report.yml`, `pr-base-freshness.yml`, `pr-recheck.yml`, everything under
`.github/scripts/`) runs from `main` regardless of what the PR contains — that is what keeps an
untrusted PR from changing how its own report is posted and checked. So a PR
cannot update both sides at once: while it is open, its analysis output is
handled by the trusted side of `main`.

The routine that follows from this:

1. **Trusted side first.** Merge the change to the trusted workflows and
   `.github/scripts/` in its own PR. Written so that it
   accepts both the current and the coming analysis output.
2. **Analysis side second.** Then merge the change to `pr-analysis.yml` or the
   `CITYGML_TOOLS_REF` pin that changes what the analyzer
   produces (new artifact files, new inspection rows).

If both sides go in one PR anyway, the trusted-side run of that PR fails once
("Unexpected artifact file", "Incomplete inspection result"); `analyze` is not
affected, the PR can be merged, and the next PR is clean. Do this knowingly or
not at all — a red check on a maintainer's PR is where residents learn to ignore
red checks.

Two more things every `.github/` PR needs, or `analyze` fails before it looks at
the content:

- the maintainer label **`tooling`** (Exchange Contract A9/A11) — apply it right
  after opening the PR; labeling re-runs the analysis. The label is also what
  lets the report count: a PR that changes anything under `.github/` runs its
  own analysis workflow, so without the label `ci-report` fails with the reason
  `workflow-change`, however green its analysis looks;
- a PR body in this repository's template: PR type "documentation / configuration only",
  the scope line, and a filled **Summary of changes** section (the
  `<!--sec:reason-->` anchor) — the reason check reads that section.

```text
[ ] Trusted-side change (pr-comment / review-report / pr-base-freshness / pr-recheck / .github/scripts) merged in its own PR before the analysis-side change
[ ] Trusted side accepts the current and the coming analysis output
[ ] Label `tooling` applied; PR body in the template structure with the Summary of changes section filled
[ ] After the analysis-side merge: the next data PR shows a green trusted-side run
```

This is GitHub's own model, not a local rule: `workflow_run` workflows run only
from the default branch and `pull_request_target` runs in the base repository's
default-branch context ([events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)),
the two-workflow split with artifacts treated as untrusted input is the pattern
GitHub Security Lab recommends for pull requests from forks
([preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)),
and the [secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
asks `workflow_run` workflows to treat artifacts from other workflows with caution.

### 6.8 CI switch

A copy of this repository used for rehearsing CI changes can stop its automatic
workflow runs with one repository variable, `CITYGML_CI`:

| Value | Effect |
|---|---|
| unset (every city repository) | every workflow runs as written |
| `off` | automatic runs are skipped; `analyze` fails at its first step instead |
| any value, manual dispatch | a workflow that offers `workflow_dispatch` runs: `pr-comment.yml` (publish a given analysis run again), `review-report.yml` and `pr-base-freshness.yml` (check every open PR) |

`analyze` fails rather than skips because it is a required check and GitHub counts
a skipped job as passed; with the switch off no pull request can pass the gate
unanalyzed. Never set the variable on a city repository that takes contributions.


You plan the annual update; the bulk parts are submitted by the machine
account and specified in the bulk-submission document.

1. `schema-update` — the new edition's artifacts (code lists under `codelists/<edition>/`, schema profile), no GML change
2. when the edition changes — either the new official edition as a fresh `source-baseline` followed by `carry-forward`, or, when the repository is the master and no official new-edition file exists, `schema-migration`
3. a single-building pilot per attribute family
4. multi-building PRs per attribute family (`source-update`)
5. dedicated PRs for geometry, LOD, and source `gml:id`
6. `lifecycle` for confirmed events
7. completion checks per mesh and across the city
8. the annual release tag

Never overwrite a whole new-year source in one PR. Adding further themes later
(transportation, flooding, terrain …) has no gate yet; do not add them until
it exists.

## 8. Releases

Release work is yours; **whether to adopt the result as the official edition
is the city's decision** (the repository is the master copy; the official
edition is an output of merged content).

### 8.1 Ordinary fixes

- Merging a PR alone never moves an existing stable release; fixes are
  included in the next scheduled patch or annual release.
- A patch release is made for serious errors, legal / personal-information
  problems, or usage hazards. Tag naming and cadence are fixed in a separate
  ADR before operation starts.

### 8.2 Annual release

```text
[ ] All attribute-family PRs for all target meshes are complete
[ ] Geometry, LOD, source gml:id, and confirmed lifecycle groups are complete
[ ] Schema profile check and, for an edition change, the carry-forward manifest review are complete
[ ] Full buildingID set, duplicates, references, Appearance, and XSD pass
[ ] The final path signature semantically matches the official new-year edition
[ ] Unresolved groups are left untouched, with a hold list and impact stated
[ ] Release notes cover source, hashes, processing, ID unification, holds, and check results
[ ] Tag, Pages, downloads, and check results point at the same commit
[ ] Carried old-codeSpace values (codelists/<edition>/) are counted with carried_codespace_report.py and resolved or accepted by the official channel
[ ] The city's decision to adopt the release as official (date, publication channel) is recorded
```

While any condition is missing, main is never presented as "the stable
new-year edition".

## 9. Periodic checks

### Weekly

```text
[ ] PRs sorted into waiting-for-approval (explained) / waiting-for-explanation / Request changes / waiting-for-latest-main
[ ] CI breakage handled separately from data failures
[ ] Next action or a close reason written on long-stalled PRs
[ ] No conflicting PRs on the same mesh
[ ] A digest of PRs awaiting approval sent to the city, if it prefers digests
```

### Monthly / before scheduled releases

```text
[ ] Candidates for unreferenced textures checked
[ ] New official sources / annual editions and the check date recorded
[ ] Pin of the shared CI tools inspected (CITYGML_TOOLS_REF) and min_hub reviewed; tooling PR decided
[ ] Organization settings reviewed: 2FA required, at least two maintainers, bypass list owners only, audit log read
[ ] Sources, rights, and open questions for the release-target commit confirmed
```

## 10. Changing seats

A new operator (a contractor, or a successor) is invited to the organization
and added to `operators`; the predecessor is removed; the machine account's
token is re-issued; the README's description of the arrangement is updated.
CODEOWNERS and rulesets are not touched. The same steps apply when 4dcitygml
withdraws.
