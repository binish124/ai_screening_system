import re
import json
import os
from utils.logger import setup_logger

logger = setup_logger("SectionSegmenter")

# Rule-based detection dictionaries handling various heading styles
SECTION_MAPPING = {
    "Experience": r'^(WORK\s*EXPERIENCE|EXPERIENCE|EMPLOYMENT|HISTORY)\b',
    "Education": r'^(EDUCATION|ACADEMICS|QUALIFICATIONS)\b',
    "Skills": r'^(SKILLS|TECHNICAL\s*SKILLS|CORE\s*COMPETENCIES)\b',
    "Certifications": r'^(CERTIFICATIONS|LICENSES|COURSES)\b',
    "Projects": r'^(PROJECTS|PERSONAL\s*PROJECTS|ACADEMIC\s*PROJECTS)\b'
}

def segment_resume(text):
    """Tags extracted text blocks to their correct sections using rule-based logic."""
    lines = text.split('\n')
    
    # Initialize the structured sections
    segments = {
        "Basics": [], # Captures header data before the first official section
        "Experience": [],
        "Education": [],
        "Skills": [],
        "Certifications": [],
        "Projects": []
    }
    
    current_section = "Basics" 
    
    for line in lines:
        line_cleaned = line.strip().upper()
        section_found = False
        
        # NLP-based scan for standard headings
        for section, pattern in SECTION_MAPPING.items():
            if re.search(pattern, line_cleaned):
                current_section = section
                section_found = True
                break
                
        # If the line isn't a heading, append it to the active tagged section
        if not section_found and line.strip():
            segments[current_section].append(line.strip())
            
    # Join the arrays back into continuous text blocks
    for key in segments:
        segments[key] = "\n".join(segments[key])
        
    return segments

def process_and_save_segmentation(input_text, output_path):
    """Generates labeled resume samples by running the text through the segmenter."""
    labeled_data = segment_resume(input_text)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, indent=2)
        
    logger.info(f"Saved labeled resume sections to {output_path}")
    return labeled_data

if __name__ == "__main__":
    # Built-in test to handle variations and missing headings
    sample_resume = """Alex Developer
    alex@email.com
    
    SKILLS
    - Python, AWS, JSON parsing
    
    WORK EXPERIENCE
    Software Engineer at Tech Corp
    - Handled tables and column layout extraction
    
    EDUCATION
    B.S. Computer Science
    
    PROJECTS
    AI Screening System Architecture
    """
    
    process_and_save_segmentation(sample_resume, "data/cleaned_resumes/labeled_sample.json")
    print("✅ Resume successfully segmented and labeled!")