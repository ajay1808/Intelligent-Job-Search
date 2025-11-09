# Project Setup and Execution Guide

This guide provides instructions on how to set up the environment and run the Job Search AI Assistant application.

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) installed.
-   Python 3.10

### 2. Clone the Repository

```bash
git clone https://github.com/ajay1808/Intelligent-Job-Search.git
cd Intelligent-Job-Search
```

### 3. Create and Activate the Conda Environment

This project uses a Conda environment to ensure consistency. The following commands will create a new environment named `jobsearch` with Python 3.10 and activate it.

```bash
conda create -n jobsearch python=3.10 -y
conda activate jobsearch
```

### 4. Install Dependencies

Install all the required Python packages into your new environment using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## How to Run

With the `jobsearch` environment still active, run the application using the following command:

```bash
python -m streamlit run app.py
```

Using `python -m streamlit` ensures that you are running the version of Streamlit installed in your Conda environment, preventing potential path issues. The application will open in your default web browser.

## 5. Project Structure

```
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .gitignore              # Files to be ignored by Git
├── api_keys/               # Stores API keys
├── cache/                  # Caches job search results
├── data/
│   ├── job_descriptions/   # Stores uploaded job descriptions
│   └── resumes/            # Stores uploaded resumes
├── src/
│   ├── __init__.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── jd_analyzer.py
│   │   └── resume_analyzer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_keys.py
│   │   ├── caching.py
│   │   └── file_operations.py
│   └── web/
│       ├── __init__.py
│       └── job_search.py
└── templates/
    └── resume_template.tex # LaTeX resume template
```

## 6. How to Use the Application

1.  **Provide API Key**: Select your desired LLM provider from the sidebar and enter your API key. The key will be saved locally for future use.
2.  **Upload Documents**: Upload your resume and an ideal job description in PDF or DOCX format.
3.  **Analyze**: Click the "Analyze" button to get insights into your resume, the job description, and a gap analysis.
4.  **Find Jobs**: Click "Find Matching Jobs" to search for relevant job postings. The results will be cached to avoid repeated searches.
5.  **Generate Materials**: Select a job from the search results and click "Generate" to create a tailored resume and cover letter.
