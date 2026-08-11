# Education & Certification Relevance Logic

## 1. Educational Normalization
Resumes contain vast inconsistencies in how degrees are written. The `education_engine.py` module uses a dictionary-based mapping to normalize variations (e.g., "B.S.", "BSc", "Bachelor's") into a standard `degree_type` (e.g., "Bachelor's"). This allows the downstream ATS scoring engine to simply check a boolean condition: `Does Candidate Degree == Target Job Degree Requirement?`

## 2. Certification Tagging
Certifications are evaluated based on keyword categorization rather than exact text matching. 
*   **Methodology:** The system scans the title of the certification against the `CERT_CATEGORIES` dictionary.
*   **Relevance Application:** If a candidate applies for a Data Analytics position, the ATS scoring engine will query the certification array specifically looking for items tagged with the `Data & Analytics` category. 

## 3. Relevancy Scoring Hierarchy
When evaluating a candidate's overall academic profile against a target job, the scoring engine applies the following weighting:
1.  **Field of Study (Highest Weight):** Does the major align with the role's industry?
2.  **Tagged Certifications (Medium Weight):** Does the candidate have up-to-date, tagged professional training in the exact tech stack required?
3.  **Degree Type (Baseline Weight):** Does the candidate meet the baseline degree requirement (e.g., Bachelor's vs. Master's)?