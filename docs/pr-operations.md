<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Pull request operations after publication

- Status: adopted procedure for post-publication operation (PR types without
  dedicated CI remain gated until it exists)
- Applies to: published city data repositories

日本語版: [docs/ja/pr-operations.md](ja/pr-operations.md)

This document is the **canonical procedure for how PRs proceed after
publication**. Other documents explain design rationale or individual tools;
the order of daily work — starting, review, merge, release — follows this
one.

## 1. Principles fixed first

1. **1 commit = 1 `uro:buildingID`** is the minimum unit of a normal update.
2. Building commits that can be reviewed under the same evidence, source,
   and change rule may be bundled into one PR.
3. Never split the same buildingID across multiple commits of one PR. It may
   appear again in another PR or another annual attribute family.
4. A building merge, split, or rebuild is one `lifecycle` event handling
   multiple IDs.
5. City-data PRs are merged with a **merge commit, never squashed**, keeping
   each building commit on main.
6. Code/documentation-only PRs are kept separate from city data and may be
   squash-merged.
7. PR **approval**, **merge** to main, and stable **release** are separate
   completion states.
8. A PR where even one building or commit fails a blocking check is not
   partially merged.
9. main may contain work in progress. Regular users are pointed to the
   latest stable release.

Language of PR text: the editing tools generate the PR title and body in the
**repository's working language** (`lang` in `4dcitygml.json`); commit subjects,
`Building:` trailers, and branch prefixes stay English/literal (the history and
machine contracts are language-independent). Because city-data PRs merge with a
merge commit (rule 5), the PR title never becomes a history title line on main.
(The practice repos deviate: their auto-merge squashes, so the repo-language PR
title does appear in the practice history, which is periodically reset.)

```text
Issue / official source
  → Draft PR
  → automated checks
  → Ready for review
  → the city's semantic review
  → maintainer merges with a merge commit
  → Pages / history index update
  → stable release after the release gate passes
```

## 2. Roles and completion responsibility

| Role | Main work | Sign of completion |
|---|---|---|
| Proposer | Prepares the change, evidence, commits, PR body | Marks the PR Ready for review |
| CI | Mechanical checks: commit scope, XML, references, format, geometry, manifest | All required checks green |
| City reviewer | Semantic judgment: values, shapes, sources, lifecycle reasons | Approve or Request changes |
| Maintainer | Final check of required checks, approvals, merge method, freshness | Merge commit lands on main |
| Release manager | Source consistency, full checks, release notes, tag | Stable tag and check results published |
| Bulk submitter (dedicated account) | Generates conversion PRs from a declared source with a provenance manifest; never edits by hand under this account | Reproduction gate green, manifest reviewed, sample audit recorded |

One person may hold several roles, but the steps and records stay separate.
Each city keeps its own CODEOWNERS and final approval authority; they are
not shared across cities.

## 3. Steps common to every PR

### 3.1 Before starting

```text
[ ] Decided the starting point: an issue, an official source, or scheduled maintenance
[ ] Identified the target city, uro:buildingID, mesh, and change type
[ ] The evidence can be published, with no license / personal-information / privacy problems
[ ] No earlier open PR changes the same mesh GML
[ ] The boundary between this PR and other PRs is decided
```

PRs that change the same mesh GML are serialized: create the next PR from
main after the earlier one merges. Different meshes may proceed in parallel
only when shared schema migrations are done and no shared textures or XLinks
are touched.

### 3.2 Branch and commits

```text
[ ] Created the working branch from the latest main at start time
[ ] The PR history is linear, with no merge commits inside the branch
[ ] Each normal-update commit changes exactly one buildingID
[ ] The same buildingID is not split across commits within the PR
[ ] Building commits are ordered by ascending uro:buildingID
[ ] Building:, Building-Added:, Building-Deleted: trailers match the actual change
[ ] Formatting-only diffs outside the target are removed with the minimal-diff version
```

Use `Draft` for saving work and checking CI. Enter the reviewer's queue only
after automated checks and self-review are done and the PR is marked
`Ready for review`.

### 3.3 PR body

```text
[ ] Picked exactly one PR type
[ ] Wrote what changes, why, and on what evidence
[ ] Listed every target buildingID, or the manifest
[ ] Stated the allowed paths and what must not change
[ ] Linked related issues with Fixes #<number> or Refs #<number>
[ ] Added evidence URLs, document names, retrieval dates, editions, hashes
[ ] If shape, LOD, attributes, IDs, and lifecycle are mixed, explained why they cannot be separated
```

