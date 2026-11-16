@echo off
title Push VeriMath to GitHub (CAAPPP)
echo ========================================================
echo   Pushing VeriMath to GitHub...
echo   Target: https://github.com/abdullahmosbah11-cmyk/CAAPPP.git
echo ========================================================
cd /d "%~dp0"

echo [1/2] Verifying remote origin...
git remote set-url origin https://github.com/abdullahmosbah11-cmyk/CAAPPP.git

echo [2/2] Pushing main branch...
git push -u origin main

echo ========================================================
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] VeriMath uploaded successfully to GitHub!
    echo Check it at: https://github.com/abdullahmosbah11-cmyk/CAAPPP
) else (
    echo [ERROR] Push failed. If this is your first time,
    echo sign in when your browser window opens, then run this file again.
)
echo ========================================================
pause
