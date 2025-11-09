@echo off
echo "Setting up Job Search AI Assistant using Conda..."

REM Check if conda is installed
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit /b
)

REM Create a conda environment
set ENV_NAME="jobsearch"
echo "Creating Conda environment '%ENV_NAME%'..."
conda create -n %ENV_NAME% python=3.9 -y

REM Activate the environment and install dependencies
echo "Installing dependencies from requirements.txt..."
call conda activate %ENV_NAME%
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the application, use the following command:"
echo "conda activate %ENV_NAME% && streamlit run app.py"
