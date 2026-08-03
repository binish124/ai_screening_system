import os
import re
import pdfplumber
import docx
from utils.logger import setup_logger

logger = setup_logger("ResumeParser")

def extract_from_pdf(file_path):
    """Extracts text from a PDF, handling columns and tables."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF {file_path}: {e}")
        return ""

def extract_from_docx(file_path):
    """Extracts text from a Word document."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Failed to read DOCX {file_path}: {e}")
        return ""

def clean_text(raw_text):
    """Cleans noise, unwanted symbols, and normalizes formatting."""
    # Remove weird invisible control characters and non-printable noise
    text = re.sub(r'[^\x20-\x7E\n\t]+', ' ', raw_text)
    
    # Normalize bullet points to a standard dash
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\*]', '-', text)
    
    # Normalize excessive newlines and spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Normalize section headings (capitalization)
    headings = ["experience", "education", "skills", "certifications", "projects"]
    for heading in headings:
        # Finds variations of headings and forces them to uppercase for easy AI mapping
        pattern = re.compile(rf'^{heading}\b', re.IGNORECASE | re.MULTILINE)
        text = pattern.sub(heading.upper(), text)
        
    return text.strip()

def process_resume(file_path, output_dir="data/cleaned_resumes"):
    """Main pipeline to extract, clean, and store the text."""
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Processing file: {file_path}")
    
    if file_path.lower().endswith('.pdf'):
        raw_text = extract_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        raw_text = extract_from_docx(file_path)
    else:
        logger.warning(f"Unsupported file format: {file_path}")
        return None

    cleaned_text = clean_text(raw_text)
    
    # Store extracted text in structured files
    base_name = os.path.basename(file_path).split('.')[0]
    output_path = os.path.join(output_dir, f"{base_name}_cleaned.txt")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
        
    logger.info(f"Successfully saved cleaned text to {output_path}")
    return output_path