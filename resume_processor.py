import os
import fitz
from resume_analyzer import ResumeAnalyzer
from extract_text_from_pdf import extract_text_from_pdf

class ResumeProcessor:
    def __init__(self, analyzer=None):
        self.analyzer = analyzer or ResumeAnalyzer()
    def process_single_resume(self, resume_text, job_description):
        result = self.analyzer.analyze_resume(resume_text, job_description)
        return result

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.dirname(__file__))
    resume_pdf_path = os.path.join(project_root, "sample_resume.pdf")
    jobdesc_pdf_path = os.path.join(project_root, "sample_job_description.pdf")
    resume_text = extract_text_from_pdf(resume_pdf_path)
    job_description = extract_text_from_pdf(jobdesc_pdf_path)
    if resume_text and job_description:
        processor = ResumeProcessor()
        result = processor.process_single_resume(resume_text, job_description)
        print(result)
    else:
        print("Please provide sample_resume.pdf and sample_job_description.pdf in llm_local_test directory.") 