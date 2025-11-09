@echo off
echo "Setting up Job Search AI Assistant..."

REM Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "Python could not be found. Please install Python and try again."
    exit /b
)

REM Create a virtual environment
echo "Creating virtual environment..."
python -m venv .venv

REM Activate the virtual environment and install dependencies
echo "Installing dependencies from requirements.txt..."
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the application, use the following command:"
echo ".venv\Scripts\activate.bat && streamlit run app.py"
