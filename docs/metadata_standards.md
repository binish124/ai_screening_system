# Metadata Standards Document

To maintain data integrity, establish chronological timelines, and track AI version performance, every data payload across the system must include the following metadata envelope.

```json
{
  "_metadata": {
    "candidate_id": "cnd-1234-abcd",
    "job_id": "job-9876-wxyz",
    "processing_timestamp": "2026-08-04T11:14:02Z",
    "model_version": {
      "extractor": "v1.0.2",
      "ats_engine": "v2.1.0"
    },
    "environment": "production"
  }
}