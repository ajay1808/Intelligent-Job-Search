#!/bin/bash
set -e

echo "Starting Job Search AI Assistant..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda and try again."
    exit 1
fi

# Read version and set environment name
VERSION=$(cat VERSION)
ENV_NAME="jobsearch-v$VERSION"

# Create the environment if it doesn't exist
if ! conda env list | grep -q "^$ENV_NAME\s"; then
    echo "Conda environment '$ENV_NAME' not found. Creating it now..."
    # Temporarily set the environment name for creation
    sed -i.bak "1s/.*/name: $ENV_NAME/" environment.yml
    conda env create -f environment.yml
    # Revert the change to environment.yml
    mv environment.yml.bak environment.yml
else
    echo "Conda environment '$ENV_NAME' already exists."
fi

# Activate the environment and run the application
echo "Activating environment '$ENV_NAME' and launching the application..."
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"
streamlit run app.py
