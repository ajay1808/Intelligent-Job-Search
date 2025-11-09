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

REM Create the conda environment
echo "Creating new Conda environment '%ENV_NAME%'..."
conda create --name %ENV_NAME% --file conda-requirements.txt -y

REM Activate the environment and install pip dependencies
echo "Activating environment and installing pip dependencies..."
call conda activate %ENV_NAME%
pip install -r requirements.txt

REM Launch the application
echo "Launching the application..."
streamlit run app.py
