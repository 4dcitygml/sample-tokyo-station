<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Getting started: from clone to your first change proposal

This guide walks through the practice flow end to end: getting this repository onto
your computer, starting the shared editing tools, connecting them to your GitHub
account, and sending your first change proposal (a pull request). It takes about
15 minutes the first time. Nothing here changes the city data directly: every edit
becomes a proposal that a maintainer reviews.

For the rules that proposals must follow, see the [PR operations guide](pr-operations.md)
and the [source recording rules](provenance-rules.md). For what may be contributed,
see the [data contribution policy](data-contribution-policy.md).

## 1. Quick start: download the starter kit

You do not need Git, a GitHub account, or a copy of the city data to begin. The
tools guide you through everything that is missing.

1. Download the **starter kit** linked from this repository's README (the *Get
   started* bullet). It is a small zip with the starter scripts and this city's
   configuration.
2. Unzip it. You get a folder such as `<city>-starter/`.
3. Start:
   - macOS: double-click `start-mac.command`. macOS blocks it the first time: on
     macOS 15 or later open *System Settings → Privacy & Security*, click *Open Anyway*
     next to the message about the file, then double-click again; on older versions
     right-click the file and choose *Open*. If it asks whether the terminal may access
     your Documents folder, allow it.
   - Windows: double-click `start-windows.bat`. If SmartScreen appears, choose
     *More info* and then *Run anyway*.

What happens, in order:

1. The starter reads `tools-release.json`, which pins the exact tools release (tag,
   file name, SHA-256).
2. It downloads that release from the `4dcitygml/tools` releases page and verifies the
   checksum. If the checksum does not match, nothing is extracted and the starter stops.
3. The tools are extracted to `~/Documents/citygml-tools/citygml-hub/`.
4. The hub opens in your browser at `http://localhost:8760/`, already connected to this
   city. Keep the terminal window open while you work; closing it stops the tools.

The download happens the first time and again whenever the city pins a newer tools
release; the starter then replaces the old copy after verifying the new one. Otherwise
later starts skip straight to step 4. Your
own copy of the city data is created by the hub in the next section; you never have to
download the repository yourself.

## 2. What you need

- macOS 12 or later, or Windows 10 or later.
- macOS only: Apple's command line tools (`git` and `python3`). If macOS offers to
  install them the first time you run the starter, accept it. If the hub later reports
  that a component for the import is missing, follow `READ-ME-FIRST.html` in the
  extracted tools folder and start again; setup resumes where it stopped. Windows
  needs nothing: Git and Python travel inside the download.
- About 400 MB of disk space (tools plus your copy of the city data).
- A GitHub account is created, if you do not have one, during the *Connect* step
  below (free; an email address and a password).

## 3. Already using Git or GitHub? See the end of this guide

