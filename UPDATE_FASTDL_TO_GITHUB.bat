@echo off
title Push FastDL Updates to GitHub
color 0a
cd /d "%~dp0"
echo ========================================================
echo       CS DARK 1.6 - SYNC FASTDL ASSETS TO GITHUB
echo ========================================================
echo.
echo Pushing updated .bz2 models and sounds to GitHub...
echo.
git push origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================================
    echo   SUCCESS! All compressed .bz2 assets are live on FastDL!
    echo ========================================================
) else (
    echo ========================================================
    echo   [FAILED] Please make sure you have internet access
    echo   and GitHub credentials configured.
    echo ========================================================
)
echo.
pause
