<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Provenance rules (recording sources and evidence)

Rules for where — and at what granularity — the sources and evidence of
attribute values, geometry, and textures are recorded.

日本語版: [docs/ja/provenance-rules.md](ja/provenance-rules.md)

> **Scope note.** These rules were designed for CityGML datasets that use the
> i-UR ADE (`uro:` — the extension adopted by Japan's PLATEAU program), which
> is where the layer-1 mechanisms below come from. City repositories based on
> other datasets (see `building_id` in `4dcitygml.json`) apply the same
> three-layer principle, substituting their dataset's own quality-metadata
> mechanism for layer 1 where one exists.

## Position — i-UR (urban ADE) plus a small "α"

These rules add **no new schema**. Per-item provenance is achieved with
standard mechanisms only (rules + tools), on two standard foundations:

- **i-UR (uro = Urban Object ADE)** — the CityGML extension adopted by
  PLATEAU. Provides `uro:DataQualityAttribute` (acquisition method, accuracy,
  provisional/confirmed) and `uro:thematicSrcDesc` (source-code list for
  thematic attributes) **per building**. This is layer 1.
- **CityGML core generics** (`gen:genericAttributeSet`) — the generic
  mechanism for "when no standard attribute exists". It carries **per-item**
  provenance, finer than i-UR's per-building granularity, while staying
  schema-valid. This is the "+α" of layer 2.

So the design is: **the ADE quality attributes (per building) are the
backbone, and generics add per-item notes (+α)** — no custom ADE, no schema
extension (interoperability is never broken; we stand on the shoulders of
giants). Layers 1 and 2 **share the same code list**, which makes them a
coherent system of "building default + its exceptions" (see the resolution
rule below). The attribute editor implements this workflow (§5).

## 0. Principle — record in three layers

| Layer | What is recorded | Where | Granularity | Role |
|---|---|---|---|---|
| **1. Official quality attributes** | Acquisition method, accuracy, provisional/confirmed | `uro:DataQualityAttribute` | building × (axis × LOD) | **Primary** — the standard comes first |
| **2. gen "source" set** | **Item-level** attribute↔source mapping, evidence links | `gen:genericAttributeSet name="出典"` | **per item (attribute)** | **Exception** — only when needed |
| **3. git history** | Who, when, why (the full story) | commit / PR / `Building:` trailer | per leaf value (guaranteed by the minimal-diff pipeline) | **Always, automatic** |

Division of labor: what survives when the data circulates on its own is
layers 1–2. The complete story in repository context (blame, PR discussion,
reproduction steps) is layer 3.

## 1. Layer 1 — official quality attributes (primary)

The finest granularity the official schema can express (i-UR 3.1 / 3.2):

| Axis | Element | Granularity |
|---|---|---|
| Geometry source | `geometrySrcDescLod0`–`Lod4` | building × LOD |
| Appearance source | `appearanceSrcDescLod0`–`Lod4` | building × LOD |
| Height acquisition | `lod1HeightType` | per building (measured 1-8,10 / provisional 0,9) |
| Accuracy | `srcScaleLod*` | building × LOD |
| **Thematic (attribute) sources** | `thematicSrcDesc` | **listed per building as a set** (cannot map to attribute names) |

Rules:

- **R1-1 (simultaneous update)**: a PR that changes a value updates the
  corresponding quality code **in the same PR**. Example: replacing
  measuredHeight with a surveyed value updates `lod1HeightType` from a
  provisional code (0/9) to a measured one.
- **R1-2 (adding origin codes)**: when attributes are added or updated from a
  new source, append the origin code to the building's `thematicSrcDesc`
  (per building; codes come from the bundled code list).
- **R1-3 (no value encoding)**: never encode source or accuracy information
  into the value itself (no ad-hoc encodings like `10000100m`; the lesson of
  the -9999 sentinel).

## 2. Layer 2 — the gen "source" set (exception, per item)

### When to use it (only if one of these applies)

- Multiple sources are mixed and the per-building set cannot tell "which
  attribute came from which source"
- A value whose individual origin is itself valuable — e.g. an on-site
  measurement or a document provided by a citizen
- A derived attribute whose attribute↔derivation mapping must be kept

### When not to use it

- When layer 1 (the standard mechanism) suffices. As the XSD note for
  generics says, use it "only where no standard attribute exists". Do not
  mechanically annotate every attribute.

### Format (rule)

```xml
<gen:genericAttributeSet name="出典">
    <gen:stringAttribute name="bldg:measuredHeight">
        <gen:value>801</gen:value>
    </gen:stringAttribute>
    <gen:stringAttribute name="bldg:storeysAboveGround">
        <gen:value>802</gen:value>
    </gen:stringAttribute>
    <gen:uriAttribute name="根拠資料:bldg:measuredHeight">
        <gen:value>https://github.com/4dcitygml/sample-tokyo-station/pull/2</gen:value>
    </gen:uriAttribute>
</gen:genericAttributeSet>
```

Meaning of the example: measuredHeight comes from code `801` (field survey),
storeysAboveGround from `802` (photo interpretation).

- **R2-1 (set name)**: the set name is fixed (`name="出典"` — "source"), **at
  most one per building**.
- **R2-2 (keys)**: the child `@name` is the **QName of the target attribute**
  (e.g. `bldg:measuredHeight`, `uro:buildingStructureType`). Where the same
  QName can occur more than once in a building, the leaf-path notation of the
  diff pipeline is used instead.
  - Whether a QName is unique is **decided mechanically per building**:
    CityGML core attributes are `maxOccurs=1` by schema and always unique;
    ADE attributes can structurally repeat (key-value pairs, disaster-risk
    records, …). The attribute editor implements this dynamic check and only
    offers QName notes for unique attributes.
- **R2-3 (values are codes)**: values must come from **the dataset's
  `codelists/…thematicSrcDesc….xml` code list only** (no free text). The same
  vocabulary as layer 1's `thematicSrcDesc`, applied per item (e.g. `801` =
  field survey, `802` = photo interpretation, `803` = GIS computation). This
  keeps machine validation (code-list lint) and label resolution working
  as-is.
  - Details such as method or date do not go into the value — they go to the
    evidence link (R2-4) and the PR body (layer 3). Provisional/confirmed
    status goes to layer-1 quality codes (never contradict them).
  - A source not in the code list → use a catch-all code (e.g. `700` "other
    document") **plus a mandatory evidence link**. If a source keeps
    recurring, **propose extending the code list itself via a PR** (code
    lists are under git management and thus reviewable).
- **R2-4 (evidence links)**: `gen:uriAttribute` with `@name` = `根拠資料`
  (whole building) or `根拠資料:<QName>` (per item). URLs to PRs, photos,
  registers, etc.
- **R2-5 (placement)**: immediately **after `core:creationDate`**, matching
  how real datasets place generics.
- **R2-6 (no values)**: the set records source information only. The value
  itself lives in the standard attribute (no duplication).
- **R2-7 (simultaneous update)**: when a target attribute's value changes,
  its source code is updated **in the same PR**.

### Source resolution rule (note > building default)

Because layers 1 and 2 share one code list, the source of any attribute
resolves uniquely:

1. **Note exists** — if the "source" set has a note for the attribute
   (QName), that code is the source (unique).
2. **No note** — refer to the building's `thematicSrcDesc` (default).
   - One code → the source is unique.
   - Multiple codes → the source is "one of them" (a candidate set). Adding
     notes only to the attributes worth pinning down lets uniqueness improve
     **incrementally without rewriting the building**.
3. Neither → treated as "unknown" (code `898` or equivalent).

- **R2-8 (note ⊆ default invariant)**: a code used in a note **must also be
  present in the building's `thematicSrcDesc`**. Introducing a new source via
  a note requires appending the same code to the default (R1-2) in the same
  PR. The default is then always "the complete set of this building's
  attribute sources" and notes are "the mapping within it" — never
  contradictory, and machine-checkable.

### Validation and pipeline (verified)

- The format above is **valid against CityGML 2.0 + i-UR 3.2 XSD** (verified
  with offline validation).
- The diff pipeline detects notes as **leaf-level paths**
  (`/genericAttributeSet[@name=出典]/stringAttribute[@name=…]/value`), so
  adding or updating provenance rides the existing reviewability pipeline
  (per-building PRs, minimal diff) **with no extra implementation**.
- Precedent: official PLATEAU distributions themselves ship large numbers of
  municipality-specific attributes as `gen:stringAttribute`, so using
  generics is an extension of official practice.

## 3. Layer 3 — git history (always, automatic)

- Commits carry a `Building: <uro:buildingID>` trailer (see
  `scripts/suggest_commit.py`). The minimal-diff gate guarantees leaf-level
  diffs, so **`git blame` works at attribute granularity**.
- When an attribute is produced by derivation or conversion, record the
  **method, parameters, and reproduction steps in the PR body** (a third
  party must be able to reproduce the result).
- The narrative ("why this value") lives in the PR description and review
  discussion — never inside the data.

## 4. Rules for cross-cutting attribute-addition PRs

A PR that adds a new attribute in bulk:

1. If a standard slot exists → add it as a **standard attribute** and append
   the origin code to `thematicSrcDesc` (R1-2)
2. If the attribute↔source mapping matters (mixed origins, derived values) →
   add the "source" set as well (layer 2)
3. Method and parameters of derivation → record in the PR body (layer 3)

## 5. How the attribute editor implements this

The attribute editor implements these rules as UI, so submitters record
compliant provenance through screen operations alone, without reading this
document:

- **The building default is shown once**: right under the building ID, the
  editor shows "sources (default for this building)" = the building's
  `thematicSrcDesc` (code + label), instead of repeating it on every row.
- **After a value change, the next action is source selection**: confirming
  a value expands a mandatory source selector in the same row. "Send
  changes" stays disabled until every changed attribute has a source, and
  the submit API re-validates the same condition. "Unknown" and "not
  created" cannot be chosen as evidence for a new change.
- **Notes only on the rows that need them**: unchanged attributes show a
  note only where their source differs from the default.
- **Dropdowns show code + label**, values are restricted to code selection
  (R2-3's shared code list); no free text.
- **R2-8 is automated**: if a chosen note code is missing from the default,
  the editor appends it to the default in the same PR and announces this in
  the UI.
- **Ambiguous attributes still require selection**: attributes whose QName
  repeats within a building cannot get an item note, so the selected code is
  synced to the building default and the mapping is recorded in the
  auto-generated PR body (layer 3).
- **PR text is auto-generated** from the selected sources and the
  before/after values; the submitter only adds optional notes and evidence
  URLs. The main text avoids XML tag names.
- **Byte preservation**: notes are inserted right after `core:creationDate`
  (R2-5) keeping the original indentation, line endings, and BOM, and the
  change rides the per-building PR pipeline unchanged.

## Related

- Contribution licensing and recording:
  [data-contribution-policy.md](data-contribution-policy.md)
- Day-to-day PR flow: [pr-operations.md](pr-operations.md)
