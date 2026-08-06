# Section Detection Accuracy Report

## 1. Methodology
The parsing engine leverages a hybrid **rule-based + NLP-based section detection** approach to parse unstructured resumes. 

## 2. Capability Breakdown
*   **Target Sections:** The engine successfully identifies and maps data to: Skills, Work Experience, Education, Certifications, and Projects.
*   **Handling Variations:** 
    *   *Tables & Columns:* Complex visual layouts (tables, columns) are handled upstream by the Day 5 `resume_parser.py` (via `pdfplumber`), which feeds normalized, linear text into this segmenter.
    *   *Missing Headings:* Unlabeled introductory text (like names, emails, and objective statements) is safely captured in a default "Basics" block before the first recognized header appears.
*   **Tagging Mechanism:** Each line is evaluated using continuous state-tracking. Once a recognized header triggers a state change, all subsequent text blocks are tagged to the new section until the next valid heading is detected.