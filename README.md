# PII Redaction Tool

A document redaction pipeline that processes DOCX files and automatically detects and deterministically replaces Personally Identifiable Information (PII) using a hybrid approach (Regex + NLP).

## Architecture

This project is built with a modular pipeline architecture:
1. **DocumentHandler**: Parses `.docx` files, extracting both paragraphs and tables.
2. **RegexDetector**: Uses regex to identify structured PII (Emails, Phone numbers, SSNs, IPs, Credit Cards).
3. **PresidioDetector**: Uses Microsoft Presidio (powered by spaCy `en_core_web_lg`) to identify unstructured PII (Names, Locations, Organizations).
4. **FakeDataGenerator**: Deterministically maps real entities to fake entities using Faker, ensuring consistency.
5. **ReplacementEngine**: Replaces identified text spans with fake data from right-to-left, avoiding index corruption.

## Setup
1. Create virtual environment: `python3 -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (or install manually `python-docx Faker presidio-analyzer presidio-anonymizer spacy`)
4. Download spaCy model: `python -m spacy download en_core_web_lg`

## Usage
Place your `.docx` files in the `input/` folder and run:
```bash
python src/main.py
```
The redacted document will be saved to `output/redacted_prospectus.docx`.

## Known Limitations
- The right-to-left replacement of `paragraph.text` strips rich text formatting (bold, italics) from the modified paragraph.
- Regex phone number detection currently expects standard 10-digit mobile numbers and may miss landlines or heavily formatted numbers (e.g., `+91 22 40094400`).