Annual `source-update` PRs additionally require:

```text
Source-From, Source-To, Scope-Mesh, Attribute-Family, Allowed-Paths,
History-Manifest, Manifest-SHA256, Building-Count,
First-Building-ID, Last-Building-ID
```

### 3.4 Automated checks and proposer confirmation

```text
[ ] Base freshness shows no unresolved "merge in the latest version"; head contains latest main
[ ] All commits passed the commit scope check
[ ] XML/XSD, CityGML structure, and convention blocking checks succeeded
[ ] XLink, Appearance, imageURI, and texture references resolve
[ ] The automated change summary matches the PR body
[ ] Buildings with geometry changes were compared old/new in the 3D view
[ ] Warnings and notices were not ignored; reasons for no-action were judged
[ ] After a churn notice, the minimal-diff version was applied and rechecked
[ ] All required checks are green on the head SHA of the final push
```

Current churn handling stops at notification and generating the minimal-diff
version; automatic application to the PR head is not implemented. Until it
is, the proposer or a maintainer applies it.

### 3.5 Reviewer's examination

```text
[ ] The PR is not Draft and is in the review queue
[ ] The head SHA under review equals the one the automated checks ran on
[ ] All required checks succeeded and latest main is included
[ ] Change summary, evidence, shape comparison, and manifest were checked against the same target
[ ] The meaning of values, shapes, sources, and old/new ID relations is sound
[ ] Additional approval conditions (lifecycle, identity, texture-override) are met
[ ] If pushes occurred after approval, re-review
```

- Fixable defects → `Request changes`, pointing to the places to fix.
- Questions or fact-finding → `Comment`; never confuse it with approval.
- `Approve` only when the evidence holds and all semantic judgment and
  required checks are done.
- Duplicate PRs, out-of-scope changes, unpublishable evidence, or
  unresolvable rights problems → close with the reason recorded.

### 3.6 Merge

```text
[ ] All required checks succeeded on the final head SHA
[ ] Request changes are resolved
[ ] Necessary CODEOWNERS / additional approvals are present
[ ] Base freshness shows latest main
[ ] "Create a merge commit" is selected for city-data PRs
[ ] PR type, target mesh, and manifest were re-confirmed right before merging
```

No auto-merge. Approval is one condition for merge permission; a reviewer's
action alone never rewrites main.

### 3.7 After merge

```text
[ ] The merge commit and the individual building commits remain on main
[ ] Checks and Pages generation on main succeeded
[ ] Issues linked with Fixes were closed correctly
[ ] The Building: trailer resolves back to the PR and merge commit
[ ] Annual release-plan states (planned / in-progress / complete) were updated
[ ] The user-facing screens distinguish "main in progress" from "latest stable release"
[ ] On anomalies, a revert PR was opened — history is never rewritten
```

No follow-up commits that write merged PR numbers or SHAs into the manifest
itself. The Pages index is regenerated from git history and GitHub.

## 4. Choosing the PR type

| PR type | Unit of one PR | Building commits | Required extra records |
|---|---|---|---|
| `correction` | One evidence / change rule | One buildingID each | Issue, evidence, before/after |
| `lifecycle` | One rebuild / split / merge | One dedicated commit, multiple IDs allowed | Old/new ID relations, reason, manifest, extra approval |
| `identity-correction` | One mis-connection / ID fix event | Follows the dedicated gate | Before/after IDs, evidence of the error, extra approval |
| `source-update` | 1 source transition × 1 mesh × 1 attribute family / rule | One buildingID each | Source/change manifest, allowed paths, counts, sample check |
| `schema-update` | One schema bundle | No GML change | Hashes of XSD / code lists, profile |
| `carry-forward` | 1 edition change × 1 mesh (previous official, repository, new official) | One `Building:` commit per re-applied building, after the new edition's `source-baseline` | Provenance manifest: reapplied / absorbed / conflicts / unmappable / carried old codeSpace |
| `schema-migration` | 1 edition change × 1 mesh when no official new-edition file exists (the repository is the master): registry-driven re-serialization of the i-UR subtree | One generated `source-baseline` of the new edition | Provenance manifest; semantic-equality check per registry key (kept / mapped / carried / unmappable) — gate not yet implemented |
| `layout` | One one-step subdivision of one parent mesh | One semantics-preserving commit | Re-aggregation check, ID / reference / size checks |
| `texture-gc` | One collection of unreferenced images | No building change | Proof of non-reference for all imageURIs, deletion list |
| `revert` | Undo of one building commit or one PR | Keeps the original unit | Target, reason, affected releases |
| Code / docs | One tool or documentation change | No building change | Tests, doc links, impact |

