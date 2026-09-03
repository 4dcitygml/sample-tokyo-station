@echo off
rem Copyright (c) 2026 4dcitygml
rem SPDX-License-Identifier: Apache-2.0
rem Starts the shared 4dcitygml editing tool connected to THIS city.
rem All logic lives in start-windows.ps1 (pinned release + SHA-256 verification,
rem fail-closed). This wrapper only exists so users can double-click a .bat.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-windows.ps1"
if errorlevel 1 pause
