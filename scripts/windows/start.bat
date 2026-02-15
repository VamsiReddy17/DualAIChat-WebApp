@echo off
title Dual AI Chat - Launcher

:: Resolve project root (two levels up from scripts\windows)
set "PROJECT_ROOT=%~dp0..\.."

echo ============================================
echo        Dual AI Chat - Starting App
echo ============================================
echo.

:: Start Backend (FastAPI) in a new terminal window
echo [1/2] Starting Backend (FastAPI) on http://localhost:8000 ...
start "DualAI - Backend" cmd /k "cd /d %PROJECT_ROOT%\apps\backend && call venv\Scripts\activate && python run.py"

:: Small delay to let backend initialize first
timeout /t 3 /nobreak >nul

:: Start Frontend (Vite + React) in a new terminal window
echo [2/2] Starting Frontend (Vite) on http://localhost:5173 ...
start "DualAI - Frontend" cmd /k "cd /d %PROJECT_ROOT%\apps\frontend && npm run dev"

:: Wait a moment then open browser
timeout /t 4 /nobreak >nul
echo.
echo ============================================
echo   Both servers are running!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ============================================
echo.
echo Opening browser...
start http://localhost:5173

echo.
echo Close the two server windows to stop the app.
echo Press any key to close this launcher...
pause >nul