`source-baseline`, `scope-extract`, and `identity-baseline` are for the
initial construction of the published history only; they are not repeated as
daily PRs after publication.

### 4.1 Daily `correction`

```text
[ ] There is a data-issue or publishable evidence
[ ] Buildings bundled into the PR can be reviewed under the same evidence and rule
[ ] Each commit has exactly one Building: <uro:buildingID>
[ ] Texture replacement was done by adding new images + updating imageURI
[ ] After geometry changes, derived attributes (height, area, …) were checked for consistency
```

Overwriting an existing texture under the same name is forbidden in
principle. Only for legitimate exceptions (shared atlases etc.), after
checking every affected building, a maintainer applies the
`texture-override` label.

### 4.2 `lifecycle`

```text
[ ] Old/new building relations are settled; no unresolved candidates mixed in
[ ] The PR contains exactly one real-world event
[ ] Change-Type: lifecycle is recorded
[ ] Building-Deleted: / Building-Added: match every actually changed ID
[ ] Relations, event/confirmation date, evidence, and decision maker are in the manifest
[ ] The lifecycle label and CODEOWNERS extra approval are present
```

If the old/new relation is unclear, do not jump to "demolished" or
"rebuilt" — park it in an issue or `lifecycle-review`.

### 4.3 `identity-correction`

Even when a mis-connected identity is found in published history, past
commits and tags are never rewritten. A new PR records the before/after IDs,
the evidence of the error, and the affected history.

```text
[ ] Identified the buildingIDs before and after the correction
[ ] There is evidence this is a mis-connection fix, not a lifecycle event
[ ] Recorded which period of past history is affected
[ ] The dedicated identity-correction CI and extra approval succeeded
```

The commit scope gate accepts buildingID replacement only as an
`identity-baseline` / `identity-correction` commit backed by a provenance
manifest (see below); the `reproduction` gate regenerates the manifest from
its declared materials. Do not mark such PRs Ready for review until these gates
have been verified on a real repository in the private pilot.

Identity PRs are bulk submissions: they are accepted by **reproduction**, not
by reading each commit. The submission package (plan issue, provenance
manifest with per-building evidence and the per-boundary ID regime, commit
trailers, dedicated account, sample audit) and the gate are specified in
[Bulk submissions: provenance, verification, and merge policy](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md).
Measured on the Tokyo 2020–2025 editions, `uro:buildingID` continuity breaks
completely where the product lineage changes (the 2022→2023 boundary
renumbered every building, and IDs shared across that boundary belonged to
*different* buildings), so an identical ID is never sufficient evidence on
its own; every link needs geometric evidence.

### 4.4 Annual `source-update`

Annual updates proceed as separate PRs in this order:

1. `schema-update` — the new edition's artifacts (code lists under `codelists/<edition>/`, schema profile), no GML change
2. when the edition changes — either the new official edition as a fresh `source-baseline` followed by `carry-forward` (three-way comparison per building and attribute), or, when the repository is the master and no official new-edition file exists, `schema-migration` (registry-driven re-serialization of the i-UR subtree, verified by semantic equality per registry key)
3. a single-building pilot per attribute family
4. multi-building PRs per attribute family
5. dedicated PRs for geometry, LOD, and source `gml:id`
6. `lifecycle` for confirmed events
7. completion checks per mesh and across the city
8. the annual release tag

```text
[ ] Pre-update assessment of source, schema, IDs, semantic rules, lifecycle, and size is done
[ ] Each PR is limited to 1 source transition × 1 mesh × 1 attribute family / rule
[ ] The manifest pins allowed paths, old/new values, and every target buildingID
[ ] A representative building per attribute family passed first
[ ] Generated from main after the earlier PR on the same mesh merged
[ ] Auto-confirmed groups are separated from ambiguous / lifecycle-review groups
[ ] The final path signature matches the pre-computed one
```

