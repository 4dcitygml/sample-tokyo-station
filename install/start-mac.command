#!/bin/bash
# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
# Starts the shared 4dcitygml editing tool connected to THIS city.
# The tools release is pinned in tools-release.json (tag + asset name + SHA-256).
# Fail-closed: nothing is downloaded until the pin is filled in, and nothing is
# executed unless the downloaded archive matches the pinned SHA-256.
set -e
# 設定ファイルを探す: リポ内 install/ から実行された場合は ../、
# 「はじめるキット」（設定同梱の小zip）から実行された場合は ./ にある
cd "$(dirname "$0")"
[ -f "../4dcitygml.json" ] && cd ..
export CITYGML_UPSTREAM="$(python3 -c 'import json; print(json.load(open("4dcitygml.json"))["repo"])')"

MANIFEST="tools-release.json"
[ -f "install/tools-release.json" ] && MANIFEST="install/tools-release.json"
read -r TAG ASSET SHA <<EOF
$(python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
e = m.get("macos") or {}
print(m.get("tag") or "-", e.get("asset") or "-", e.get("sha256") or "-")
PY
)
EOF
if [ "$TAG" = "-" ] || [ "$ASSET" = "-" ] || [ "$SHA" = "-" ]; then
  echo "配布ツールのリリースがまだ確定していません（install/tools-release.json が未記入です）。" >&2
  echo "管理者向け: 最初の tools リリース後に tag / asset / sha256 を記入してください。" >&2
  exit 1
fi

DEST="$HOME/Documents/citygml-tools"
APP="$DEST/citygml-hub/program/hub.py"
MARK="$DEST/citygml-hub/.release-tag"   # tag of the installed release; a different pin triggers an update
INSTALLED="$(cat "$MARK" 2>/dev/null || true)"
if [ ! -f "$APP" ] || [ "$INSTALLED" != "$TAG" ]; then
  if [ -f "$APP" ]; then echo "編集ツールを更新しています（$INSTALLED → $TAG）..."; else echo "Downloading the editing tool ($TAG)..."; fi
  mkdir -p "$DEST"
  TMP_ZIP="$(mktemp "${TMPDIR:-/tmp}/citygml-hub.XXXXXX")"
  curl -fL "https://github.com/4dcitygml/tools/releases/download/$TAG/$ASSET" -o "$TMP_ZIP"
  ACTUAL="$(shasum -a 256 "$TMP_ZIP" | cut -d' ' -f1)"
  if [ "$ACTUAL" != "$SHA" ]; then
    rm -f "$TMP_ZIP"
    echo "ダウンロードした zip の SHA-256 が一致しません（期待 $SHA / 実際 $ACTUAL）。中断します。" >&2
    exit 1
  fi
  # Unpack next to the old copy first; only a verified, complete archive replaces it.
  STAGE="$(mktemp -d "${TMPDIR:-/tmp}/citygml-hub-stage.XXXXXX")"
  unzip -oq "$TMP_ZIP" -d "$STAGE"
  rm -f "$TMP_ZIP"
  rm -rf "$DEST/citygml-hub"
  mv "$STAGE/citygml-hub" "$DEST/citygml-hub"
  rmdir "$STAGE" 2>/dev/null || true
  printf '%s\n' "$TAG" > "$MARK"
fi
exec python3 "$APP"
