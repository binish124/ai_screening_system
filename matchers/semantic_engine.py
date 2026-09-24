import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the model to convert resumes and job descriptions into embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    """Converts a string of text into a high-dimensional vector embedding."""
    if not text.strip():
        return None
    return model.encode([text])

def calculate_similarity(text1, text2):
    """Measures semantic similarity using Cosine Similarity."""
    emb1 = generate_embedding(text1)
    emb2 = generate_embedding(text2)
    
    if emb1 is None or emb2 is None:
        return 0.0
        
    return float(cosine_similarity(emb1, emb2)[0][0])

def score_candidate(structured_resume, structured_jd):
    """
    Compares core sections of the profile to generate granular semantic scores.
    """
    # Compare: Skills
    resume_skills = " ".join(structured_resume.get("skills", []))
    jd_skills = " ".join(structured_jd.get("required_skills", []))
    skill_score = calculate_similarity(resume_skills, jd_skills)

    # Compare: Experience summaries
    resume_exp = " ".join([exp.get("summary", "") for exp in structured_resume.get("experience", [])])
    jd_exp = structured_jd.get("experience_requirements", "")
    exp_score = calculate_similarity(resume_exp, jd_exp)

    # Compare: Project descriptions
    resume_projects = " ".join([proj.get("description", "") for proj in structured_resume.get("projects", [])])
    jd_projects = structured_jd.get("project_requirements", "")
    project_score = calculate_similarity(resume_projects, jd_projects)

    # Calculate overall weighted similarity
    overall_match = (skill_score * 0.4) + (exp_score * 0.4) + (project_score * 0.2)

    return {
        "skills_match": round(skill_score, 3),
        "experience_match": round(exp_score, 3),
        "projects_match": round(project_score, 3),
        "overall_score": round(overall_match, 3)
    }

if __name__ == "__main__":
    # Test dataset
    sample_resume = {
        "skills": ["Python", "Machine Learning", "Data Pipelines", "NLP"],
        "experience": [{"summary": "Built predictive models and orchestrated automated data pipelines."}],
        "projects": [{"description": "Developed a local RAG chatbot using large language models and vector databases."}]
    }
    
    sample_jd = {
        "required_skills": ["Python", "Data Science", "Scikit-Learn", "Deep Learning"],
        "experience_requirements": "Seeking a candidate with experience building predictive machine learning models and deploying data architectures.",
        "project_requirements": "Familiarity with retrieval-augmented generation or NLP systems is highly preferred."
    }
    
    results = score_candidate(sample_resume, sample_jd)
    print("Semantic Matching Output:")
    print(json.dumps(results, indent=2))