#!/bin/bash
set -e

echo "Starting Job Search AI Assistant..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit 1
fi

# Create or update the conda environment from the environment.yml file
echo "Ensuring Conda environment 'jobsearch' is up to date..."
conda env update --file environment.yml --prune

# Activate the environment and run the application
echo "Activating environment and launching the application..."
eval "$(conda shell.bash hook)"
conda activate jobsearch
streamlit run app.py