Never overwrite a whole new-year source in one PR. Each attribute PR is
generated from the new-year copy in the work area, based on the
not-yet-applied buildingID manifest.

`source-update` PRs are bulk submissions: ship the provenance manifest and
`Provenance-Manifest:` trailers described in
[Bulk submissions: provenance, verification, and merge policy](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md);
reviewers verify the plan, the manifest, and a random sample, and CI
reproduces the conversion.

### 4.5 `schema-update` and edition changes (`carry-forward`)

```text
[ ] schema-update changes no GML; only edition artifacts (codelists/<edition>/, schemas/, provenance/schema-update/)
[ ] The artifacts' digests and their official source (ZIP member) are recorded
[ ] Offline XSD validation of the current data passes under the new profile
[ ] An edition change is applied as: new official edition = source-baseline, then carry-forward (never a structural conversion of the old file)
[ ] The carry-forward manifest lists reapplied / absorbed / conflicts / unmappable / carried old-codeSpace per building
[ ] Conflicts and unmappable attributes were decided by a reviewer; carried codes are counted for the release gate
```

Two routes exist for an edition change. While official editions are produced
independently, the new official edition becomes the next baseline and the
accumulated changes are re-applied on it by a three-way comparison per
building and semantic attribute (`carry-forward`, see
[Bulk submissions: provenance, verification, and merge policy](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md)).
Once the repository is the master copy and the official edition is exported
from it, no external new-edition file exists: `schema-migration` then
generates the new edition's serialization from the repository's own content
— the CityGML core is unchanged within 2.0 (a 3.0 transition converts the
core through 3DCityDB), and the i-UR subtree is re-serialized per building
from the semantic registry, the code-list crosswalk (codes without a 1:1
mapping keep their old codeSpace) and the new edition's XSD order. Its gate is
semantic equality per registry key (kept / mapped / carried / unmappable) and
reproduction; it is designed but not yet implemented. Either route is
verified by the same registry-based comparison. `schema-update` is gated by
the commit scope check (artifact paths only, no CityGML change);
`carry-forward` is gated like `source-update` plus the `reproduction` gate.

### 4.6 `layout`

```text
[ ] Confirmed before the update that a stored GML would reach 50 MiB or more
[ ] Subdivided only the current mesh on pre-update main, by exactly one level
[ ] Recorded Change-Type: layout, with no building-ID trailer
[ ] Building count, ID set, semantic hash, Appearance, and XLink are unchanged
[ ] Envelope, XSD, and temporary re-aggregation checks pass
[ ] All files after subdivision are under 50 MiB, with no tracked file at 100 MiB or more
```

A once-subdivided mesh is never merged back to a coarser mesh, even if it
shrinks in later years. The current tool supports one subdivision step;
deeper levels are unlocked only after extension and verification.

### 4.7 `texture-gc`

```text
[ ] Every deletion candidate is unreferenced by all imageURIs on main
[ ] Zero new dangling references
[ ] The deletion list, count, and byte size are recorded in the PR body
[ ] No building GML, attributes, or geometry change in the same PR
```

### 4.8 `revert` and urgent fixes

Published mistakes are never hidden by force-push or tag replacement — they
are undone by a new PR.

```text
[ ] Decided whether to revert one building commit or the whole PR
[ ] Recorded the target commit or merge commit SHA
[ ] Wrote the reason, how it was found, and the affected buildings and releases
[ ] Ran the full normal checks on the reverted CityGML
[ ] Decided whether a patch release is needed if a published release is affected
```

Even under urgency, required checks and human approval are never skipped.
Respond by narrowing the scope and raising the priority.

## 5. Releases

### 5.1 Ordinary daily fixes

- After merge, the fix is reflected on main and in the building history.
- Merging a PR alone never moves an existing stable release.
- It is included in the next scheduled patch or annual release.
- A patch release is made for serious errors, legal / personal-information
  problems, or usage hazards.

Patch-release tag naming and cadence are fixed in a separate ADR before
publication.

### 5.2 Annual releases

```text
[ ] All attribute-family PRs for all target meshes are complete
[ ] Geometry, LOD, source gml:id, and confirmed lifecycle groups are complete
[ ] Schema profile check and, for an edition change, the carry-forward manifest review are complete
[ ] Full buildingID set, duplicates, references, Appearance, and XSD pass
[ ] The final path signature semantically matches the official new-year edition
[ ] Unresolved groups are left untouched, with a hold list and impact stated
[ ] The release-plan is release-ready
[ ] Release notes cover source, hashes, processing, ID unification, holds, and check results
[ ] Tag, Pages, downloads, and check results point at the same commit
[ ] Carried old-codeSpace values (codelists/<edition>/) are counted with carried_codespace_report.py and resolved or accepted by the official channel
```

