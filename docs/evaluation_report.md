# Evaluation Report

**Project:** Hybrid PII Redaction Tool for DOCX  
**Evaluation Date:** July 2026

> **Note:** This evaluation report documents the performance of the current implementation on a manually curated benchmark. The reported metrics should not be interpreted as general-purpose performance across all document types.

## Objective

The goal of this evaluation was to measure the detection performance of the hybrid PII redaction pipeline on a manually annotated benchmark derived from a financial prospectus. The evaluation focuses on entity detection quality, boundary accuracy, and common failure modes.

## Benchmark Dataset

| Property | Value |
|----------|-------|
| Source | Financial Prospectus |
| Paragraphs | 100 |
| Annotated Entities | 135 |
| Annotation Method | Manual |
| Evaluation Types | Strict + Lenient |

## Entity Challenge Summary

| Entity | Main Challenge |
|--------|----------------|
| **PERSON** | Boundary errors and field labels |
| **ADDRESS** | Span extraction (fragmentation) |
| **ORGANIZATION** | Indian legal entities (Trusts, Exchanges) |
| **EMAIL** | None observed |
| **PHONE** | Minor confusion with registration IDs |

## Overall Metrics

### Strict Evaluation (Exact Boundaries Only)
| Metric | Result |
|--------|--------|
| **Total Unique Entities Detected** | 93 (True Positives) |
| **Overall Precision** | 0.674 |
| **Overall Recall** | 0.689 |
| **Overall F1 Score** | 0.681 |

### Lenient Evaluation (Boundary/Overlap Allowed)
| Metric | Result |
|--------|--------|
| **Total Unique Entities Detected** | 103 (True Positives) |
| **Overall Precision** | 0.746 |
| **Overall Recall** | 0.763 |
| **Overall F1 Score** | 0.755 |

## Per-Entity Results

| Entity | TP (Strict) | F1 (Strict) | TP (Lenient) | F1 (Lenient) |
|--------|-------------|-------------|--------------|--------------|
| **EMAIL** | 33 | 1.000 | 33 | 1.000 |
| **PHONE** | 20 | 0.976 | 20 | 0.976 |
| **ADDRESS** | 17 | 0.548 | 23 | 0.742 |
| **PERSON** | 23 | 0.529 | 27 | 0.621 |
| **ORGANIZATION**| 0 | 0.000 | 0 | 0.000 |

## Error Analysis

### False Positives

**Context & Field Labels**
- Generic field labels like "Email" or "Fiscals" misinterpreted as PERSON entities.
- Generic business terms (e.g., "Distriparks") flagged as PERSON.

**Location Context Errors**
- Units of measurement (e.g., "MT") or administrative concepts (e.g., "United States of America" inside an accounting standard name) flagged as physical ADDRESS entities.

**Boundary Over-Extension**
- ADDRESS spans fragmenting or splitting incorrectly across commas and newline characters.

### False Negatives

**Formatting Artifacts (Capitalization Blindness)**
- Promoter names and corporate entities completely missed when appearing in ALL CAPS table blocks.

**Domain Vocabulary Deficiencies**
- Missing Indian corporate entities (e.g., "HUF", "Family Trust").
- Missing regulatory bodies and stock exchanges (e.g., "SEBI", "BSE", "NSE", "RoC").
- Missing Indian newspaper titles.

## Key Findings

- Regex-based detection achieved near-perfect performance on structured PII (Email and Phone).
- Boundary extraction remains the primary limitation for ADDRESS entities, evidenced by a ~20 point gap between strict and lenient F1 scores.
- Generic English NER models struggle with Indian legal organizations and financial domain vocabulary.
- Table cells and ALL CAPS text significantly reduced recognition performance compared to standard prose.

## Limitations

- The benchmark specifically tests financial prospectuses; performance on other formats (e.g., medical records, legal contracts) is unverified.
- Document-level formatting loss can occur within heavily redacted paragraphs due to string-level substitution.
- The pipeline does not support cross-paragraph entity resolution (e.g., linking a first name on page 1 with a surname on page 2).

## Future Work

- Map replacement offsets to DOCX `runs` rather than full paragraphs to preserve exact rich-text formatting.
- Implement domain-specific exclusion lists (e.g., ignoring "the Company" or specific accounting standards).
- Train custom spaCy recognizers targeted at Indian addresses and organizational entities.
- Introduce an OCR pipeline to extract and redact PII embedded in images within the `.docx`.
