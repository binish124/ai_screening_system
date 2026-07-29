# AI Screening & Interview System

This repository contains a modular AI system designed for automated applicant tracking, resume parsing, candidate screening, and AI-driven interviewing.

## 📂 Project Layout

The repository is structured to scale efficiently as we add more complex AI models:

*   **`data/`**: Stores raw and processed datasets, sample resumes, and job descriptions.
*   **`parsers/`**: Contains scripts to extract text and structured data from PDFs, Word docs, and other resume formats.
*   **`ats_engine/`**: The core logic for the Applicant Tracking System, handling candidate pipelines and metadata.
*   **`screening_ai/`**: AI models and prompts dedicated to evaluating candidate qualifications against job requirements.
*   **`interview_ai/`**: Conversational AI agents designed to conduct initial candidate interviews and gather qualitative data[cite: 1].
*   **`scoring/`**: Algorithms and models that calculate final candidate suitability scores[cite: 1].
*   **`utils/`**: Shared helper functions, including our standardized AI activity logger (`logger.py`)[cite: 1].
*   **`tests/`**: Unit and integration tests to verify system integrity (`pytest`)[cite: 1].

---

## 🛠 Code Standards & Documentation Format

To maintain a professional and scalable codebase, all contributions must adhere to the following standards[cite: 1]:

### 1. Code Formatting & Linting
*   **Formatter:** We use **Black** for uncompromising code formatting. Run `black .` before committing any code.
*   **Linter:** We use **Pylint** to catch errors and enforce coding standards.
*   **Style Guide:** All Python code must strictly adhere to **PEP 8** standards.

### 2. Documentation Standard
*   **Docstrings:** All modules, classes, and functions must be documented using **Google-style docstrings**. This ensures our AI components are easily readable.
*   **Type Hinting:** Python type hints (e.g., `def parse_resume(file_path: str) -> dict:`) are mandatory for all function signatures to improve predictability and IDE support.

### 3. Logging
*   Do not use standard `print()` statements for AI logic. 
*   Always import and utilize the centralized logger from `utils.logger` to ensure all model inputs, outputs, and errors are safely recorded in `logs/ai_system.log`[cite: 1].