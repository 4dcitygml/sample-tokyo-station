# Practice cities

This folder is for the practice repositories (the `sample-*-station` cities) only. A real city
leaves it as it is: nothing here runs, because GitHub runs workflows only from
`.github/workflows/`. It sits under `.github/` because a city repository takes changes only to
its data, documents and configuration (Exchange Contract A11); a change here, like any
`.github/` change, needs the maintainer's `tooling` label.

A practice city is this template plus its own data and configuration plus the files of this
folder activated. There is no separate practice master: every file a practice city runs comes
from the template.

## What is here

| File | Activated as | What it does |
|---|---|---|
| `manual-reset.yml` | `.github/workflows/manual-reset.yml` | A maintainer returns the practice data to the `baseline` branch through one pull request; the history stays |
| `practice_reset.py` | (not activated; the workflow runs it) | Reads the data directories; after the merge, closes the open data proposals with the note from `.github/scripts/texts.py` |
| `allowed-differences.json` | (not activated) | What a practice city may differ in from the template; read by the tools test |

## Activating it in a practice city

1. Copy `manual-reset.yml` into `.github/workflows/` (byte for byte).
2. Repository variable `PRACTICE_REPO` = the repository's own `owner/name`. The workflow runs
   only where it matches, so a fork or a copy stays inert.
3. A `baseline` branch holding the pristine practice data.
4. No personal token, no other secret and no change to the Actions settings: the workflow only
   pushes a branch, and the maintainer opens the pull request.

## The reset, step by step (for the maintainer)

1. Actions > "Manual practice reset" > Run workflow, typing `RESET`.
2. The run pushes `reset/<date>`; its summary links the pull request to open, with the title and
   the Summary of changes filled in. If main already holds the baseline data, nothing happens.
3. Open the pull request from that link. Its checks start as for any pull request.
4. When `analyze` and `ci-report` are green, merge (squash) with the ruleset's bypass: the
   maintainer who opened the pull request cannot give its code-owner review. GitHub adds a co-author line for
   the Actions bot, which is already the author; the duplicate is harmless. The trailers
   `Change-Type: practice-reset` and `Reset-To: <commit>` must stay: the merge's push to main
   reads them and closes the open proposals that change nothing but the data directories, with
   a note in the city's language. Other pull requests stay open.

## What a practice city may differ in

A practice city carries every file of the template byte for byte, this folder and the
`.example` files included. It differs only as `allowed-differences.json` in this folder lists,
which the tools test that compares the city copies reads:

- template only (not carried): `.github/dependabot.yml`; action updates reach the city through
  the template sync;
- replaced: `README.md`, `LICENSE`, `NOTICE` (the practice data's licensing), and
  `.github/PULL_REQUEST_TEMPLATE.md` (the template's file for the city's `lang`,
  `.github/PULL_REQUEST_TEMPLATE/<lang>.md`, or the English default);
- added: `4dcitygml.json`, `theme.json`, `logo.png`, `docs/practice-photos/` (CC0 or public-domain
  photos for practising textures, with their `CREDITS.md`), the data directories and `provenance/`, and
  the getting-started in the city's language, `docs/<lang>/getting-started.md` (when `lang` is
  not en), which the city's README links for residents;
- activated: the files of this folder copied into `.github/workflows/`.

`.github/CODEOWNERS` stays the template's file in a practice city; a real city names its own code
owners there.
