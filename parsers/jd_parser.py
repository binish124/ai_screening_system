import re
import json
import os
from utils.logger import setup_logger

logger = setup_logger("JDParser")

# Synonym dictionaries for role variations and skill synonyms
ROLE_SYNONYMS = {
    "software engineer": ["sde", "software developer", "programmer", "coder"],
    "data scientist": ["ml engineer", "machine learning engineer", "data analyst"]
}

SKILL_SYNONYMS = {
    "Python": ["python3"],
    "Machine Learning": ["ml", "deep learning", "ai", "artificial intelligence"],
    "JavaScript": ["js", "ecmascript", "node", "react"],
    "AWS": ["amazon web services", "cloud"]
}

def normalize_text(text):
    """Normalizes JD text by converting to lowercase and removing excessive whitespace."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def detect_role(normalized_text):
    """Detects role names and maps variations to standard titles."""
    for standard_role, variations in ROLE_SYNONYMS.items():
        if standard_role in normalized_text:
            return standard_role.title()
        for variant in variations:
            if variant in normalized_text:
                return standard_role.title()
    return "Unknown Role"

def extract_skills(normalized_text):
    """Detects required skills and handles skill synonyms."""
    found_skills = []
    for standard_skill, synonyms in SKILL_SYNONYMS.items():
        # Check standard skill
        if standard_skill.lower() in normalized_text:
            found_skills.append({"name": standard_skill, "is_mandatory": True})
            continue
        # Check synonyms
        for synonym in synonyms:
            if synonym in normalized_text:
                found_skills.append({"name": standard_skill, "is_mandatory": True})
                break
    return found_skills

def extract_experience(normalized_text):
    """Extracts experience requirements using regex."""
    # Looks for patterns like '3+ years', '3-5 years', 'at least 4 years'
    match = re.search(r'(\d+)\s*(?:\+|-|to)?\s*(?:\d+)?\s*years?', normalized_text)
    if match:
        return {"minimum_years": int(match.group(1))}
    return {"minimum_years": 0}

def extract_education(normalized_text):
    """Extracts education preferences."""
    education_keywords = ["bachelor", "master", "phd", "degree", "b.s.", "b.a."]
    found_education = []
    for edu in education_keywords:
        if edu in normalized_text:
            found_education.append(edu.title())
    return list(set(found_education))

def parse_jd(raw_text):
    """Builds the job requirement object structure."""
    normalized = normalize_text(raw_text)
    
    jd_profile = {
        "role_details": {
            "designation": detect_role(normalized),
            "department": "Engineering" # Defaulted for template
        },
        "required_skills": extract_skills(normalized),
        "experience_requirements": extract_experience(normalized),
        "education_requirements": extract_education(normalized)
    }
    return jd_profile

def process_and_save_jd(raw_text, output_path):
    """Prepares AI-friendly JD profiles and saves structured output samples."""
    parsed_data = parse_jd(raw_text)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2)
    
    logger.info(f"Successfully saved structured JD output to {output_path}")
    return output_path

if __name__ == "__main__":
    # Test execution for output generation
    sample_jd_text = """
    We are looking for a talented ML Engineer to join our team. 
    You should have 4+ years of experience in data infrastructure. 
    Must be proficient in Python3 and AWS. 
    A Bachelor degree in Computer Science is required.
    """
    process_and_save_jd(sample_jd_text, "data/sample_jds/parsed_jd_output.json")
    print("✅ JD parsed and saved successfully.")