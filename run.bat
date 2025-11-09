@echo off
echo "Starting Job Search AI Assistant..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Create or update the conda environment
set ENV_NAME="jobsearch"
echo "Ensuring Conda environment '%ENV_NAME%' is up to date..."
conda create --name %ENV_NAME% --file conda-requirements.txt -y

REM Activate the environment and install pip dependencies
echo "Activating environment and installing pip dependencies..."
call conda activate %ENV_NAME%
pip install -r requirements.txt

REM Launch the application
echo "Launching the application..."
streamlit run app.py
