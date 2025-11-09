#!/bin/bash
echo "Setting up Job Search AI Assistant..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install Python 3 and try again."
    exit
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the application, use the following command:"
echo "source .venv/bin/activate && streamlit run app.py"
