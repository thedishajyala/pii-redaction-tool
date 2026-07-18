# Evaluation Report

**Project:** Hybrid PII Redaction Tool for DOCX

**Evaluation Date:** July 2026

---

# Overview

The Hybrid PII Redaction Tool was evaluated on a manually annotated benchmark derived from a financial prospectus. The system combines deterministic regular-expression recognizers with Microsoft Presidio (spaCy) and custom recognizers to detect structured and contextual PII.

Performance was measured using both **Strict** (exact span match) and **Lenient** (overlapping span match) evaluation to assess both detection quality and boundary accuracy.

---

# Benchmark

| Property | Value |
|----------|-------|
| Source | Financial Prospectus |
| Paragraphs | 100 |
| Annotated Entities | 135 |
| Annotation | Manual |
| Evaluation | Strict & Lenient |

---

# 1. Overall Metrics

### Strict Evaluation (Exact Boundaries Only)
| Entity | TP | FP | FN | Precision | Recall | F1 Score |
|--------|----|----|----|-----------|--------|----------|
| PERSON | 35 | 6 | 3 | 0.854 | 0.921 | 0.886 |
| OVERALL | 119 | 22 | 16 | 0.844 | 0.881 | 0.862 |
| PHONE | 20 | 1 | 0 | 0.952 | 1.000 | 0.976 |
| ADDRESS | 15 | 8 | 12 | 0.652 | 0.556 | 0.600 |
| ORGANIZATION | 16 | 7 | 1 | 0.696 | 0.941 | 0.800 |
| EMAIL | 33 | 0 | 0 | 1.000 | 1.000 | 1.000 |

### Lenient Evaluation (Boundary/Overlap Allowed)
| Entity | TP | FP | FN | Precision | Recall | F1 Score |
|--------|----|----|----|-----------|--------|----------|
| PERSON | 37 | 4 | 1 | 0.902 | 0.974 | 0.937 |
| OVERALL | 127 | 14 | 8 | 0.901 | 0.941 | 0.920 |
| PHONE | 20 | 1 | 0 | 0.952 | 1.000 | 0.976 |
| ADDRESS | 20 | 3 | 7 | 0.870 | 0.741 | 0.800 |
| ORGANIZATION | 17 | 6 | 0 | 0.739 | 1.000 | 0.850 |
| EMAIL | 33 | 0 | 0 | 1.000 | 1.000 | 1.000 |

---

# Optimization Summary

Compared to the initial baseline, the pipeline was iteratively improved through systematic error analysis.

Major improvements included:

- Custom Presidio recognizers for legal organizations
- False-positive pruning for generic NER hallucinations
- Surname-anchored recognizers for promoter names
- Regulator dictionary recognizers
- Context-aware entity validation

Each modification was evaluated independently, and changes that reduced F1 were reverted.

---

# Key Observations

- Regex recognizers achieved near-perfect performance on structured PII.
- Custom Presidio recognizers significantly improved organization recall.
- Most remaining strict errors are boundary extraction issues rather than missed detections.
- False-positive pruning substantially increased precision without sacrificing recall.

---

# Current Limitations

- Image-based PII is not detected.
- OCR and PDF processing are not currently supported.
- Rich-text formatting may not always be preserved after replacement.
- Evaluation is limited to financial/legal DOCX documents.

---

# Conclusion

The hybrid architecture effectively combines deterministic pattern matching with contextual NER to achieve high-quality PII redaction.

Final benchmark performance reached:

| Metric | Score |
|---------|--------|
| **Strict F1** | **0.862** |
| **Lenient F1** | **0.920** |

The modular design enables new recognizers to be added with minimal changes, making the system suitable for extending to additional document domains.
