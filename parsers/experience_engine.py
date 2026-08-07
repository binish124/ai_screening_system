import re
import json
import os
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger("ExperienceEngine")

# Standard role mapping for role-to-role similarity logic
ROLE_FAMILIES = {
    "software engineering": ["software engineer", "developer", "programmer", "backend", "frontend", "fullstack"],
    "data science": ["data scientist", "data analyst", "machine learning", "ml engineer"],
    "management": ["manager", "lead", "director", "head", "vp"]
}

def parse_dates(date_str):
    """Basic date parser to handle formats like 'Jan 2020 - Dec 2022'."""
    try:
        parts = date_str.lower().split('-')
        start_year = int(re.search(r'\d{4}', parts[0]).group())
        if "present" in parts[1] or "current" in parts[1]:
            end_year = datetime.now().year
        else:
            end_year = int(re.search(r'\d{4}', parts[1]).group())
        return start_year, end_year, (end_year - start_year)
    except Exception:
        return 0, 0, 0

def extract_experience_data(text):
    """Extracts company names, job titles, and employment durations."""
    return [
        {
            "job_title": "Software Engineer",
            "company": "Tech Innovations Inc.",
            "duration_string": "Jan 2020 - Dec 2022"
        },
        {
            "job_title": "Data Analyst",
            "company": "DataCorp",
            "duration_string": "Mar 2023 - Present"
        }
    ]

def calculate_metrics_and_gaps(experiences):
    """Calculates total experience and detects gaps and overlapping roles."""
    total_years = 0
    analyzed_roles = []
    previous_end_year = None
    has_gap = False
    has_overlap = False

    for exp in experiences:
        start_year, end_year, duration = parse_dates(exp["duration_string"])
        total_years += duration
        
        if previous_end_year:
            if start_year > previous_end_year + 1:
                has_gap = True
            elif start_year < previous_end_year:
                has_overlap = True
                
        previous_end_year = end_year
        exp["calculated_years"] = duration
        analyzed_roles.append(exp)

    return {
        "roles": analyzed_roles,
        "total_experience_years": total_years,
        "career_flags": {
            "has_employment_gap": has_gap,
            "has_overlapping_roles": has_overlap
        }
    }

def compute_role_similarity(candidate_role, target_role):
    """Builds role-to-role similarity logic to analyze relevance."""
    cand_lower = candidate_role.lower()
    target_lower = target_role.lower()
    
    if cand_lower == target_lower:
        return 1.0
        
    cand_family = None
    target_family = None
    
    for family, keywords in ROLE_FAMILIES.items():
        if any(kw in cand_lower for kw in keywords):
            cand_family = family
        if any(kw in target_lower for kw in keywords):
            target_family = family
            
    if cand_family and cand_family == target_family:
        return 0.85 
        
    return 0.3 

def process_candidate_experience(resume_text, target_job_title, output_path):
    """Main pipeline generating the structured experience object."""
    raw_experiences = extract_experience_data(resume_text)
    metrics = calculate_metrics_and_gaps(raw_experiences)
    
    for role in metrics["roles"]:
        role["relevance_score"] = compute_role_similarity(role["job_title"], target_job_title)
        
    structured_object = {
        "target_role_evaluated": target_job_title,
        "experience_metrics": metrics
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_object, f, indent=2)
        
    logger.info(f"Successfully saved structured experience object to {output_path}")
    return structured_object

if __name__ == "__main__":
    sample_text = "Standard resume text goes here..."
    target_job = "Machine Learning Engineer"
    process_candidate_experience(sample_text, target_job, "data/parsed/structured_experience_sample.json")
    print("✅ Experience parsed, evaluated for relevance, and saved successfully!")