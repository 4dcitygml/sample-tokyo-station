# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
# Starts the shared 4dcitygml editing tool connected to THIS city.
# The tools release is pinned in tools-release.json (tag + asset name + SHA-256).
# Fail-closed: nothing is downloaded until the pin is filled in, and nothing is
# executed unless the downloaded archive matches the pinned SHA-256.
$ErrorActionPreference = "Stop"

# 設定ファイルを探す: リポ内 install/ から実行された場合は ..\、
# 「はじめるキット」（設定同梱の小zip）から実行された場合は .\ にある
Set-Location $PSScriptRoot
if (Test-Path "..\4dcitygml.json") { Set-Location ".." }
$config = Get-Content "4dcitygml.json" -Raw | ConvertFrom-Json
$env:CITYGML_UPSTREAM = $config.repo

$manifestPath = "tools-release.json"
if (Test-Path "install\tools-release.json") { $manifestPath = "install\tools-release.json" }
$m = Get-Content $manifestPath -Raw | ConvertFrom-Json
$tag = $m.tag
$asset = $m.windows.asset
$sha = $m.windows.sha256
if (-not $tag -or -not $asset -or -not $sha) {
  Write-Host "配布ツールのリリースがまだ確定していません（install/tools-release.json が未記入です）。"
  Write-Host "管理者向け: 最初の tools リリース後に tag / asset / sha256 を記入してください。"
  exit 1
}

$dest = Join-Path $env:USERPROFILE "Documents\citygml-tools"
$app = Join-Path $dest "citygml-hub\program\hub.py"
$py = Join-Path $dest "citygml-hub\program\PythonPortable\python.exe"
$mark = Join-Path $dest "citygml-hub\.release-tag"   # tag of the installed release; a different pin triggers an update
$installed = if (Test-Path $mark) { (Get-Content $mark -Raw).Trim() } else { "" }

if (-not (Test-Path $app) -or $installed -ne $tag) {
  if (Test-Path $app) { Write-Host "編集ツールを更新しています（$installed → $tag）..." } else { Write-Host "Downloading the editing tool ($tag)..." }
  New-Item -ItemType Directory -Force $dest | Out-Null
  $tmp = Join-Path $env:TEMP "citygml-hub-download.zip"
  curl.exe -fLsS "https://github.com/4dcitygml/tools/releases/download/$tag/$asset" -o $tmp
  if ($LASTEXITCODE -ne 0) {
    Write-Host "ダウンロードに失敗しました。ネットワークを確認してください。"
    exit 1
  }
  $actual = (Get-FileHash $tmp -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -ne $sha.ToLowerInvariant()) {
    Remove-Item $tmp
    Write-Host "ダウンロードした zip の SHA-256 が一致しません（期待 $sha / 実際 $actual）。中断します。"
    exit 1
  }
  # Unpack next to the old copy first; only a verified, complete archive replaces it.
  $stage = Join-Path $env:TEMP "citygml-hub-stage"
  if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
  Expand-Archive -LiteralPath $tmp -DestinationPath $stage -Force
  Remove-Item $tmp
  $target = Join-Path $dest "citygml-hub"
  if (Test-Path $target) { Remove-Item $target -Recurse -Force }
  Move-Item (Join-Path $stage "citygml-hub") $target
  Remove-Item $stage -Recurse -Force
  Set-Content -Path $mark -Value $tag -NoNewline
}

if (-not (Test-Path $py)) {
  Write-Host "同梱 Python が見つかりません: $py"
  Write-Host "ダウンロードした配布物が壊れている可能性があります。$dest を削除してやり直してください。"
  exit 1
}
& $py $app
exit $LASTEXITCODE
