@echo off
echo "Starting Job Search AI Assistant..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Read version and set environment name
set /p VERSION=<VERSION
set ENV_NAME=jobsearch-v%VERSION%

REM Create the environment if it doesn't exist
conda env list | findstr /C:"%ENV_NAME% " >nul
if %errorlevel% neq 0 (
    echo "Conda environment '%ENV_NAME%' not found. Creating it now..."
    
    REM Temporarily set the environment name for creation
    (echo name: %ENV_NAME% && findstr /v /i "name:" environment.yml) > temp_env.yml
    conda env create -f temp_env.yml
    del temp_env.yml
) else (
    echo "Conda environment '%ENV_NAME%' already exists."
)

REM Activate the environment and run the application
echo "Activating environment '%ENV_NAME%' and launching the application..."
call conda activate %ENV_NAME%
streamlit run app.py
