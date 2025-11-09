#!/bin/bash
set -e

echo "Starting Job Search AI Assistant..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit 1
fi

# Create or update the conda environment
ENV_NAME="jobsearch"
echo "Ensuring Conda environment '$ENV_NAME' is up to date..."
conda create --name $ENV_NAME --file conda-requirements.txt -y

# Activate the environment and install pip dependencies
echo "Activating environment and installing pip dependencies..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME
pip install -r requirements.txt

# Launch the application
echo "Launching the application..."
streamlit run app.py
