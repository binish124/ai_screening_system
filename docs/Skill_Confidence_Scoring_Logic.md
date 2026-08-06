# Skill Confidence Scoring Logic

## Overview
To extract technical and non-technical skills accurately[cite: 5], the `skill_extractor.py` engine doesn't just extract skills; it assigns a mathematical confidence score (from 0.0 to 1.0) to represent how explicitly the candidate demonstrated that skill in their resume.

## Scoring Tiers

The engine uses a tiered rule-based approach to assign confidence scores based on NLP-based entity recognition[cite: 5]:

### 1. Tier 1: Exact Explicit Match (Confidence: 1.0)
*   **Logic:** The candidate's text exactly matches the primary standard name of the skill in the master dictionary.
*   **Example:** The dictionary looks for "Python" and the resume specifically says "Python".
*   **Meaning:** 100% confidence the skill is present as standardly defined.

### 2. Tier 2: Synonym or Variant Match (Confidence: 0.90)
*   **Logic:** The candidate used an abbreviation, alternative spelling, or industry synonym[cite: 5].
*   **Example:** The dictionary looks for "JavaScript", but the candidate wrote "JS" or "ECMAScript".
*   **Meaning:** 90% confidence. We are highly certain they possess the core skill, but applied a slight penalty because it was extracted via alias mapping rather than explicit standard phrasing.

### 3. Tier 3: Inferred from Skill Stacks (Confidence: 0.85)
*   **Logic:** The candidate mentioned a tech stack[cite: 5] (e.g., "MERN"), and the engine automatically inferred the constituent technologies (MongoDB, Express.js, React, Node.js).
*   **Meaning:** 85% confidence. While they know the stack, they didn't explicitly list the individual technology. This slightly lower score helps the AI distinguish between someone who explicitly wrote "React" versus someone who simply wrote "MERN".

## Deduplication and Normalization
Because resumes often repeat skills across different jobs, the engine will inevitably extract the same skill multiple times. 

To deduplicate and normalize extracted skills[cite: 5], the system uses a **"Max Score Override"** rule. If a skill is found multiple times with different confidence scores, the engine drops the duplicates and retains only the *highest* confidence score recorded for that specific skill.