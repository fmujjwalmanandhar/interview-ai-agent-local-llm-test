import os
import json
import fitz
from resume_analyzer import ResumeAnalyzer
from dotenv import load_dotenv
load_dotenv()

# Utility to extract text from a local PDF file
def extract_text_from_pdf(pdf_path, max_pages=50):
    if not os.path.exists(pdf_path):
        print(f"Warning: PDF file not found: {pdf_path}")
        return ""
    doc = fitz.open(pdf_path)
    text_parts = []
    pages_to_process = min(doc.page_count, max_pages)
    for page_num in range(pages_to_process):
        try:
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text)
        except Exception:
            continue
    doc.close()
    return "\n".join(text_parts)

if __name__ == "__main__":
    # Use the llm_local_test directory for PDFs
    project_root = os.path.abspath(os.path.dirname(__file__))
    resume_pdf_path = os.path.join(project_root, "sample_resume.pdf")
    jobdesc_pdf_path = os.path.join(project_root, "sample_job_description.pdf")
    print(f"Extracting text from Resume PDF ...\n")
    resume_text = extract_text_from_pdf(resume_pdf_path)
    print(f"Extracting text from Description PDF ...\n")
    job_description = extract_text_from_pdf(jobdesc_pdf_path)
    analyzer = ResumeAnalyzer()
    result = analyzer.analyze_resume(resume_text, job_description)
    print(json.dumps({"result": result}, indent=2))