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

## 1. What you need

- A free GitHub account. You will sign in once; the tools remember it.
- macOS 12 or later, or Windows 10 or later.
- macOS only: Apple's command line tools (`git` and `python3`). If a dialog offers to
  install them the first time you run the starter, accept it; no other installation is
  needed. Windows needs nothing: Git and Python travel inside the download.
- About 400 MB of disk space (tools plus your copy of the city data).

## 2. Get this repository

Either of these works:

- **Clone** (recommended if you have Git):

  ```bash
  git clone <URL of this repository>
  ```

- **Download**: on the repository page choose *Code → Download ZIP* and unzip it.

You now have a folder with `install/`, `4dcitygml.json`, and the city data.

## 3. Start the tools

- macOS: double-click `install/start-mac.command`. If macOS says the file is from an
  unidentified developer, right-click it and choose *Open*. If it asks whether the
  terminal may access your Documents folder, allow it.
- Windows: double-click `install/start-windows.bat`. If SmartScreen appears, choose
  *More info* and then *Run anyway*.

What happens, in order:

1. The starter reads `install/tools-release.json`, which pins the exact tools release
   (tag, file name, SHA-256).
2. It downloads that release from the `4dcitygml/tools` releases page and verifies the
   checksum. If the checksum does not match, nothing is extracted and the starter stops.
3. The tools are extracted to `~/Documents/citygml-tools/citygml-hub/`.
4. The hub opens in your browser at `http://localhost:8760/`, already connected to this
   city. Keep the terminal window open while you work; closing it stops the tools.

The download happens only the first time. Later starts skip straight to step 4.

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
- **Your proposals**: the pull requests you sent, with the result of the automated
  checks and the reviewer's status.

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
   in the repository's working language, and the hub opens it.

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
  port: `python3 ~/Documents/citygml-tools/citygml-hub/program/hub.py --port 8761`.
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
