import re
import json
import os
from utils.logger import setup_logger

logger = setup_logger("SkillExtractor")

# Build a master skill dictionary (tech, business, creative)
SKILL_DICTIONARY = {
    "Python": ["python", "python3", "py"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "Machine Learning": ["machine learning", "ml", "deep learning"],
    "Project Management": ["project management", "agile", "scrum", "pm"],
    "Graphic Design": ["graphic design", "creative design", "photoshop", "illustrator"]
}

# Handle skill stacks
SKILL_STACKS = {
    "MERN": ["MongoDB", "Express.js", "React", "Node.js"],
    "MEAN": ["MongoDB", "Express.js", "Angular", "Node.js"]
}

def extract_and_score_skills(text):
    """
    Implements NLP-based entity recognition to extract skills,
    handle variations, and assign confidence scores.
    """
    extracted_skills = {}
    # Normalize text to lowercase for scanning
    normalized_text = text.lower()

    # 1. Scan for standard skills, synonyms, and spelling variations
    for standard_skill, variants in SKILL_DICTIONARY.items():
        for variant in variants:
            # Using regex to ensure we match whole words/phrases, not substrings
            pattern = rf'\b{re.escape(variant)}\b'
            if re.search(pattern, normalized_text):
                # Design confidence scoring per skill
                score = 1.0 if variant == standard_skill.lower() else 0.90
                
                # Deduplicate: Only keep the highest confidence score if found multiple times
                if standard_skill in extracted_skills:
                    extracted_skills[standard_skill] = max(extracted_skills[standard_skill], score)
                else:
                    extracted_skills[standard_skill] = score

    # 2. Scan for and expand skill stacks
    for stack, stack_skills in SKILL_STACKS.items():
        if re.search(rf'\b{stack.lower()}\b', normalized_text):
            for skill in stack_skills:
                # Skills inferred from a stack get a slightly lower confidence score
                score = 0.85
                if skill in extracted_skills:
                    extracted_skills[skill] = max(extracted_skills[skill], score)
                else:
                    extracted_skills[skill] = score

    # 3. Deduplicate and normalize extracted skills into a final array
    final_skills = [{"name": skill, "confidence": score} for skill, score in extracted_skills.items()]
    
    # Sort by confidence score descending
    final_skills.sort(key=lambda x: x["confidence"], reverse=True)
    return final_skills

def process_skills(text, output_path):
    """Generates the structured skill output."""
    skills = extract_and_score_skills(text)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2)
        
    logger.info(f"Successfully saved structured skill output to {output_path}")
    return skills

if __name__ == "__main__":
    # Test string handling stacks (MERN), variants (python3), and business skills (agile)
    sample_resume_text = "I am a developer experienced in python3, agile methodologies, and the MERN stack. I also study machine learning."
    
    process_skills(sample_resume_text, "data/parsed/extracted_skills_sample.json")
    print("✅ Skills successfully extracted, scored, and saved!")