<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Data Contribution Policy (attributes, geometry, textures, photos)

status: v2 (v1 "photo contribution policy" extended to all data contributions)

This policy governs the rights in **contributions to the data files of this
repository (CityGML and texture images under the data directories)**. By
submitting a PR that changes data, the submitter agrees to this policy (the
editing tools record this agreement in the PR body).

日本語版: [docs/ja/data-contribution-policy.md](ja/data-contribution-policy.md)

## 1. All data contributions are CC0 1.0

- Submitters provide their data contributions (attribute values, geometry
  fixes, textures, photos) under
  **[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)**
  (public-domain dedication), to the extent any rights arise in them at all.
- Corrections to attribute values (storey counts, usage codes, flood depths,
  …) and geometry (coordinates) are **facts / data** and are normally not
  copyrightable in the first place. This clause is a safety-side declaration
  ("even if rights somehow arise, they are CC0") — the same approach Wikidata
  takes for structured data.
- Photos are independent copyrighted works. Submitters therefore also agree
  **not to exercise moral rights** (which cannot be waived or transferred in
  some jurisdictions, e.g. under Japanese law). Texturing involves cropping,
  perspective correction, compositing, and recompression, so this consent to
  modification is essential.
- **Contributions to code and documentation are outside this policy.** They
  follow the repository license (Apache-2.0) via the GitHub Terms of Service
  (D.6 inbound = outbound), as usual.
- The repository's data distribution as a whole keeps the license of its
  official source (see the repository README and `4dcitygml.json`; e.g.
  CC BY 4.0 for PLATEAU-derived data). Integrating CC0 material does not
  conflict with this.

## 2. Additional conditions for submitting photos

1. The photo must be **taken by yourself** (no photos by others, no images
   from the web or social media).
2. It must be **taken from a lawful location** such as a public road.
3. **Privacy and personal information**: photos in which the following are
   recognizable must be avoided, or those parts masked / blurred before
   submission:
   - people's faces or appearance (passers-by, residents)
   - vehicle license plates
   - nameplates, room interiors, laundry, and similar traces of daily life
4. **Third-party works in the frame**: local copyright law usually permits
   photographing building exteriors and allows *incidental* inclusion of
   signs, posters, and displays (in Japan: Arts. 46 and 30-2 of the Copyright
   Act). Avoid photos where such works are the main subject.

The texture editor asks for an explicit consent check when creating a PR
(photos are substantial copyrighted works, so consent is explicit). The
attribute editor records agreement in the PR body without a checkbox —
**friction is proportional to the rights risk** by design.

## 3. Recording and honoring contributions (independent of copyright)

- Contributions are permanently recorded in the git history (commit author
  and the `Building:` trailer). `git log --grep "Building: <id>"` and author
  aggregation can trace who contributed to which building.
- Visualization and honoring of contributions based on this record
  (contributor lists, certificates of appreciation, …) may be operated
  independently of copyright ownership.

## 4. Requesting removal

- If a privacy or personality-rights problem is discovered in an image after
  the fact, please tell us in an issue. We will promptly remove it from the
  current data.
- Because of how git works, **data remains in the past history even after
  removal**. For serious cases involving personality rights or privacy, the
  maintainers will consider countermeasures including removal from history
  (history rewrite).

---

## Appendix: decision record

Summary of the considerations when this policy was adopted (kept for
transparency).

**Approaches compared**:

| Approach | Example | Assessment |
|---|---|---|
| Platform license (contributor keeps copyright, grants the operator a broad license) | Google Maps reviews | Fits a single operator's display use, but attribution management remains for open-data redistribution |
| Collective attribution (terms assign rights to a foundation, collective "© contributors" notice) | OpenStreetMap | Solid track record, but heavy terms documents and operations |
| **CC0 (factual data dedicated to the public domain)** | **Wikidata** | **Adopted.** Downstream users (municipalities, researchers, companies) can use the data without per-photo attribution management |

**Deciding factors**:

1. **Avoiding attribution stacking** — per-photo CC BY would mean permanently
   managing attribution for every texture in NOTICE files, which breaks down
   in folders mixed with official-source textures.
2. **Moral rights** — in some jurisdictions (e.g. Japan, Copyright Act
   Art. 59) they cannot be waived or transferred, so explicit non-exercise
   consent is added on top of CC0 (texturing modifies the work, so the right
   of integrity must be addressed).
3. **Extension to attributes and geometry (v2)** — factual data is not
   copyrightable, so the declaration is mostly a no-op, but it costs nothing
   and removes ambiguity. Limited to **data contributions** (extending CC0 to
   code would conflict with the Apache-2.0 scheme).
4. **Friction design** — explicit consent (checkbox) only for substantial
   works (photos); attribute edits get an automatic note in the PR body only.
5. **Honoring is independent of copyright** — the git history (author,
   `Building:` trailer) doubles as a contribution ledger, so "whose
   contribution" remains traceable even under CC0.
