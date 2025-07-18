# Resume Analyzer LLM App

## Overview

This project provides an AI-powered resume analysis tool using large language models (LLMs) served via [Ollama](https://ollama.com/). The core logic is in the `ResumeAnalyzer` class, which extracts structured data from resumes and analyzes them against job descriptions using LLMs.

## Features

- Extracts structured information from raw resume text using an LLM
- Analyzes resumes for strengths, weaknesses, and fit for a job description
- Robust handling of LLM output quirks (malformed JSON, code fences, etc.)
- Easily swap between different LLMs (e.g., llama3, gemma, deepseek, etc.)

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running
- Required Python packages (see `requirements.txt`)

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Install and start Ollama:**

   - [Download and install Ollama](https://ollama.com/download)
   - Start Ollama (it runs as a background service)

3. **List available models:**

   ```bash
   ollama list
   ```

   This will show models you have pulled (e.g., `llama3:latest`, `gemma:2b`, etc.)

4. **Pull a model if needed:**
   ```bash
   ollama pull llama3:latest
   # or
   ollama pull gemma:2b
   ```

## Running the App

### 1. Start the LLM Proxy (if used)

This file acts as a proxy server to the LLM API (optional, depending on your setup):

```bash
python llm_proxy.py
```

### 2. Run the Test Script

This will run the resume analysis pipeline:

```bash
python test_with_proxy.py
```

## Swapping Models

You can change the LLM model used by the app in two ways:

### **A. In Code**

Edit the model name in the `ResumeAnalyzer` constructor:

```python
analyzer = ResumeAnalyzer(model="llama3:latest")
# or
analyzer = ResumeAnalyzer(model="gemma:2b")
```

### **B. Using Environment Variable**

Set the `MODEL_API_ENDPOINT` environment variable to point to your Ollama endpoint (default is `http://localhost:11434/api/generate`).

To change the model, pass the model name as a parameter when calling methods, or set it in the constructor.

## What Does the ResumeAnalyzer Class Do?

- **Initialization:** Sets up the API endpoint and model name.
- **extract_resume_data:**
  - Takes raw resume text, builds a prompt, sends it to the LLM, and extracts structured data (as JSON).
  - Handles malformed LLM output and tries to recover valid JSON.
- **analyze_resume:**
  - Takes resume text and a job description, extracts structured data, then analyzes the resume for fit, strengths, weaknesses, and summary using the LLM.
  - Prints and returns the analysis in a compact JSON format.
- **Model Swapping:** You can use any model available in Ollama by changing the model name in the constructor or method call.

## Example Usage

```python
from resume_analyzer import ResumeAnalyzer
analyzer = ResumeAnalyzer(model="llama3:latest")
resume_text = open('sample_resume.txt').read()
job_description = open('sample_job_description.txt').read()
result = analyzer.analyze_resume(resume_text, job_description)
print(result)
```

## Troubleshooting

- If you get timeout or connection errors, make sure Ollama is running and the model is pulled.
- If the LLM output is not valid JSON, the app will attempt to auto-correct and parse it.

## License

MIT

## Contact / Contributions

Feel free to open issues or pull requests!
