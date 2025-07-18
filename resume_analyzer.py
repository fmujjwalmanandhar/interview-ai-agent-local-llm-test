import json
import os
import requests
import re
import time
from typing import Any, Dict


from get_resume_extraction_prompt import get_resume_extraction_prompt
from resume_analysis_prompt import get_resume_analysis_prompt

class ResumeAnalyzer:
    def __init__(self, endpoint=None, model="gemma:2b"):
        self.endpoint = endpoint or os.getenv("MODEL_API_ENDPOINT", "http://localhost:11434/api/generate")
        self.model = model

    @staticmethod
    def auto_close_json(json_str):
        # Balance curly braces
        open_curly = json_str.count('{')
        close_curly = json_str.count('}')
        if open_curly > close_curly:
            json_str += '}' * (open_curly - close_curly)
        # Balance square brackets
        open_square = json_str.count('[')
        close_square = json_str.count(']')
        if open_square > close_square:
            json_str += ']' * (open_square - close_square)
        return json_str

    def _call_llm_and_extract_json(self, prompt: str, model: str = None) -> str:
        model = model or self.model
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        print(f"Using model {model} \n")
        try:
            resp = requests.post(self.endpoint, json=payload, timeout=120)
            try:
                resp_json = resp.json()
            except Exception as e:
                error = {
                    "error": f"ResponseNotJSON: {str(e)}",
                    "raw_response": resp.text
                }
                return error

            response_text = resp_json.get("response")
            if not response_text or not isinstance(response_text, str):
                error = {
                    "error": "KeyError: 'response' missing or not a string in Ollama response",
                    "raw_response": resp_json
                }
                return error
            # print(f"response_text: {response_text}")
            response_text = response_text.strip()
            # print(f"response_text strip: {response_text}")
            # Try direct parse
            try:
                result = json.loads(response_text)
                return json.dumps(result, separators=(',', ':'))
            except Exception:
                # Fallback: remove code fences and try regex extraction
                if response_text.startswith("```"):
                    response_text = response_text.strip("`")
                    response_text = response_text.replace("json", "", 1).strip()
                matches = re.findall(r'(\{.*?\}|\[.*?\])', response_text, re.DOTALL)
                if matches:
                    json_str = max(matches, key=len)
                    # Remove trailing commas before } or ]
                    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
                    # Add a comma between ] or } and " if missing (between properties)
                    json_str = re.sub(r'([}\]])\s*[\r\n]+\s*"', r'\1,\n"', json_str)
                    # Auto-close braces/brackets
                    json_str = self.auto_close_json(json_str)
                    try:
                        result = json.loads(json_str)
                        return json.dumps(result, separators=(',', ':'))
                    except Exception as e:
                        error = {
                            "error": f"JSONDecodeError: {str(e)}",
                            "raw_response": response_text,
                            "json_attempt": json_str
                        }
                        return error
                else:
                    error = {
                        "error": "No JSON object found in response",
                        "raw_response": response_text
                    }
                    return error
        except Exception as e:
            error = {
                "error": f"{type(e).__name__}: {str(e)}",
            }
            return error

    def analyze_resume(self, resume_text, job_description, model: str = None):
        start_time_resume_extraction = time.time()
        print(f"Trying to extract data from resume....\n")
        resume_data = self.extract_resume_data(resume_text, model=model)
        end_time_resume_extraction = time.time()
        time_taken_to_extract_resume = end_time_resume_extraction - start_time_resume_extraction
        print(f"Time taken to extract resume: {time_taken_to_extract_resume:.2f} seconds\n")
        # print(f"after resume extraction data: {resume_data}\n\n")

        start_time_resume_analysis = time.time()
        prompt = get_resume_analysis_prompt(job_description, resume_data)
        result = self._call_llm_and_extract_json(prompt, model=model)
        end_time_resume_analysis = time.time()
        time_taken_to_analyze_resume = end_time_resume_analysis - start_time_resume_analysis
        print(f"Time taken to analyze resume: {time_taken_to_analyze_resume:.2f} seconds\n")
        msg = {
        "result": result
        }

        parsed_result = json.loads(msg["result"])

        print(json.dumps(parsed_result, indent=2))
        return result

    def extract_resume_data(self, resume_text: str, model: str = None) -> Dict[str, Any]:
        if not resume_text or not isinstance(resume_text, str):
            error = {"error": "Invalid resume text provided"}
            # print(error)
            return error
        prompt = get_resume_extraction_prompt(resume_text)
        return self._call_llm_and_extract_json(prompt, model=model)
    
   