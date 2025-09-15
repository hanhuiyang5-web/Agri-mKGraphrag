@echo off
echo =========================================
echo Agri-mGraphrag V2 Windows Setup Script
echo =========================================
echo.

REM Check Python version
python --version | findstr /C:"3.11" >nul || python --version | findstr /C:"3.12" >nul
if %errorlevel% neq 0 (
    echo ERROR: Python 3.11 or 3.12 required!
    echo Current version:
    python --version
    pause
    exit /b 1
)

echo ✓ Python version check passed

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv agri_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo ✓ Virtual environment created
echo.
echo Activating environment...
call agri_env\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing requirements...
pip install -r requirements_v2.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

REM Create directories
echo.
echo Creating directories...
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir logs 2>nul
mkdir models 2>nul

REM Copy example config
echo.
echo Setting up configuration...
copy config\config_example.yaml config\config.yaml 2>nul

echo.
echo ========================================
echo ✓ Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit config\config.yaml with your API keys
echo 2. Install and start Neo4j database
echo 3. Run: python demo_v2.py
echo.
echo To activate environment later:
echo   agri_env\Scripts\activate.bat
echo.
pause