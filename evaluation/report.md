# PII Redaction Pipeline Evaluation Report

## 1. Overall Metrics

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

## 2. Error Taxonomy

### Most Common Errors
- **BOUNDARY**: 8
- **FP-ORGANIZATION**: 6
- **FN-ADDRESS**: 5
- **FP-ADDRESS**: 3
- **TYPE_ERROR**: 2
- **FP-PERSON**: 2
- **FP-PHONE**: 1
- **FN-PERSON**: 1

### Source Context Impact
- **Table Cell**: 15 errors
- **Running text**: 13 errors

## 3. Qualitative Insights
1. **Boundary Quality**: The difference between Strict and Lenient scores highlights boundary issues (e.g. failing to capture full addresses or isolating surnames).
2. **Structured Text Degradation**: Table cells produced a disproportionately high number of annotation corrections compared to running text, highlighting the increased difficulty of NER in highly structured document layouts.
3. **Capitalization Blindness**: The model failed to detect entities (especially Persons and Organizations) in ALL CAPS blocks like promoter tables and newspaper listings.
