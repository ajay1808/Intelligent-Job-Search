from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Skills(BaseModel):
    name: str = Field(description="Name of the skill")
    proficiency: Optional[str] = Field(description="Proficiency level if available")

class ResumeAnalysis(BaseModel):
    strengths: List[str] = Field(description="List of candidate's strengths")
    areas_for_development: List[str] = Field(description="Areas where the candidate can improve")
    skills: List[Skills] = Field(description="List of skills with optional proficiency levels")
    experience: str = Field(description="Summary of relevant experience")

class JobRequirements(BaseModel):
    required_skills: List[str] = Field(description="List of required skills for the job")
    experience_level: str = Field(description="Required experience level")
    key_responsibilities: List[str] = Field(description="Key job responsibilities")

class ATSAnalysis(BaseModel):
    ats_score: str = Field(description="ATS match score as a percentage")
    keywords_match: List[str] = Field(description="List of matching keywords found")
    suggestions: Optional[List[str]] = Field(description="Suggestions for improvement")

class Job(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    url: str = Field(description="Job posting URL")
    posted_date: str = Field(description="Date the job was posted")
    description: str = Field(description="Full job description")
    match_score: Optional[float] = Field(description="Match score between 0 and 1")
    key_requirements: Optional[List[str]] = Field(description="Key requirements extracted from description")

class SearchQuery(BaseModel):
    queries: List[str] = Field(description="List of search queries")
    priority: List[float] = Field(description="Priority score for each query between 0 and 1")