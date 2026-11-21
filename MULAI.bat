@echo off
rem DCI SEO Auditor - klik dua kali berkas ini untuk membuka menu.
rem Author: Duta Corpora Indonesia (DCI)
chcp 65001 >nul
title DCI SEO Auditor
cd /d "%~dp0"
set "PY="
for %%C in ("py -3" "python" "python3") do (
  if not defined PY (
    %%~C -c "import sys" >nul 2>nul && set "PY=%%~C"
  )
)
if not defined PY goto tanpapython
%PY% -X utf8 alat\menu.py
goto selesai

:tanpapython
echo.
echo ============================================================
echo   Python belum terpasang di komputer ini.
echo ============================================================
echo.
echo   1. Buka https://www.python.org/downloads/ lalu unduh Python.
echo   2. Saat memasang, CENTANG kotak "Add python.exe to PATH".
echo   3. Selesai memasang, klik dua kali MULAI.bat lagi.
echo.
echo   Bila komputer ini dikelola kantor, minta bantuan admin IT.

:selesai
echo.
pause
