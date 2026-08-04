# AI Data Pipeline Diagram

This diagram maps the lifecycle of AI data from upload to the final hiring decision, including the machine learning retraining loop.

```mermaid
graph TD
    %% Define Pipeline Stages
    A[Raw Candidate Resume Upload] -->|Saved to Blob Storage| B(parsers/extractor.py)
    B -->|Extracts Text & Cleans| C{Parsed Candidate JSON}
    
    J[Raw Job Description] -->|parsers/jd_parser.py| K{Parsed JD JSON}
    
    C -->|Input| D(ats_engine/)
    K -->|Input| D
    D -->|Generates Match Metrics| E{ATS Score JSON}
    
    E -->|If Score > Threshold| F(screening_ai/)
    F -->|Outbound Call & Text Parsing| G{Screening Report JSON}
    
    G -->|If Passed| H(interview_ai/)
    H -->|HR/Tech/Machine Test| I{Interview Results JSON}
    
    I --> L(scoring/ Aggregation)
    L --> M[Final Hiring Decision]
    
    %% Retraining Loop
    M -.->|Feedback Loop: Hired/Rejected| N[(Retraining Dataset)]
    N -.->|Updates Models| D
    N -.->|Updates Models| F
    N -.->|Updates Models| H