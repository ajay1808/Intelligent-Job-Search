#!/bin/bash
echo "Setting up Job Search AI Assistant using Conda..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit
fi

# Create a conda environment
ENV_NAME="jobsearch"
echo "Creating Conda environment '$ENV_NAME'..."
conda create -n $ENV_NAME python=3.9 -y

# Activate the environment and install dependencies
echo "Installing dependencies from requirements.txt..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the application, use the following command:"
echo "conda activate $ENV_NAME && streamlit run app.py"
