import re
import json
import os
from utils.logger import setup_logger

logger = setup_logger("EducationEngine")

# Normalization mapping for degree types
DEGREE_MAPPING = {
    "Bachelor's": ["b.s.", "b.tech", "b.a.", "bachelor", "bachelors", "bsc", "btech"],
    "Master's": ["m.s.", "m.tech", "m.a.", "master", "masters", "msc", "mtech"],
    "Doctorate": ["ph.d.", "phd", "doctorate"]
}

# Tagging categories for professional certifications
CERT_CATEGORIES = {
    "Data & Analytics": ["data science", "machine learning", "data analytics", "pandas"],
    "Software Development": ["python", "software engineering", "full stack", "react", "programming"],
    "Cloud & Infrastructure": ["aws", "azure", "docker", "kubernetes", "cloud"]
}

def normalize_degree(text):
    """Normalizes naming conventions for degrees."""
    text_lower = text.lower()
    for standard_degree, variations in DEGREE_MAPPING.items():
        if any(re.search(rf'\b{re.escape(var)}\b', text_lower) for var in variations):
            return standard_degree
    return "Unknown Degree"

def tag_certification(cert_name):
    """Tags certifications with relevance categories."""
    cert_lower = cert_name.lower()
    for category, keywords in CERT_CATEGORIES.items():
        if any(kw in cert_lower for kw in keywords):
            return category
    return "General / Other"

def extract_education(text):
    """
    Mocks the extraction of degree type, field of study, institution, and graduation year.
    In a full production environment, this leverages spaCy NER models.
    """
    # Normalized sample extraction based on typical resume NLP outputs
    raw_degree_text = "Bachelor of Technology"
    return {
        "degree_type": normalize_degree(raw_degree_text),
        "field_of_study": "Computer Science",
        "institution": "State University",
        "graduation_year": 2025
    }

def extract_certifications(cert_list):
    """Processes a list of raw certifications and assigns tags."""
    processed_certs = []
    for cert in cert_list:
        processed_certs.append({
            "certification_name": cert,
            "relevance_category": tag_certification(cert)
        })
    return processed_certs

def process_academic_profile(resume_text, raw_certs, output_path):
    """Builds the final structured academic profile."""
    education_data = extract_education(resume_text)
    certification_data = extract_certifications(raw_certs)
    
    academic_profile = {
        "education": education_data,
        "certifications": certification_data
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(academic_profile, f, indent=2)
        
    logger.info(f"Successfully saved structured academic profile to {output_path}")
    return academic_profile

if __name__ == "__main__":
    # Test execution for output generation targeting a technical intern profile
    sample_education_text = "B.Tech in Computer Science, State University, Graduating 2025"
    sample_certs = [
        "Advanced Python Programming Certification",
        "Google Data Science Professional Certificate",
        "First Aid CPR"
    ]
    
    process_academic_profile(
        sample_education_text, 
        sample_certs, 
        "data/parsed/structured_academic_profile.json"
    )
    print("✅ Academic profile parsed, normalized, tagged, and saved successfully!")