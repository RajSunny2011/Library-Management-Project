@echo off
REM Batch script to set up a Python virtual environment and install required packages

REM Set the virtual environment name
SET VENV_NAME=.env

REM Check if the virtual environment folder exists
IF NOT EXIST "%VENV_NAME%" (
    ECHO Creating virtual environment...
    python -m venv %VENV_NAME%
)

REM Activate the virtual environment
CALL "%VENV_NAME%\Scripts\activate.bat"

REM Install required packages from requirements.txt
IF EXIST "requirements.txt" (
    ECHO Installing packages from requirements.txt...
    pip install -r requirements.txt
) ELSE (
    ECHO No requirements.txt found, skipping installation.
)

ECHO Setup complete.
ECHO The virtual environment is now active.
pause
