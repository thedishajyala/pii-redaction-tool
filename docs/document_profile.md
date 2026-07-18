# Document Profile: Red Herring Prospectus.docx

## 1. General Information
| Metric | Value |
|--------|-------|
| File Size | 1.76 MB |
| Sections | 85 |
| Total Paragraphs (Main) | 1006 |
| Total Tables | 76 |
| Total Rows | 878 |
| Total Cells | 3722 |

## 2. Paragraph Statistics
| Metric | Value |
|--------|-------|
| Empty Paragraphs | 519 |
| Non-Empty Paragraphs | 4686 |
| Shortest Paragraph | 1 chars |
| Longest Paragraph | 3050 chars |
| Average Length | 94.13 chars |
| Median Length | 17.00 chars |
| 95th Percentile Length | 483.15 chars |

## 3. Formatting Complexity
| Metric | Value |
|--------|-------|
| Total Runs | 68799 |
| Average Runs/Paragraph | 13.22 |
| Paragraphs with >1 Run | 3023 |
| Bold Runs | 11794 |
| Italic Runs | 6071 |
| Underline Runs | 1 |

## 4. Tables
| Metric | Value |
|--------|-------|
| Number of Tables | 76 |
| Largest Table (Cells) | 189 |
| Average Rows/Table | 11.55 |
| Average Columns/Table | 5.04 |

## 5. Text Statistics
| Metric | Value |
|--------|-------|
| Total Characters | 445760 |
| Total Words | 69746 |
| Unique Words | 7128 |
| Average Words/Paragraph | 14.88 |
| Average Word Length | 5.39 chars |
| Longest Word | 83 chars |

## 6. Structure
| Metric | Value |
|--------|-------|
| Headers Present | 85 |
| Footers Present | 85 |
| Images (Inline) | 7 |
| Hyperlinks | Not natively exposed |

## 7. Regex Density (Baseline PII)
| Entity | Count |
|--------|-------|
| Emails Detected | 70 |
| Phones Detected | 1 |
| IPs Detected | 0 |
| Credit Cards Detected | 0 |
| SSNs Detected | 0 |

- **Paragraphs containing Email:** 55
- **Paragraphs containing Phone:** 1

## 8. Runtime Benchmark
| Phase | Duration (s) |
|-------|--------------|
| Load Document | 0.159 |
| Regex Scan | 0.056 |
| Presidio Scan | 26.181 |
| Replacement | 0.037 |
| Save Document | 0.262 |
| **Total Runtime** | **26.694** |

## 9. Observations & Complexity
- **Document Complexity:** High
- **Estimated Redaction Difficulty:** High
- **Observations:**
  - The document contains heavily fragmented formatting (indicated by the high number of runs).
  - A significant portion of the text resides inside 76 tables, justifying our recursive table traversal logic.
  - The performance bottleneck is skewed towards the Presidio (NLP) scanning phase (26.18s vs 0.06s for Regex).
