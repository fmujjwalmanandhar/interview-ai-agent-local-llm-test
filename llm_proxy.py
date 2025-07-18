# llm_proxy.py
"""
Gemini-to-LM Studio proxy server.

- Forwards Gemini API requests to a local LM Studio LLM (OpenAI-compatible API).
- Set your model name via the LM_STUDIO_MODEL environment variable, or edit below.
- Run with: python llm_proxy.py
- Requires: fastapi, uvicorn, requests
"""
from fastapi import FastAPI, Request, HTTPException
import requests
import uvicorn
import os
import time

app = FastAPI()

# Ollama endpoint (adjust if needed)
MODEL_API_ENDPOINT="http://localhost:11434/api/generate"
MODEL_NAME = os.environ.get("MODEL_NAME", "gemma:2b")  # Set your model name here or via env var

@app.post("/v1beta/models/{model_name}:generateContent")
async def gemini_proxy(model_name: str, request: Request):
    data = await request.json()
    # Extract prompt from Gemini-style request
    # start_time_resume_extraction = time.time()
        
    prompt = data.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
    # Map Gemini params to OpenAI/LM Studio params
    lm_payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    try:
        resp = requests.post(MODEL_API_ENDPOINT, json=lm_payload, timeout=60)
        resp.raise_for_status()
        resp_json = resp.json()
        text = resp_json["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio: {e}")
    # Return in Gemini-like format

    # end_time_resume_extraction = time.time()
    # time_taken_to_extract_resume = end_time_resume_extraction - start_time_resume_extraction
    # print(f"time taken time_taken_to_extract_resume: {time_taken_to_extract_resume}")

    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": text}]
                }
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)