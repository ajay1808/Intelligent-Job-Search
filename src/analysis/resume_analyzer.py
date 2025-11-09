import google.generativeai as genai
import json
import os
from datetime import datetime, timedelta
import hashlib
from typing import Dict, Any

CACHE_DIR = "cache/analysis"
CACHE_DURATION_DAYS = 7

def _get_cache_key(text: str, analysis_type: str) -> str:
    """Generate a unique cache key based on text content"""
    return hashlib.md5(f"{text}_{analysis_type}".encode()).hexdigest()

def _load_from_cache(cache_key: str) -> Dict[str, Any]:
    """Load analysis results from cache if valid"""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_data = json.load(f)
            if datetime.fromisoformat(cached_data["timestamp"]) + timedelta(days=CACHE_DURATION_DAYS) > datetime.now():
                return cached_data["data"]
    return None

def _save_to_cache(cache_key: str, data: dict):
    """Save analysis results to cache"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    with open(cache_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "data": data
        }, f)

def analyze_resume(resume_text: str, api_key: str, api_provider: str = "Gemini") -> Dict[str, Any]:
    """
    Analyzes the resume text to extract key information using a faster model for basic analysis.
    """
    if api_provider != "Gemini":
        return {"error": "This implementation currently only supports Gemini."}

    cache_key = _get_cache_key(resume_text, "resume_analysis")
    cached_result = _load_from_cache(cache_key)
    if cached_result:
        return cached_result

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Analyze the following resume and provide a summary of the candidate's strengths, areas for development, skills, and experience.
    Format the output as a JSON object with the keys "strengths", "areas_for_development", "skills", and "experience".
    The "skills" key should be a list of objects with "name" and optional "proficiency" fields.

    Resume:
    {resume_text}
    """

    try:
        response = model.generate_content(prompt + "\nRespond only with valid JSON.")
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(cleaned_text)
        _save_to_cache(cache_key, result)
        return result
    except Exception as e:
        raise ValueError(f"Error during resume analysis with Gemini: {e}") from e

def ats_analysis(resume_text: str, jd_text: str, api_key: str, api_provider: str = "Gemini") -> Dict[str, Any]:
    """
    Performs an ATS-like analysis of the resume against a job description.
    Uses caching to avoid repeated analysis of the same resume-JD pair.
    """
    if api_provider != "Gemini":
        return {"error": "This implementation currently only supports Gemini."}

    cache_key = _get_cache_key(f"{resume_text}_{jd_text}", "ats_analysis")
    cached_result = _load_from_cache(cache_key)
    if cached_result:
        return cached_result

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')  # Using pro model for more accurate analysis

    prompt = f"""
    Analyze the following resume against the job description from an ATS perspective.
    Provide a detailed analysis of the match, including specific keywords found and suggestions for improvement.
    Format the output as a JSON object with the keys "ats_score", "keywords_match", and "suggestions".
    The "ats_score" should be a percentage string, "keywords_match" should be a list of strings, and "suggestions" should be a list of improvement recommendations.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(cleaned_text)
        _save_to_cache(cache_key, result)
        return result
    except Exception as e:
        raise ValueError(f"Error during ATS analysis with Gemini: {e}") from e
