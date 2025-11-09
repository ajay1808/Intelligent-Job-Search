import os
import docx
from PyPDF2 import PdfReader
from io import BytesIO

RESUMES_DIR = "data/resumes"
JDS_DIR = "data/job_descriptions"
USER_DATA_CACHE_DIR = "cache/user_data"

def save_uploaded_file(uploaded_file, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def cache_user_file(uploaded_file, file_type):
    """Cache user uploaded file (resume, jd, or template)."""
    if not os.path.exists(USER_DATA_CACHE_DIR):
        os.makedirs(USER_DATA_CACHE_DIR)
    
    # Remove old file of the same type
    for f in os.listdir(USER_DATA_CACHE_DIR):
        if f.startswith(file_type):
            os.remove(os.path.join(USER_DATA_CACHE_DIR, f))

    file_ext = os.path.splitext(uploaded_file.name)[1]
    cache_path = os.path.join(USER_DATA_CACHE_DIR, f"{file_type}{file_ext}")
    with open(cache_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return cache_path

def get_cached_user_file(file_type):
    """Get the path of a cached user file."""
    if not os.path.exists(USER_DATA_CACHE_DIR):
        return None
    for f in os.listdir(USER_DATA_CACHE_DIR):
        if f.startswith(file_type):
            return os.path.join(USER_DATA_CACHE_DIR, f)
    return None

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return ""

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_latex(latex_content):
    """A simple function to strip LaTeX commands and extract text."""
    # This is a basic implementation and might not handle all LaTeX complexities.
    # Remove commands with arguments
    import re
    text = re.sub(r'\\[a-zA-Z]+(\*|\[.*?\])?\{.*?\}', '', latex_content)
    # Remove commands without arguments
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Remove environments
    text = re.sub(r'\\begin\{.*?\}|\\end\{.*?\}', '', text)
    # Remove comments
    text = re.sub(r'%.*?\n', '', text)
    # Remove math mode content
    text = re.sub(r'\$.*?\$', '', text)
    # Remove excess whitespace
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    return text
