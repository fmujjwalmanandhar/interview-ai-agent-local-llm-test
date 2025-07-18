"""
Resume extraction prompt for ResumeAnalyzer.

This prompt is used to extract structured data from resume text.
"""


def get_resume_extraction_prompt(resume_text: str) -> str:
   return f"""IMPORTANT: Respond with only a valid JSON object, with no explanation, no code fences, and no extra text. Output only the JSON object.


IMPORTANT RULES:
1. Return ONLY a valid JSON object with no additional text
2. All property names must be in double quotes
3. Use null for missing values
4. Use empty arrays [] for missing lists
5. Use empty strings "" for missing text
6. Ensure the JSON is properly formatted with no trailing commas

Required JSON structure:
{{
    "name": "string",
    "years_of_experience": "number",
    "skills": {{
        "programming_languages": [],
        "frameworks_libraries": [],
        "databases": [],
        "cloud_platforms": [],
        "devops_tools": [],
        "other_tools": [],
        "soft_skills": []
    }},
    "education": [
        {{
            "degree": "string",
            "institution": "string",
            "years": "string"
        }}
    ],
    "work_experience": [
        {{
            "title": "string",
            "company": "string",
            "location": "string",
            "start_date": "string",
            "end_date": "string",
            "description": "string",
            "technologies_used": []
        }}
    ],
    "projects": [
        {{
            "name": "string",
            "description": "string",
            "technologies_used": [],
            "project_url": "string"
        }}
    ],
    "certifications": [],
    "github_profile": "string",
    "linkedin_profile": "string",
    "email": "string",
    "phone": "string"
}}

Resume text:
{resume_text}

REMEMBER: Output ONLY the JSON object, with no explanation or extra text.
"""
