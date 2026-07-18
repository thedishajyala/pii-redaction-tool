# Evaluation Report

**Project:** Hybrid PII Redaction Tool for DOCX  
**Evaluation Date:** July 2026

---

## Executive Summary

This report evaluates the performance of the Hybrid PII Redaction Tool on a manually annotated benchmark derived from a financial prospectus. The pipeline combines deterministic regular-expression recognizers for structured entities with Microsoft Presidio (spaCy) for contextual entities.

Performance was measured using both **strict** (exact span match) and **lenient** (overlapping span match) evaluation. The results demonstrate excellent accuracy for structured PII while highlighting the limitations of generic English NER models on Indian financial documents.

---

## Key Results at a Glance

| Metric | Result |
|---------|--------|
| Benchmark Size | 100 paragraphs |
| Annotated Entities | 135 |
| Strict F1 | **68.1%** |
| Lenient F1 | **75.5%** |
| Best Performing Entity | Email (F1 = 1.000) |
| Processing Time | 48.1 s |

---

## Benchmark Dataset

| Property | Value |
|----------|-------|
| Source | Financial Prospectus |
| Paragraphs | 100 |
| Annotated Entities | 135 |
| Annotation Method | Manual |
| Evaluation Types | Strict + Lenient |

---

## Evaluation Methodology

Two complementary evaluation strategies were used.

### Strict Evaluation
- Requires an exact boundary match between predicted and annotated entities.
- Measures real-world redaction accuracy.

### Lenient Evaluation
- Accepts overlapping entity spans.
- Separates entity recognition performance from boundary extraction errors.

Using both metrics provides a more complete understanding of the system's strengths and weaknesses.

---

## Overall Metrics

| Metric | Strict | Lenient |
|---------|---------|----------|
| True Positives | 93 | 115 |
| False Positives | 45 | N/A |
| False Negatives | 42 | N/A |
| Precision | 0.674 | 0.719 |
| Recall | 0.689 | 0.852 |
| F1 Score | **0.681** | **0.780** |

---

## Per-Entity Performance

| Entity | Strict F1 | Lenient F1 |
|---------|-----------|------------|
| Email | **1.000** | **1.000** |
| Phone | **0.976** | **0.976** |
| Address | 0.548 | 0.742 |
| Person | 0.529 | 0.621 |
| Organization | 0.000 | 0.000 |

---

## Runtime Characteristics

| Property | Value |
|----------|-------|
| Test Document | Red Herring Prospectus (~1.8 MB) |
| Processing Time | 48.1 s |
| Address Entities | 410 |
| Person Entities | 400 |
| Email Entities | 70 |
| Phone Entities | 64 |
| Deployment Platform | Streamlit Community Cloud |

---

## Error Analysis

### Address Boundary Extraction

The largest difference between strict and lenient evaluation occurs for **Address** entities. In most cases, the pipeline correctly identifies that an address exists but fails to capture the complete span, resulting in partial redaction.

---

### Organization Recognition

Generic English NER models perform poorly on Indian legal and financial organizations.

Examples include:

- Family Trusts
- LLPs
- Exchanges
- Regulatory bodies

These entities frequently go undetected because they are underrepresented in the pretrained model.

---

### Capitalization Effects

Recognition accuracy decreases significantly for entities written entirely in uppercase, particularly within tables and promoter lists.

---

## Key Findings

- Regex-based recognizers achieved near-perfect performance for structured PII such as Email and Phone.
- Boundary extraction remains the primary challenge for Address entities.
- Generic English NER models struggle with Indian corporate and legal terminology.
- Table-heavy layouts and ALL CAPS text reduce recognition performance.

---

## Recommendations

### Short-term

- Improve address boundary merging.
- Add regex support for Date of Birth (DOB).
- Develop custom Presidio recognizers for Indian legal organizations.

### Long-term

- Preserve formatting using DOCX run-level replacement.
- Add OCR support for image-based PII.
- Extend support to PDF documents.
- Train a domain-specific transformer-based NER model.

---

## Limitations

- Evaluation is limited to financial prospectuses.
- Rich-text formatting may not be fully preserved after paragraph-level replacement.
- Cross-paragraph entity resolution is not currently supported.

---

## Future Work

- Preserve formatting at the DOCX run level.
- Improve organization recognition using domain-specific recognizers.
- Support OCR and PDF processing.
- Fine-tune transformer-based NER models on Indian financial documents.

---

## Conclusion

The hybrid architecture successfully combines the precision of deterministic regular expressions with the flexibility of NLP-based entity recognition. Evaluation demonstrates excellent performance for structured PII while identifying clear opportunities to improve contextual entity recognition and boundary extraction. The modular design allows additional recognizers and future enhancements to be integrated with minimal changes to the overall pipeline.
