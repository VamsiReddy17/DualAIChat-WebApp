@echo off
title Dual AI Chat - Stopping
echo ============================================
echo        Dual AI Chat - Stopping App
echo ============================================
echo.

:: Kill Backend (Python/Uvicorn)
echo [1/2] Stopping Backend (Python/Uvicorn)...
taskkill /F /FI "WINDOWTITLE eq DualAI - Backend*" >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo    Backend stopped.

:: Kill Frontend (Node/Vite)
echo [2/2] Stopping Frontend (Node/Vite)...
taskkill /F /FI "WINDOWTITLE eq DualAI - Frontend*" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo    Frontend stopped.

echo.
echo ============================================
echo   Both servers have been stopped.
echo ============================================
echo.
echo Press any key to close...
pause >nul
