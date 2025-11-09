# Project Setup and Execution Guide

This guide provides instructions on how to set up the environment and run the Job Search AI Assistant application.

## 1. Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## 2. Environment Setup

It is highly recommended to use a virtual environment to manage project dependencies.

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

**On macOS and Linux:**

```bash
source .venv/bin/activate
```

**On Windows:**

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 4. Running the Application

Once the dependencies are installed, you can run the Streamlit application:

```bash
streamlit run app.py
```

The application should now be open and accessible in your web browser.

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
