@echo off
echo "Starting Job Search AI Assistant..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Remove the old environment to ensure a clean slate
set ENV_NAME="jobsearch"
conda env list | findstr /C:%ENV_NAME% >nul
if %errorlevel% equ 0 (
    echo "Removing existing Conda environment '%ENV_NAME%' to ensure a clean setup..."
    conda env remove -n %ENV_NAME% -y
)

REM Create the conda environment from the environment.yml file
echo "Creating new Conda environment from environment.yml..."
conda env create -f environment.yml

REM Activate the environment and run the application
echo "Activating environment and launching the application..."
call conda activate %ENV_NAME%
streamlit run app.py
