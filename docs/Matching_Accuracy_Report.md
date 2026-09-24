# Matching Accuracy Report

## 1. Tuning Similarity Thresholds
Because vector embeddings understand semantic closeness rather than exact text matches, a perfect `1.0` score is nearly impossible. Based on testing the `all-MiniLM-L6-v2` model, the system uses the following tuned similarity thresholds to classify applicants:
*   **High Match (Threshold > 0.75):** The candidate's background conceptually aligns with the core requirements. Proceed to interview phase.
*   **Moderate Match (Threshold 0.55 - 0.74):** The candidate possesses adjacent skills but lacks direct domain experience. Flag for manual recruiter review.
*   **Low Match (Threshold < 0.55):** The semantic distance is too vast; the candidate's background does not align with the role.

## 2. Validation Across Multiple Job Types
To ensure the model is not biased toward a specific industry, semantic validation tests must be conducted across diverse profiles:
*   **Data & Analytics Roles:** Testing semantic alignment between highly technical terms (e.g., matching "Pandas and Matplotlib" against a JD requiring "data visualization").
*   **Software Engineering Roles:** Evaluating architectural comparisons (e.g., matching "React and Next.js" against a JD requesting "frontend web development").
*   **Non-Technical / Operations Roles:** Ensuring the model accurately interprets management workflows (e.g., evaluating logistics experience against a municipal services JD).