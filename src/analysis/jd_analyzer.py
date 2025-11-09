import google.generativeai as genai
import json

def analyze_jd(jd_text, api_key, api_provider):
    """
    Analyzes the job description to extract key requirements.
    """
    if api_provider != "Gemini":
        return {"error": "This implementation currently only supports Gemini."}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')

    prompt = f"""
    Analyze the following job description and extract the key requirements.
    Format the output as a JSON object with the keys "required_skills", "experience_level", and "key_responsibilities".
    The "required_skills" key should be a simple list of strings.

    Job Description:
    {jd_text}
    """

    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_text)
    except Exception as e:
        raise ValueError(f"Error during JD analysis with Gemini: {e}") from e


def _normalize_skills(skills_list):
    normalized = []
    if not isinstance(skills_list, list):
        return []
    for skill in skills_list:
        if isinstance(skill, dict):
            # Try to find a 'skill' key or just take the first value
            if 'skill' in skill and isinstance(skill['skill'], str):
                normalized.append(skill['skill'])
            else:
                # Fallback: take the first string value in the dict
                for value in skill.values():
                    if isinstance(value, str):
                        normalized.append(value)
                        break # take only the first one
        elif isinstance(skill, str):
            normalized.append(skill)
    return normalized


def gap_analysis(resume_analysis, jd_analysis):
    """
    Identifies gaps between the resume and the job description.
    """
    resume_skills_raw = resume_analysis.get("skills", [])
    jd_skills_raw = jd_analysis.get("required_skills", [])

    resume_skills = set(_normalize_skills(resume_skills_raw))
    jd_skills = set(_normalize_skills(jd_skills_raw))
    
    missing_skills = list(jd_skills - resume_skills)
    
    return {"missing_skills": missing_skills}
