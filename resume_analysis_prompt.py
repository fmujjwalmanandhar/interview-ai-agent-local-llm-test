"""
Resume analysis prompt for ResumeAnalyzer.

This prompt is used to analyze resume data against job descriptions.
"""

import json
from typing import Any, Dict


def get_resume_analysis_prompt(
    job_description: str, resume_data: Dict[str, Any]
) -> str:
    """
    Generate the prompt for analyzing resume data against job description.

    Args:
        job_description (str): The job description to match against
        resume_data (Dict[str, Any]): The structured resume data

    Returns:
        str: The formatted prompt for resume analysis
    """
    return f"""You are a resume analyzer. Evaluate how well a candidate fits a job description.

INSTRUCTIONS:
- Return ONLY a valid raw JSON object
- No text, markdown, or explanation
- Use double quotes for all keys and string values
- Use null for missing values and "" for missing text
- The output must strictly follow this JSON schema:

{{
  "resume_match_score": float (0 to 10),
  "strengths": "string",
  "weaknesses": "string",
  "recommendation_ai": {{
    "status": "Selected" | "Rejected",
    "reason": "string or null"
  }},
  "profile_summary": "string"
}}

EVALUATION STEPS:
1. Extract required years of experience from the job description.
2. Compare candidate's total experience to job requirement.
3. Assess technical skill match (keyword overlap, partial matches).
4. Review project relevance and complexity.
5. Evaluate domain/industry alignment.
6. Consider education/certifications.
# 7. **If the job description contains a section or points titled 'Client Feedback', give these points EXTRA WEIGHT in the resume_match_score.**
#    - If the candidate matches or addresses any of the client feedback points, increase their score accordingly.
#    - Also, reflect these points in the strengths and weaknesses fields: if the candidate matches client feedback, mention it as a strength; if not, mention it as a weakness.
#    - **If the candidate's resume does NOT address ANY of the Client Feedback points, DEDUCT up to 1 points from the total score. Clearly mention missing client feedback points as weaknesses.**

SCORING RULE (total 10 points):
- Technical Skills Match: up to 4 pts
- Project Experience: up to 2 pts
- Experience Alignment: up to 2 pts
- Education & Certifications: up to 1 pt
- Domain Knowledge: up to 1 pt
- **If 'Client Feedback' exists:**
  - Allocate up to 2 bonus points for matching these feedback points (cannot exceed 10).
  - **If the candidate does NOT address any client feedback points, DEDUCT up to 1 points from the total score.**

RECOMMENDATION RULES:
- 9-10: Selected (excellent match)
- 7-8: Selected (good match)
- 6: Selected (acceptable, potential)
- 4-5: Rejected (skills or experience gap)
- 0-3: Rejected (poor match)

**When rejecting candidates (status: "Rejected"), if Client Feedback exists in the job description and the candidate does not address it, include this information in the recommendation_ai.reason field. For example: "Candidate lacks required experience in [specific skill] and does not address client feedback regarding [specific feedback point]."**

SPECIAL NOTES:
- 90%+ skill match can compensate for experience gap
- Strong certifications or portfolio may offset short experience
- For junior roles, be more flexible with requirements
- **Client Feedback should be prioritized if present.**

Job Description:
{job_description}

Candidate Profile:
{json.dumps(resume_data, separators=(',', ':'))}"""