The starter kit is the simplest way in for everyone, including developers. If you
prefer to work with Git and GitHub directly, or want to build your own tool, read
[Advanced: Git, GitHub, and your own tools](#advanced-git-github-and-your-own-tools)
after the walkthrough. The rules that proposals must satisfy are the same in every
case.

## 4. Initial setup in the hub (three steps)

The hub shows a three-step setup screen until your working copy exists.

1. **Connect.** The screen states exactly what you authorize: the `public_repo`
   permission, which lets the tools create a copy of public repositories and open pull
   requests on your behalf. Click *Copy the number and open GitHub*, paste the number on
   the GitHub page that opens, and confirm. Signing in leaves no public trace; the
   authorization is listed only in your own GitHub settings, where you can revoke it at
   any time.
2. **Create a copy.** The hub forks this repository into your GitHub account. From this
   point the copy is public under your name, like any fork on GitHub.
3. **Import.** The hub clones your copy to `~/Documents/CityGML Data/` (a numbered
   folder is used if that already exists). Large cities take a few minutes.

Click *Start* when the third step is done. If a step fails, the button changes to a
retry; the most common cause is a network interruption.

## 5. The hub screen

After setup the hub lists the tools and your proposals:

- **Attribute Editor**: view and edit building attributes from a map, then send a
  proposal.
- **Texture Editor**: replace or add facade textures (only where the city has them).
- **Your contributions**: the proposals (and issues) you sent, with the result of the
  automated checks and the reviewer's status.

Each tool opens in a new browser tab on its own local port. The hub also shows where
your working copy is.

## 6. Your first change proposal

In the Attribute Editor:

1. Click a mesh frame on the map; the building footprints in that mesh appear.
2. Click a building. A 3D preview and an attribute card open.
3. Click a value to edit it. Changed values are shown in yellow.
4. When you confirm a value, a source field opens in the same row: choose the document
   you checked. A proposal cannot be sent while any changed attribute has no source.
5. Choose *Send your changes*, add a note or a URL if useful, and let the
   pre-submission check run (one target building, valid XML, only building data
   changed, sources recorded).
6. The proposal is created on this repository with a generated title and description
   in the repository's working language. The editor shows a *View your submission on
   GitHub* link; the hub lists it under your contributions.

Within a few minutes the automated checks comment on the proposal: a change summary, a
reviewability check, and a table of thirteen gates. Items marked as needing attention
come with instructions; fix them in the editor and send again from the same building,
and the checks rerun. When everything passes, the maintainer reviews and merges. Your
name in the history is your GitHub account, the same as in any pull request.

## 7. Next time

Run the same starter again. Setup is skipped, and the hub opens directly. If the
checks report that your copy is behind the city (*base stale*), open your fork on
GitHub and choose *Sync fork → Update branch*, then start again.

## 8. Practice repositories

The sample cities are practice environments. Proposals, comments, and review there
are real GitHub history, but the data is periodically reset to its baseline, so a
merged practice change does not have to be "right"; it has to follow the rules. Use
them freely before working on a real city.

## 9. Troubleshooting

- *Port 8760 is already in use*: another hub is running. Close it or pass another
  port (macOS example): `python3 ~/Documents/citygml-tools/citygml-hub/program/hub.py --port 8761`.
- *SHA-256 mismatch*: the download was corrupted or altered. Run the starter again;
  if it keeps failing, report it through the channels in the organization's
  [SUPPORT.md](https://github.com/4dcitygml/.github/blob/main/SUPPORT.md).
- *`python3` or `git` not found (macOS)*: install Apple's command line tools with
  `xcode-select --install`, then start again.
- *The setup screen appears although setup was done*: the working copy was moved or
  deleted. Import again, or point `~/.citygml_attr_editor.json` at the new location.

## 10. Where things are, and how to remove them

| What | Where |
|---|---|
| The tools | `~/Documents/citygml-tools/` |
| Your working copy of the city | `~/Documents/CityGML Data/` |
| Sign-in token and settings | `~/.citygml_auth.json`, `~/.citygml_attr_editor.json`, `~/.citygml_git_credentials` |

To remove everything, delete those items and revoke *4dcitygml hub* under
*Settings → Applications → Authorized OAuth Apps* on GitHub. Your fork and any
proposals you sent remain on GitHub; delete the fork from its settings page if you
no longer want it.

## Advanced: Git, GitHub, and your own tools

Everything the hub does is ordinary Git and GitHub, so you may skip the hub entirely.

- **Clone and branch by hand.** `git clone` this repository (or your fork), edit the
  CityGML with any editor, commit, and open a pull request. Every GitHub feature is
  available to you: forks, branches, the web editor, Codespaces, the API, the CLI,
  Actions on your fork.
- **The rules live in the pull request, not in the tool.** The automated checks apply
  the same thirteen gates to every proposal, however it was made. Before your first
  manual proposal read the [PR operations guide](pr-operations.md) (one change = one
  building, commit trailers, the reason section, byte-preserving edits), the
  [source recording rules](provenance-rules.md), and the machine-readable
  [PR Exchange Contract](https://github.com/4dcitygml/tools/blob/main/docs/exchange-contract.md),
  which states exactly what CI enforces and offers a local checker that runs the same
  code as CI.
- **Build your own tool.** Any program that produces proposals satisfying the contract is
  welcome, from a script to a full editor or a QGIS plugin. Add a `Created-By:` trailer
  so maintainers can tell clients apart, use the practice repositories as your sandbox,
  and tell us about it in an issue on `4dcitygml/tools`.
- **Where the hub's copy lives.** If you also use the hub, its working copy is the clone
  under `~/Documents/CityGML Data/`; the hub reads the connected city from the clone's
  `origin` remote, so pointing that clone at another fork or branch works as expected.
