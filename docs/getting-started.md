<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Getting started: from clone to your first change proposal

This guide walks through the practice flow end to end: getting this repository onto
your computer, starting the shared editing tools, connecting them to your GitHub
account, and sending your first change proposal (a pull request). It takes about
15 minutes the first time. Nothing here changes the city data directly: every edit
becomes a proposal that is checked automatically and approved by the city's
maintainers.

After you send: the automated checks run within minutes and post their report, and
the city's maintainers approve — you only need to act if someone asks
you to change something. For the rules that proposals must follow, see the [PR operations guide](pr-operations.md)
and the [source recording rules](provenance-rules.md). For what may be contributed,
see the [data contribution policy](data-contribution-policy.md).

## 1. Quick start: one command

You do not need Git, a GitHub account, or a copy of the city data to begin. The
tools guide you through everything that is missing. The one line below is the
whole installation; it is the same on every computer and never gets stale.

- **macOS**: open *Terminal* (Spotlight → "Terminal"), paste the line from this
  repository's README (*Get started*), press Return:

  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/4dcitygml/tools/install-v1/install/citygml.sh)" -- 4dcitygml/sample-tokyo-station
  ```
  If macOS offers to install the *command line developer tools*, accept and run the
  line again afterwards. If it asks whether the terminal may access your Documents
  folder, allow it.
- **Windows**: open *PowerShell* (Start → "PowerShell"), paste the README's line, press
  Enter. Git and Python travel inside the download; nothing else is installed.

What happens, in order:

1. The command fetches the newest release of the editing tools from
   `4dcitygml/tools` and verifies it against the SHA-256 digest GitHub publishes
   for that file. If the digest does not match, nothing is installed and the command stops.
2. The tools are placed in `~/Documents/citygml-tools/citygml-hub/<version>/`, and a
   copy of the launcher script stays in `~/Documents/citygml-tools/`.
3. The hub opens in your browser, already connected to this city. Keep the terminal
   window open while you work; closing it stops the tools.
4. After the setup below, the hub offers to create a **desktop icon** for this city.
   From then on you open the tools with that icon; the terminal line is only for the
   first time (or for another computer).

This repository contains data, documents and settings only. Every program that runs
on your computer comes from `4dcitygml/tools` releases — the same for every city.

## 2. What you need

- macOS 12 or later, or Windows 10 or later.
- macOS only: Apple's command line tools (`git` and `python3`). If macOS offers to
  install them the first time you run the command, accept it. Windows needs nothing:
  Git and Python travel inside the download.
- About 400 MB of disk space (tools plus your copy of the city data).
- A GitHub account is created, if you do not have one, during the *Connect* step
  below (free; an email address and a password).

## 3. Already using Git or GitHub? See the end of this guide

The one-line command is the simplest way in for everyone, including developers. If you
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
reviewability check, and a table of fourteen gates. Items marked as needing attention
come with instructions; fix them in the editor and send again from the same building,
and the checks rerun. When everything passes, the city's maintainers approve, and the change is merged. Your
name in the history is your GitHub account, the same as in any pull request.

## 7. Next time

Double-click the desktop icon the hub created (or run the same one-line command
again — it is safe to repeat). Setup is skipped, and the hub opens directly. The hub
brings your copy of the city data up to date in the background and shows the state
on its screen; if a proposal is still reported as behind the city (*base stale*), send
it again from the same building after the sync has completed.

When a newer version of the tools is published, the hub shows a banner. *Get it now*
downloads and verifies it; the new version is used from the next start. Nothing is
downloaded or restarted without your click.

## 8. Practice repositories

The sample cities are practice environments. Proposals, comments, and review there
are real GitHub history, but the data is periodically reset to its baseline, so a
merged practice change does not have to be "right"; it has to follow the rules. Use
them freely before working on a real city.

## 9. Troubleshooting

- *The browser opened a different port than last time*: another hub (another city)
  was already running on the usual port, so this one stepped to the next free port. Both
  keep working; each city has its own window.
- *SHA-256 mismatch*: the download was corrupted or altered. Run the command again;
  if it keeps failing, report it through the channels in the organization's
  [SUPPORT.md](https://github.com/4dcitygml/.github/blob/main/SUPPORT.md).
- *`python3` or `git` not found (macOS)*: install Apple's command line tools with
  `xcode-select --install`, then run the command again.
- *The setup screen appears although setup was done*: the working copy was moved or
  deleted. Import again, or point the city's entry in `~/.citygml_attr_editor.json`
  (`cities`) at the new location.
- *The tools cannot be updated (offline)*: the hub keeps running the installed version;
  the banner returns when you are online.

## 10. Where things are, and how to remove them

| What | Where |
|---|---|
| The tools (one folder per version) and the launcher script | `~/Documents/citygml-tools/` |
| The desktop icon | wherever you dragged it (it only points at the launcher script) |
| Your working copy of the city | `~/Documents/CityGML Data/` |
| Accounts and settings | `~/.citygml/auth/` (one file per connected GitHub account), `~/.citygml_attr_editor.json` |

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
  the same fourteen gates to every proposal, however it was made. Before your first
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
