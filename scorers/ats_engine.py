import json

# Configurable weight system based on the target role type
ROLE_WEIGHTS = {
    "Software Engineering": {
        "skills": 0.40,
        "experience": 0.30,
        "semantic_similarity": 0.20,
        "education": 0.10
    },
    "Data & Analytics": {
        "skills": 0.35,
        "experience": 0.30,
        "semantic_similarity": 0.20,
        "education": 0.15
    },
    "Default": {
        "skills": 0.25,
        "experience": 0.25,
        "semantic_similarity": 0.25,
        "education": 0.25
    }
}

def handle_missing_data(score_dict, field):
    """Handles missing data by returning 0.0 and a flag for the explainability report."""
    if field not in score_dict or score_dict.get(field) is None:
        return 0.0, True
    return float(score_dict.get(field)), False

def generate_candidate_score(candidate_data, role_type="Default"):
    """
    Candidate score generator that calculates the final weighted score 
    and builds an explainable scoring output.
    """
    weights = ROLE_WEIGHTS.get(role_type, ROLE_WEIGHTS["Default"])
    
    # Extract sub-scores and handle missing data
    skill_score, skill_missing = handle_missing_data(candidate_data, "skills_score")
    exp_score, exp_missing = handle_missing_data(candidate_data, "experience_score")
    edu_score, edu_missing = handle_missing_data(candidate_data, "education_score")
    sem_score, sem_missing = handle_missing_data(candidate_data, "semantic_score")

    # Apply dynamic weight system per role
    weighted_skill = skill_score * weights["skills"]
    weighted_exp = exp_score * weights["experience"]
    weighted_edu = edu_score * weights["education"]
    weighted_sem = sem_score * weights["semantic_similarity"]

    final_score = round(weighted_skill + weighted_exp + weighted_edu + weighted_sem, 3)

    # Build explainable scoring output
    explanation = []
    explanation.append(f"Base Configuration: Applied weights for '{role_type}'.")
    
    if skill_missing:
        explanation.append("Warning: Skill data missing. Scored as 0.")
    else:
        explanation.append(f"Skills: Earned {round(weighted_skill*100, 1)}% out of a possible {weights['skills']*100}%.")
        
    if exp_missing:
        explanation.append("Warning: Experience data missing. Scored as 0.")
    else:
        explanation.append(f"Experience: Earned {round(weighted_exp*100, 1)}% out of a possible {weights['experience']*100}%.")
        
    if edu_missing:
        explanation.append("Warning: Education data missing. Scored as 0.")
    else:
        explanation.append(f"Education: Earned {round(weighted_edu*100, 1)}% out of a possible {weights['education']*100}%.")

    if sem_missing:
        explanation.append("Warning: Semantic semantic data missing. Scored as 0.")
    else:
        explanation.append(f"Semantic Match: Earned {round(weighted_sem*100, 1)}% out of a possible {weights['semantic_similarity']*100}%.")

    return {
        "final_match_percentage": round(final_score * 100, 1),
        "role_configuration_used": role_type,
        "score_breakdown": {
            "skills_contribution": round(weighted_skill, 3),
            "experience_contribution": round(weighted_exp, 3),
            "education_contribution": round(weighted_edu, 3),
            "semantic_contribution": round(weighted_sem, 3)
        },
        "explainability_report": explanation
    }

if __name__ == "__main__":
    # Mock data aggregated from Day 9, Day 10, Day 11, and Day 12 outputs
    sample_candidate_scores = {
        "skills_score": 0.85,
        "experience_score": 0.90,
        "education_score": 1.0,  
        # Purposely omitting "semantic_score" to test missing data handling
    }
    
    # Test the candidate score generator
    report = generate_candidate_score(sample_candidate_scores, role_type="Data & Analytics")
    print(json.dumps(report, indent=2))