<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Pull request operations after publication

- Status: adopted procedure for post-publication operation (PR types without
  dedicated CI remain gated until it exists). Third edition: the contract
  only; the seat-specific procedures moved to their own documents.
- Applies to: published city data repositories

This document is the **contract** every pull request follows after
publication: the principles, the seats, the PR types, and the conditions
under which nothing merges. How each seat does its work is in its own
document:

| You are | Read |
|---|---|
| A resident or staff member sending a proposal with the editing tools | [Getting started](getting-started.md) — the tools satisfy this contract for you |
| A member of the city's `maintainers` team (the approver) | [Approver's guide](approver-guide.md) — one page |
| A member of the `operators` team (a contractor, or 4dcitygml as operator) | [Operator handbook](operator-handbook.md) |
| The machine account submitting tool-generated changes | [Bulk submissions: provenance, verification, and merge policy](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md) |

## 1. Principles

1. **1 commit = 1 building ID** is the minimum unit of a normal update (the ID that `building_id` in `4dcitygml.json` names, e.g. `uro:buildingID`).
2. A normal correction PR covers **one building**. Reproducible bulk
   submissions have their own manifest-backed route (principle 7). A rebuild,
   split or merge uses the dedicated **one lifecycle event** route (principle 4).
   Do not bundle unrelated manual corrections into any of these routes.
3. Never split the same buildingID across multiple commits of one PR. It may
   appear again in another PR or another annual attribute family.
4. A building merge, split, or rebuild is one `lifecycle` event handling
   multiple IDs.
5. City-data PRs are merged with a **merge commit, never squashed**, keeping
   each building commit on main. The ruleset allows the `merge` method (plus
   `squash` for documentation); it is never squash-only.
6. Code, documentation, and tooling-update PRs are kept separate from city
   data and may be squash-merged.
7. Changes a script generated from a source or an external dataset are
   **bulk submissions**, regardless of count: a provenance manifest, accepted
   by reproduction. Changes checked and entered by hand are ordinary PRs, read
   in full.
8. **The final approver is always the city** (the `maintainers` team).
   Operators check generated reports and merge; they hold no approval authority. In the
   vocabulary of the Kubernetes OWNERS model: operators are *reviewers*, the
   city's maintainers are *approvers*.
9. A PR where even one building or commit fails a blocking check is not
   partially merged. Blocking failures surface in CI before any human review,
   and the operator checks the generated report and its attention items, so a building
   that "fails" at approval time is a mis-scoped PR, not a case for a split.
10. main may contain work in progress. Regular users are pointed to the
    latest stable release. The official edition is *an output of merged
    content*; whether to adopt it as official is the city's decision.

Language of PR text: the editing tools generate the PR title and body in the
**repository's working language** (`lang` in `4dcitygml.json`); commit subjects,
`Building:` trailers, and branch prefixes stay English/literal (the history and
machine contracts are language-independent). Because city-data PRs merge with a
merge commit (rule 5), the PR title never becomes a history title line on main.
(The practice repos deviate: their pull requests are merged by squash, so the
repo-language PR title does appear in the practice history. A maintainer returns practice data to
its baseline with a manual reset pull request; the history stays.)

```text
Issue / official source / resident's proposal
  → PR with changes and evidence (Draft is optional while work is in progress)
  → automated checks (14 gates)
  → CI generates the shared report and any correction request
  → reviewers use GitHub Approve; current required approval count is configurable
  → operator merges with a merge commit
  → Pages / history index update
  → stable release after the release gate passes → the city adopts it as official
```

## 2. Seats

Review participation is configurable by the city. A reviewer can be a city
employee, a contractor, or someone covering several responsibilities. Everyone
reads the same CI report and uses GitHub **Approve**. There is no required
operator-only Comment confirmation or fixed order of reviewers.

| Role | Responsibility |
|---|---|
| Proposer | Submits the change and evidence; cannot approve their own PR |
| Reviewer (approver) | Reads the shared report and comparisons, then Approves or Requests changes |
| Repository administrator | Manages permissions, required counts and other repository rules |
| Operations staff | Maintains tools, handles questions, merges approved proposals and prepares releases; may also be a reviewer |
| Tool provider | Publishes shared tools and proposes tooling updates |

