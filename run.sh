#!/bin/bash
set -e

echo "Starting Job Search AI Assistant..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit 1
fi

# Remove the old environment to ensure a clean slate
ENV_NAME="jobsearch"
if conda env list | grep -q "$ENV_NAME"; then
    echo "Removing existing Conda environment '$ENV_NAME' to ensure a clean setup..."
    conda env remove -n $ENV_NAME -y
fi

# Create the conda environment from conda-forge
echo "Creating new Conda environment '$ENV_NAME' from conda-forge..."
conda create --name $ENV_NAME --file conda-requirements.txt -c conda-forge -y

# Install pip dependencies
echo "Installing pip dependencies..."
conda run -n $ENV_NAME pip install -r requirements.txt

# Launch the application
echo "Launching the application..."
conda run -n $ENV_NAME streamlit run app.py
