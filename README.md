# Hybrid PII Redaction Tool for DOCX

![Python](https://img.shields.io/badge/Python-3.11-blue)
![spaCy](https://img.shields.io/badge/spaCy-3.8-success)
![Presidio](https://img.shields.io/badge/Microsoft-Presidio-orange)
![DOCX](https://img.shields.io/badge/Input-DOCX-green)

A modular pipeline for detecting and replacing Personally Identifiable Information (PII) with consistent synthetic values using a hybrid approach combining regex-based pattern matching and Microsoft Presidio.

## Live Demo
Check out the deployed app here: **[https://disha-pii-redaction-tool.streamlit.app](https://disha-pii-redaction-tool.streamlit.app)**

---

## Architecture

<p align="center">
  <img src="docs/architecture.png" width="900">
</p>

The runtime pipeline consists of five modular stages:
1. **Document Processing**: Parses `.docx` files into paragraphs and tables.
2. **Detection**: Runs deterministic regex alongside NLP models (Presidio/spaCy) in parallel.
3. **Merging**: Filters unsupported entity types and deduplicates overlapping detections.
4. **Redaction**: Replaces text spans right-to-left with deterministic fake data.
5. **Evaluation**: An offline workflow to benchmark predictions against ground truth.

---

## Features

- **Hybrid Detection**: Combines fast regex for structured data with NLP (Presidio) for unstructured entities.
- **Deterministic Replacement**: Ensures repeated occurrences of the same entity always map to the exact same replacement using a consistent Faker mapping.
- **DOCX Paragraph + Table Support**: Safely parses and modifies `.docx` files, including dense tables and nested paragraphs.
- **Evaluation Framework**: Includes a standalone, offline evaluation pipeline to benchmark precision, recall, and boundary accuracy.
- **Modular Architecture**: Clean separation between document handling, detection, redaction, and evaluation.

---

## Hybrid Detection Strategy

| Entity | Detection Method | Notes |
|--------|------------------|-------|
| **EMAIL** | Regex | Pattern Matching (High Precision) |
| **PHONE** | Regex | Pattern Matching |
| **CREDIT CARD** | Regex | Pattern Matching |
| **SSN** | Regex | Pattern Matching |
| **IP** | Regex | Pattern Matching |
| **PERSON** | Presidio | NLP (spaCy `en_core_web_lg`) |
| **ORGANIZATION** | Presidio | NLP (spaCy `en_core_web_lg`) |
| **ADDRESS** | Presidio | NLP (spaCy `en_core_web_lg`) |

---

## Evaluation Summary

### Evaluation Methodology
The pipeline was evaluated against a manually annotated benchmark consisting of 100 representative paragraphs (135 annotated entities) extracted from a financial prospectus. Both strict span matching and lenient entity-level matching were used to assess performance.

| Metric | Result |
|--------|--------|
| **Benchmark Size** | 100 paragraphs |
| **Annotated Entities**| 135 |
| **Email F1** | 1.000 |
| **Phone F1** | 0.976 |
| **Address F1 (Strict)**| 0.548 |
| **Address F1 (Lenient)**| 0.742 |
| **Organization Detection**| Benchmark highlighted limitations |

### Key Findings
- Regex detection achieved near-perfect performance for structured PII.
- Boundary extraction remains the primary challenge for ADDRESS entities.
- Default Presidio struggled on the curated ORGANIZATION benchmark (Indian corporate/legal entities).
- The evaluation demonstrates strong performance on structured PII (Email and Phone), while highlighting challenges in boundary extraction for Address entities and organization recognition in Indian financial documents.

---

## Design Decisions

| Design Decision | Rationale |
|-----------------|-----------|
| **Hybrid detection** | Regex is extremely reliable for structured PII (emails, phones), while NLP is better suited for names, organizations, and addresses. |
| **Deterministic fake replacements** | Ensures repeated occurrences of the same entity (e.g., a Promoter's name) always map to the same replacement throughout the document, preserving semantic readability. |
| **Right-to-left replacement** | Replaces detected entities from the end of the paragraph to the beginning, preventing string index shifts while modifying text. |
| **Separate evaluation pipeline** | Keeps benchmarking independent of production processing, allowing for rigorous testing without bloating the runtime code. |

---

## Documentation

Additional project documentation is available in the `docs/` directory:

- `architecture.png` – High-level system architecture
- `document_profile.md` – Dataset profiling and complexity analysis
- `evaluation_report.md` – Detailed benchmark results and error analysis
- `annotation_guidelines.md` – Ground truth annotation protocol

---

## Project Structure

```text
.
├── app/
├── docs/
│   ├── annotation_guidelines.md
│   ├── architecture.png
│   ├── document_profile.md
│   └── evaluation_report.md
├── evaluation/
│   ├── evaluate.py
│   ├── matcher.py
│   └── metrics.py
├── src/
│   ├── detector.py
│   ├── replacer.py
│   └── fake_data.py
├── tools/
└── requirements.txt
```

---

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pii-redaction-tool

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install exact pinned dependencies
pip install -r requirements.txt

# Download the required spaCy model
python -m spacy download en_core_web_lg
```

> **Note:** The `en_core_web_lg` model is required for Presidio's NLP-based entity detection and is not installed automatically with `pip install`.

---

## Usage

```bash
python src/main.py
```
Input documents should be placed in the `input/` directory. Redacted documents are written to `output/`.

---

## Known Limitations

- **Formatting Loss**: The right-to-left replacement modifies the entire paragraph text string, which can strip granular rich text formatting (bold/italics) from the modified paragraph.
- **Capitalization Blindness**: Presidio NER struggles to detect names and organizations in ALL CAPS blocks (e.g., table headers, promoter lists).
- **OCR/PDF Support**: The tool operates strictly on `.docx` XML. It cannot extract or redact PII embedded in images or flat PDFs.
- **Organization Accuracy**: The generic `en_core_web_lg` model has low recall for Indian corporate legal entities (e.g., Trusts, LLPs).

---

## Future Improvements

- **Run-aware formatting preservation**: Rebuilding the redaction engine to map character offsets to DOCX `runs` instead of paragraph text.
- **OCR support**: Integrating Tesseract to handle image-based PII.
- **PDF processing**: Extending the `DocumentHandler` to parse PDF layouts.
- **Custom recognizers**: Adding specialized Presidio recognizers for Indian legal entities and localized addresses.
- **Fine-tuned NER**: Training a custom spaCy model on financial prospectuses.

---
This project was developed as part of the Scaler AI Labs Internship.
