# Hybrid PII Redaction Tool for DOCX

A hybrid document redaction tool that detects and anonymizes Personally Identifiable Information (PII) from Microsoft Word (.docx) documents using deterministic regular expressions and Microsoft Presidio (spaCy). The tool preserves document structure while replacing sensitive information with realistic, deterministic fake values.

> Developed as part of the **Scaler AI Labs Internship Assignment**

🌐 **Live Demo:** https://disha-pii-redaction-tool.streamlit.app

---

## Architecture

<p align="center">
<img src="docs/architecture.png" width="900">
</p>

The pipeline combines deterministic pattern matching for structured entities with Named Entity Recognition for contextual entities. Custom Presidio recognizers extend detection for domain-specific organization names while lightweight post-processing reduces false positives.

---

## Features

- Hybrid detection pipeline (Regex + Presidio + spaCy)
- Deterministic fake replacements using Faker
- Consistent replacement mapping across the document
- DOCX paragraph and table processing
- Streamlit web interface
- Offline benchmarking and evaluation framework
- Modular architecture for adding new PII recognizers

---

## Supported PII Types

| Entity | Detection Method |
|---------|------------------|
| Email | Regex |
| Phone Number | Regex |
| Credit Card | Regex |
| SSN / Identifier | Regex |
| IP Address | Regex |
| Person | Presidio + spaCy |
| Organization | Presidio + Custom Recognizers |
| Address | Presidio + Context Validation |

---

## Installation

```bash
git clone https://github.com/thedishajyala/pii-redaction-tool.git

cd pii-redaction-tool

python -m venv .venv

source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## Usage

### Streamlit

```bash
streamlit run app/streamlit_app.py
```

### Command Line

```bash
python src/main.py
```

---

## Evaluation

The system was evaluated on a manually annotated benchmark derived from a financial prospectus.

| Metric | Score |
|---------|-------|
| **Strict F1** | **0.862** |
| **Lenient F1** | **0.920** |
| Best Structured Entity | Email (1.000 F1) |
| Benchmark | 100 Paragraphs |
| Annotated Entities | 135 |

Detailed results are available in [docs/evaluation_report.md](docs/evaluation_report.md).

---

## Project Structure

```
.
├── app/                # Streamlit frontend
├── docs/               # Architecture & evaluation
├── evaluation/         # Benchmark framework
├── input/              # Input documents
├── src/                # Detection pipeline
├── tools/              # Helper scripts
└── requirements.txt
```

---

## Current Limitations

- Image-based PII is not supported.
- OCR/PDF processing is outside the current scope.
- Generic English NER models remain challenging for some legal entities.
- Rich DOCX formatting may not always be preserved after replacement.

---

## Future Improvements

- OCR support for scanned documents
- PDF processing pipeline
- Transformer-based domain-specific NER
- Additional Presidio recognizers for legal documents

---

## Documentation

Additional documentation is available inside the **docs/** folder.

- Architecture
- Evaluation Report
- Annotation Guidelines
- Dataset Profile

---

## Tech Stack

- Python
- Microsoft Presidio
- spaCy
- Faker
- python-docx
- Streamlit

---

## License

This project was developed for the **Scaler AI Labs Internship Assignment**.
