# Intelligent Job Search Assistant

This AI-powered assistant streamlines your job search by analyzing your resume against an ideal job description, finding relevant job postings, and generating tailored application materials.

## Features

-   **AI-Powered Analysis**: Get deep insights into your resume, an ideal job description, and a gap analysis between the two.
-   **Smart Job Search**: Automatically finds relevant, recent job postings based on your profile.
-   **ATS-Friendly Materials**: Generate a tailored LaTeX resume and a professional cover letter for any job you select.
-   **Performance Comparison**: See a "Before vs. After" ATS analysis to understand how the generated resume improves your chances.
-   **Local Caching**: Caches job searches and analysis to speed up subsequent uses and reduce API costs.

## Getting Started

### Prerequisites

-   An Anaconda or Miniconda distribution of Python.
-   Git

## Quickstart

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ajay1808/Intelligent-Job-Search.git
    cd Intelligent-Job-Search
    ```

2.  **Run the application:**

    -   **For macOS and Linux:**
        ```bash
        ./run.sh
        ```

    -   **For Windows:**
        ```bat
        run.bat
        ```
    When you run the script, it will automatically create a Conda environment using the reliable `conda-forge` channel, install the core dependencies from `conda-requirements.txt`, install the remaining packages from `requirements.txt`, and then launch the application.

The application should now be open and accessible in your web browser.

## How to Use the Application

1.  **Provide API Keys**: In the sidebar, enter your API keys for Gemini (for analysis) and Perplexity (for job searching). Your keys are saved locally for future sessions.
2.  **Upload Documents**: Upload your resume and an ideal job description. You can also provide a custom LaTeX resume template.
3.  **Analyze and Search**: Click "Analyze and Search for Jobs" to kick off the process.
4.  **Generate Materials**: Select a job from the results list and click "Generate" to create a tailored resume and cover letter.
5.  **Manage History**: View previously found jobs or clear your search history from the sidebar.
