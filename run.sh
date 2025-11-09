#!/bin/bash
echo "Starting Job Search AI Assistant..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit
fi

# Create and set up the conda environment if it doesn't exist
ENV_NAME="jobsearch"
if ! conda env list | grep -q "$ENV_NAME"; then
    echo "Conda environment '$ENV_NAME' not found. Creating it now from environment.yml..."
    conda env create -f environment.yml
else
    echo "Conda environment '$ENV_NAME' already exists."
fi

# Activate the environment and run the application
echo "Activating environment and launching the application..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME
streamlit run app.py
