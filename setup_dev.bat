@echo off
REM Windows Development Setup Script for T-Flow AI Medical Triage System
echo ================================
echo T-Flow AI Development Setup
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or 3.12 from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo 🔧 Installing/updating dependencies...

python -m pip install --upgrade pip
pip install -r backend\requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found
    echo Please copy .env.example to .env and fill in your API keys:
    echo   - GROQ_API_KEY
    echo   - SUPABASE_URL
    echo   - SUPABASE_ANON_KEY
    echo.
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Created .env from .env.example
        echo Please edit .env file with your actual API keys
    )
) else (
    echo ✅ .env file found
)

echo.
echo ================================
echo Setup complete! 🎉
echo ================================
echo.
echo To run the development server:
echo   1. Make sure .env file has your API keys
echo   2. Run: cd backend && python run_server.py
echo.
echo To run tests:
echo   python test.py
echo   python backend\system_check.py
echo.
echo API Documentation will be at: http://localhost:8000/docs
echo ================================

pause
