@echo off
echo Setting up AI Code Review Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Next steps:
echo 1. Copy env_example.txt to .env
echo 2. Edit .env with your Hugging Face API token
echo 3. Run: python start.py
echo.
echo For Hugging Face API token:
echo - Go to https://huggingface.co/settings/tokens
echo - Create a new token with read permissions
echo.
pause 