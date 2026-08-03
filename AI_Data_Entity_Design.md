# AI Data Entity Design Document

## Overview
This document outlines the standard data entities required to parse unstructured hiring data into AI-ready formats.

## Standard Data Entities
1. **Candidate Profile**: Represented by `resume_schema.json`. Captures applicant basics, skills, chronological experience, and education.
2. **Job Profile**: Represented by `jd_schema.json`. Captures the designation, mandatory skills, and minimum experience required for a role.
3. **Skill Object**: Standardizes skills across both resumes and JDs to calculate matching scores.
4. **Experience Object**: Captures chronological work history, extracting the designation, company, and descriptive responsibilities for NLP analysis.

*Note: The explicit JSON structures for these entities are maintained in the root directory as `resume_schema.json` and `jd_schema.json`.*  