While any release-ready condition is missing, main is never presented as
"the stable new-year edition".

## 6. Merge stop conditions

Do not Approve or merge when any of the following holds:

- The PR is behind the latest main
- A required check failed, did not run, or targets an old head SHA
- Source, evidence, license, or publishability cannot be confirmed
- The PR type does not match the actual change
- Even one buildingID, path, or old/new value is outside the manifest
- An earlier PR on the same mesh is unmerged
- BuildingID identity, lifecycle relations, or schema-conversion semantics are unresolved
- A required layout PR for a mesh reaching 50 MiB is not done
- Churn remains, making out-of-scope buildings or lines appear changed
- Required CODEOWNERS / lifecycle / identity / texture-override approvals are missing
- A PR type without dedicated CI is being slipped through as a normal update

## 7. Current implementation and remaining work

### 7.1 What the current repository can check

- The 1-buildingID constraint and trailer match for normal commits
- Prohibition of duplicate buildingID commits within a PR
- Commit-scope exceptions for `lifecycle`, `layout`, `source-baseline`, `scope-extract`
- `identity-baseline` / `identity-correction` commits: trailer and manifest reference, byte-preserving ID replacement, tier rule, repository-wide ID uniqueness
- `source-update` value replacements within one attribute family: manifest-backed `Building:` commits, byte-exact application of the manifest's changes, all targets applied
- The `reproduction` gate re-fetches a bulk manifest's materials and regenerates it (identity and source-update kinds)
- Per-building history derived from git regardless of commit granularity (`scripts/building_history.py` in tools: follows the building through ID changes, whole-file baselines and manifest-backed commits, reporting registry-keyed changes per commit); the `history-index.yml` workflow publishes it as a static Pages site (`history/index.html` + `history/buildings/<id>.json`, next to the repository content served by the same Pages site)
- Target-municipality set and retained-building invariance for `scope-extract`
- XML/XSD, structure, references, textures, geometry checks and comparison views
- Base-freshness guidance
- A reviewer screen separating Draft / checking / waiting-for-merge / waiting-for-review

### 7.2 To implement before unlocking the corresponding PR types

- Per-edition schema profiles as a validation option (today one master schema covers i-UR 2.0–3.2)
- Pilot verification of the implemented `identity-baseline` / `identity-correction` gates (commit scope rules + `identity` reproduction) on a real repository
- Pilot verification of the `source-update` value-replacement gate (one attribute family per PR; manifest-backed commits, reproduction) on a real repository
- Edition restructurings (attribute containers added or removed by a new edition — the majority of the measured 2020→2025 differences) are handled by `carry-forward` (implemented) while official editions exist; the registry-driven `schema-migration` for the master-copy phase (re-serializer, semantic-equality gate, i-UR 4.0 registry) is designed but not implemented
- Full matching of Allowed-Paths, old/new values, and manifest IDs for `source-update`
- The release gate for final path signature and official-source consistency
- Subdivision / re-aggregation tools for deeper mesh levels where needed
- A Pages index generating buildingID → commit → PR → merge commit → release from git history
- Automatic application of the minimal-diff version for same-repo and fork PRs
- The ADR for patch-release tag naming, cadence, and urgency criteria

Unimplemented dedicated gates are never substituted by documentation alone.
Confirm reject and revert behavior on a real repository before putting them
into public operation.

## 8. Periodic checks after publication

### Weekly

```text
[ ] Reviewed PRs separated into waiting-for-review / Request changes / waiting-for-latest-main
[ ] Handled CI breakage separately from data failures
[ ] Wrote the next action or a close reason on long-stalled PRs
[ ] No conflicting PRs on the same mesh
```

### Monthly / before scheduled releases

```text
[ ] Checked candidates for unreferenced textures
[ ] Recorded new official sources / annual editions and the check date
[ ] Inspected tag pins of required workflows and shared tools
[ ] Checked CODEOWNERS, approval authority, and vacancies from departures
[ ] Confirmed sources, rights, and open questions for the release-target commit
```
