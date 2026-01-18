@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   YOUTUBE FACELESS VIDEO GENERATOR - ONE CLICK AUTOMATION
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Set the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check if virtual environment exists
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [SETUP] Virtual environment created successfully!
)

:: Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade dependencies
echo [SETUP] Installing dependencies...
python -m pip install --upgrade pip -q 2>nul
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install.
    echo Continuing anyway...
)

:: Check if .env file exists
if not exist ".env" (
    echo.
    echo ============================================================
    echo   API KEYS CONFIGURATION REQUIRED
    echo ============================================================
    echo.
    echo No .env file found. Creating from template...
    
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo.
        echo IMPORTANT: Please edit the .env file with your API keys:
        echo   - GEMINI_API_KEY (Google Gemini for AI script generation)
        echo   - GROQ_API_KEY (Groq for faster AI script generation)
        echo   - PEXELS_API_KEY (Pexels for stock video footage)
        echo   - PIXABAY_API_KEY (Pixabay for additional stock footage)
        echo.
        echo Get your free API keys from:
        echo   - Gemini: https://makersuite.google.com/app/apikey
        echo   - Groq: https://console.groq.com/keys
        echo   - Pexels: https://www.pexels.com/api/
        echo   - Pixabay: https://pixabay.com/api/docs/
        echo.
        notepad ".env"
        echo.
        echo After editing .env, run this script again.
        pause
        exit /b 0
    ) else (
        echo ERROR: .env.example not found!
        pause
        exit /b 1
    )
)

:: Main menu
:menu
cls
echo ============================================================
echo   YOUTUBE FACELESS VIDEO GENERATOR
echo ============================================================
echo.
echo   1. Generate Video (Enter topic manually)
echo   2. Show Trending Topics (Monetization Focused)
echo   3. Interactive Mode (Step-by-step prompts)
echo   4. Quick Generate (Use suggested topic)
echo   5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto manual
if "%choice%"=="2" goto trends
if "%choice%"=="3" goto interactive
if "%choice%"=="4" goto quick
if "%choice%"=="5" goto end
goto menu

:manual
echo.
set /p topic="Enter video topic: "
if "%topic%"=="" (
    echo ERROR: Topic cannot be empty!
    pause
    goto menu
)
set /p length="Enter video length in minutes (default: 8): "
if "%length%"=="" set length=8
set /p ai="Choose AI provider (auto/groq/gemini/ollama, default: auto): "
if "%ai%"=="" set ai=auto

echo.
echo ============================================================
echo   GENERATING VIDEO
echo ============================================================
echo   Topic: %topic%
echo   Length: %length% minutes
echo   AI Provider: %ai%
echo ============================================================
echo.

cd scripts
python master_automation.py --topic "%topic%" --length %length% --ai %ai%
cd ..

echo.
echo ============================================================
echo   VIDEO GENERATION COMPLETE!
echo ============================================================
echo.
echo Your video files are in the scripts/projects folder.
echo.
pause
goto menu

:trends
echo.
echo ============================================================
echo   FETCHING TRENDING TOPICS...
echo ============================================================
echo.
cd scripts
python master_automation.py --suggest-topics
cd ..
echo.
pause
goto menu

:interactive
echo.
cd scripts
python master_automation.py --interactive
cd ..
echo.
pause
goto menu

:quick
echo.
echo ============================================================
echo   QUICK GENERATE - HIGH CPM TOPICS
echo ============================================================
echo.
echo Select a topic category:
echo   1. Finance (CPM: $15-$50)
echo   2. Technology (CPM: $10-$30)
echo   3. Business (CPM: $12-$35)
echo   4. Health (CPM: $10-$25)
echo   5. Education (CPM: $8-$20)
echo.
set /p cat="Enter category (1-5): "

if "%cat%"=="1" set topic=5 Investment Mistakes That Cost You Thousands
if "%cat%"=="2" set topic=AI Tools That Will Change Your Life
if "%cat%"=="3" set topic=Business Ideas You Can Start Today
if "%cat%"=="4" set topic=Morning Habits of Successful People
if "%cat%"=="5" set topic=Skills That Will Make You Rich

if "%topic%"=="" (
    echo Invalid selection!
    pause
    goto menu
)

echo.
echo Selected topic: %topic%
echo.
set /p confirm="Generate video with this topic? (y/n): "
if /i not "%confirm%"=="y" goto menu

echo.
echo ============================================================
echo   GENERATING VIDEO
echo ============================================================
echo   Topic: %topic%
echo   Length: 8 minutes
echo   AI Provider: auto
echo ============================================================
echo.

cd scripts
python master_automation.py --topic "%topic%" --length 8 --ai auto
cd ..

echo.
echo ============================================================
echo   VIDEO GENERATION COMPLETE!
echo ============================================================
echo.
pause
goto menu

:end
echo.
echo Thank you for using YouTube Faceless Video Generator!
echo.
call venv\Scripts\deactivate.bat 2>nul
exit /b 0
