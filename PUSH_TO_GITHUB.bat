@echo off
title Push FastDL to GitHub
color 0b
cd /d "%~dp0"
echo ========================================================
echo       CS DARK 1.6 - UPLOAD FASTDL TO GITHUB
echo ========================================================
echo.
echo Please create a new PUBLIC repository on GitHub (e.g. csdark-fastdl).
echo Then copy the repository HTTPS link (e.g. https://github.com/Username/csdark-fastdl.git).
echo.
set /p REPO_URL="Paste your GitHub Repository URL here: "
if "%REPO_URL%"=="" (
    echo [ERROR] No URL entered!
    pause
    exit /b
)
echo.
echo [1/2] Linking repository...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
echo.
echo [2/2] Pushing all 267 files to GitHub (main branch)...
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================================
    echo   SUCCESS! All assets uploaded to GitHub successfully!
    echo ========================================================
    echo.
    echo Next easy steps:
    echo 1. Open your repository on GitHub.
    echo 2. Go to 'Settings' (icon at the top) -> 'Pages' (left sidebar).
    echo 3. Under 'Build and deployment', choose Branch: 'main' -> click 'Save'.
    echo 4. Copy your Pages URL (e.g. https://username.github.io/csdark-fastdl/) and send it to me!
    echo ========================================================
) else (
    echo.
    echo [NOTE] If GitHub asked for login, complete the sign-in prompt.
)
pause