The city may change the required count whenever its arrangement changes. An
authorized administrator records the date, before/after count and reason. One
account contributes at most one approval. Plan for the people who can actually
approve each PR, excluding its author; the total number of accounts with write
access is not necessarily the intended review group. Membership and optional
Code Owner requirements govern eligibility separately from the numeric count.

GitHub enforces the required approvals; the hub shows each reviewer whether they
approved, not how many approvals remain. See [review settings](review-settings.md).

## 3. PR types

| PR type | Unit of one PR | Building commits | Required extra records | Seat · where specified |
|---|---|---|---|---|
| `correction` | One building | One commit, one buildingID | Issue, evidence, before/after | Proposer, operator · handbook §6.1 |
| `lifecycle` | One rebuild / split / merge | One dedicated commit, multiple IDs allowed | Old/new ID relations, reason, Lifecycle-Manifest, city judgment | Operator · handbook §6.2 |
| `layout` | One one-step subdivision of one parent mesh | One semantics-preserving commit | Re-aggregation check, ID / reference / size checks | Operator · handbook §6.3 |
| `texture-gc` | One collection of unreferenced images | No building change | Proof of non-reference for all imageURIs, deletion list | Operator · handbook §6.4 |
| `revert` | Undo of one building commit or one PR | Keeps the original unit | Target, reason, affected releases | Operator · handbook §6.5 |
| `tooling` | One update of `CITYGML_TOOLS_REF` to a new `tools-v` release (CI verifies it against the tools tags) | No building change | Release notes, "no data change", `min_hub` if clients are affected | 4dcitygml proposes, operator verifies · handbook §6.6 |
| Docs / configuration | One documentation or configuration change (`docs/`, README, `4dcitygml.json`, theme, logo). Code is not accepted in a city repository (Exchange Contract A11) | No building change | Doc links, impact | Operator |
| `identity-correction` | One mis-connection / ID fix event | Per the dedicated gate | Before/after IDs, evidence, extra approval | Bulk submitter · bulk-submission document |
| `source-update` | 1 source transition × 1 mesh × 1 attribute family | One buildingID each | Provenance manifest, allowed paths, counts, sample | Bulk submitter · bulk-submission document |
| `carry-forward` | 1 edition change × 1 mesh | One `Building:` commit per re-applied building after the new edition's `source-baseline` | Provenance manifest (reapplied / absorbed / conflicts / unmappable / carried) | Bulk submitter · bulk-submission document |
| `semantic-correction` | 1 supported recipe × 1 mesh | One `Building:` commit per target | Fixed input and rationale, exact transformation, reproduction; released tooling and pilot verification required | [Recipe scope](https://github.com/4dcitygml/tools/blob/main/docs/lod0-semantic-correction.md) |
| `schema-update` | One schema bundle | No GML change | Digests of XSD / code lists, profile | Operator · bulk-submission document |
| `schema-migration` | 1 edition change × 1 mesh when the repository is the master | One generated `source-baseline` | Provenance manifest; semantic equality per registry key — gate not yet implemented | Bulk submitter · bulk-submission document |

`source-baseline`, `scope-extract`, and `identity-baseline` are for the
initial construction of the published history only; they are not repeated as
daily PRs. Adding further themes later (transportation, flooding, terrain …)
as a per-theme `source-baseline` has no gate yet.

## 4. Nothing merges when

- The PR is behind the latest main
- A required check failed, did not run, or targets an old head SHA
- Source, evidence, license, or publishability cannot be confirmed
- The PR type does not match the actual change
- Even one buildingID, path, or old/new value is outside the manifest
- An earlier PR on the same mesh is unmerged
- BuildingID identity, lifecycle relations, or schema-conversion semantics are unresolved
- A required layout PR for a mesh reaching 50 MiB is not done
- Churn remains, making out-of-scope buildings or lines appear changed
- No successful `analyze` and current `ci-report` checks from GitHub Actions
- GitHub's currently required number of eligible approvals is not met
- An approval was dismissed under the repository's stale-review policy
- Code Owner, last-push or other configured requirements are not met
- A PR type without dedicated CI is being slipped through as a normal update

Implementation status of the gates (what CI checks today, what is still to be
built) is maintained with the tools:
[Implementation status](https://github.com/4dcitygml/tools/blob/main/docs/implementation-status.md).
