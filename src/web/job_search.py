import google.generativeai as genai
import json
from datetime import datetime
from perplexity import Perplexity

def search_for_jobs_with_perplexity(search_query, perplexity_api_key):
    """
    Searches for jobs using Perplexity AI and returns a structured JSON output.
    """
    client = Perplexity(api_key=perplexity_api_key)
    
    prompt = f"""
    Find the top 5 job postings for the query: "{search_query}".
    The jobs should have been posted within the last 7 days.
    Include the company name, job title, a direct URL to the job posting, the date it was posted, and a brief description.
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="sonar-pro",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "jobs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "company_name": {"type": "string"},
                                        "job_title": {"type": "string"},
                                        "job_url": {"type": "string"},
                                        "posted_date": {"type": "string", "format": "date"},
                                        "description": {"type": "string"}
                                    },
                                    "required": ["company_name", "job_title", "job_url", "posted_date", "description"]
                                }
                            }
                        },
                        "required": ["jobs"]
                    }
                }
            }
        )
        # Standardize the keys
        jobs = json.loads(completion.choices[0].message.content).get("jobs", [])
        standardized_jobs = []
        for job in jobs:
            standardized_jobs.append({
                "title": job.get("job_title"),
                "company": job.get("company_name"),
                "url": job.get("job_url"),
                "posted_date": job.get("posted_date"),
                "description": job.get("description")
            })
        return standardized_jobs
    except Exception as e:
        raise ValueError(f"Error during job search with Perplexity: {e}") from e

def filter_jobs_with_gemini(jobs, resume_text, jd_text, gemini_api_key):
    """
    Filters a list of jobs using Gemini to find the best matches.
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')

    prompt = f"""
    You are an expert career coach. Given the candidate's resume, their ideal job description, and a list of job postings,
    filter out any jobs that are not a good fit, are not recent, or seem like low-quality listings.
    Return only the jobs that are a strong match for the candidate.
    The output should be a JSON array of the filtered jobs, maintaining the original structure.

    Candidate's Resume:
    {resume_text}

    Ideal Job Description:
    {jd_text}

    Job Postings:
    {json.dumps(jobs, indent=2)}
    """
    try:
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_text)
    except Exception as e:
        raise ValueError(f"Error filtering jobs with Gemini: {e}") from e


def search_for_jobs(resume_analysis, jd_analysis, perplexity_api_key, gemini_api_key, resume_text, jd_text):
    """
    Searches for recent job postings using a two-step process:
    1. Generate search queries with Gemini.
    2. Search for jobs with Perplexity.
    3. Filter the results with Gemini.
    """
    # Step 1: Generate search queries with Gemini
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
    skills_list = resume_analysis.get("skills", [])
    if skills_list and isinstance(skills_list[0], dict):
        skills = ", ".join([s.get("name", "") for s in skills_list if s.get("name")])
    else:
        skills = ", ".join(skills_list)
    experience = resume_analysis.get("experience", "")
    prompt_queries = f"""
    Based on the following skills and experience, generate a list of 3 diverse job search queries.
    Format the output as a JSON array of strings.
    Skills: {skills}
    Experience: {experience}
    """
    try:
        response = model.generate_content(prompt_queries)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        search_queries = json.loads(cleaned_text)
    except Exception as e:
        raise ValueError(f"Error generating search queries with Gemini: {e}") from e

    # Step 2: Search for jobs with Perplexity
    all_perplexity_jobs = []
    for query in search_queries:
        try:
            all_perplexity_jobs.extend(search_for_jobs_with_perplexity(query, perplexity_api_key))
        except Exception as e:
            print(f"Could not fetch jobs for query '{query}': {e}")

    if not all_perplexity_jobs:
        return []

    # Step 3: Filter the results with Gemini
    return filter_jobs_with_gemini(all_perplexity_jobs, resume_text, jd_text, gemini_api_key)
