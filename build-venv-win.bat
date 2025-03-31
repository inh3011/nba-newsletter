@echo off

REM Check if Python is installed
C:\Users\inseong\AppData\Local\Programs\Python\Python313\python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.10 or higher.
    exit /b 1
)

REM Create virtual environment
C:\Users\inseong\AppData\Local\Programs\Python\Python313\python -m venv venv_win

REM Activate virtual environment
call venv_win\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install poetry
poetry install

echo Virtual environment setup complete.
