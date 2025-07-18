import os
import fitz

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