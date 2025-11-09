@echo off
echo "Starting Job Search AI Assistant..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Create and set up the conda environment if it doesn't exist
set ENV_NAME="jobsearch"
conda env list | findstr /C:%ENV_NAME% >nul
if %errorlevel% neq 0 (
    echo "Conda environment '%ENV_NAME%' not found. Creating it now..."
    conda create -n %ENV_NAME% python=3.9 -y
    
    echo "Installing dependencies from requirements.txt..."
    call conda activate %ENV_NAME%
    pip install -r requirements.txt
) else (
    echo "Conda environment '%ENV_NAME%' already exists."
)

REM Activate the environment and run the application
echo "Activating environment and launching the application..."
call conda activate %ENV_NAME%
streamlit run app.py
