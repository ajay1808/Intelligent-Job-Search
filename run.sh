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

# Create the conda environment from the environment.yml file
echo "Creating new Conda environment from environment.yml..."
conda env create -f environment.yml

# Activate the environment and run the application
echo "Activating environment and launching the application..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME
streamlit run app.py
