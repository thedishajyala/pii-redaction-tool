# Evaluation Report: PII Redaction Pipeline

## Overview
This report documents the performance and engineering observations of the hybrid PII detection pipeline tested against a 127-page financial document (Red Herring Prospectus).

## Detection Performance (Regex)
- **Emails**: 40 successfully detected and replaced. The regex pattern `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` worked perfectly across paragraphs and tables.
- **Phone Numbers**: 1 detected.
- **Missed Formats (Phones)**: The regex `(?:\+91[- ]?)?[6-9]\d{9}` was too strict, missing landline formats (e.g., `+91 22 40094400`, `022-68052182`) and space-delimited formats.
- **SSN / Credit Card / IP**: 0 detected (Expected for this document type).

## Detection Performance (NLP / Presidio)
- Presidio successfully identified `PERSON` and `LOCATION` entities.
- **Observation**: NLP models occasionally miss entities based on context (e.g., "OpenAI" was missed as an Organization in early tests). This highlights the necessity of the hybrid approach.

## Engineering Challenges & Solutions
**Duplicate Detection Bug**: 
During hybrid integration, duplicate detections occurred because the regex and NLP detectors identified the same email using different entity labels (`EMAIL` vs `EMAIL_ADDRESS`). This resulted in overlapping replacements. 
**Resolution**: The issue was resolved by normalizing entity types and deduplicating based on character spans `(start, end)` before replacement, ensuring that a single slice of text is only replaced once.

**Formatting Loss**:
Updating `paragraph.text` directly removes run-level formatting. For a production system requiring perfect format retention, traversing and modifying run objects would be required.
