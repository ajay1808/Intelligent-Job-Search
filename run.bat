@echo off
echo "Starting Job Search AI Assistant..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Create or update the conda environment from the environment.yml file
echo "Ensuring Conda environment 'jobsearch' is up to date..."
conda env update --file environment.yml --prune

REM Activate the environment and run the application
echo "Activating environment and launching the application..."
call conda activate jobsearch
streamlit run app.py
