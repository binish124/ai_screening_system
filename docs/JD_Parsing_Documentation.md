# Job Description (JD) Parsing Documentation

## 1. Overview
The JD Parsing System (`parsers/jd_parser.py`) is designed to convert raw, unstructured employer job descriptions into structured, AI-readable JSON objects that match the schema defined in Day 4.

## 2. Text Normalization
Before extraction, the parser standardizes the text by:
* Converting all characters to lowercase to prevent case-sensitivity mismatches.
* Stripping excessive whitespace and replacing multi-line breaks with single spaces to create a continuous string for accurate Regular Expression scanning.

## 3. Extraction Methodologies
The parser isolates four key data points from the normalized text:

* **Role Names:** Utilizes a dictionary mapping (`ROLE_SYNONYMS`) to detect variations (e.g., "SDE", "Programmer") and standardizes them into a primary title (e.g., "Software Engineer").
* **Required Skills:** Implements a two-pass scan against a `SKILL_SYNONYMS` dictionary. It checks for the standard skill name, and if absent, scans for known industry acronyms or alternative names (e.g., mapping "js" to "JavaScript").
* **Experience Requirements:** Utilizes Python's `re` module to locate numerical values directly preceding the word "year" or "years", handling formatting variations like "3+ years" or "3-5 years".
* **Education Preferences:** Scans the document for standard degree keywords (Bachelor, Master, PhD) and appends them to a required education array.

## 4. Output Generation
The module packages the extracted entities into a nested dictionary structure and dumps the output into an AI-friendly JSON format, which can be ingested by the scoring engine in later stages.