import time
from collections import Counter
from document_handler import DocumentHandler
from detector import RegexDetector
from presidio_detector import PresidioDetector
from fake_data import FakeDataGenerator
from replacer import ReplacementEngine

SUPPORTED_ENTITY_TYPES = {
    "PERSON",
    "ORGANIZATION",
    "ORG",
    "ADDRESS",
    "EMAIL",
    "PHONE",
    "SSN",
    "CREDIT_CARD",
    "IP"
}

def redact_text(text, regex_detector, presidio_detector, replacer, generator, metrics_counter=None):
    if not text.strip():
        return text

    regex_matches = regex_detector.detect(text)
    nlp_matches = presidio_detector.detect(text)
    
    all_matches = regex_matches + nlp_matches
    
    all_matches = [
        m for m in all_matches
        if m["type"] in SUPPORTED_ENTITY_TYPES
    ]
    
    unique_matches = []
    seen = set()
    for m in all_matches:
        identifier = (m["start"], m["end"])
        if identifier not in seen:
            seen.add(identifier)
            unique_matches.append(m)

    if not unique_matches:
        return text

    if metrics_counter is not None:
        for m in unique_matches:
            metrics_counter[m["type"]] += 1

    return replacer.replace(
        text,
        unique_matches,
        generator,
    )

def run_pipeline(input_path, output_path):
    """
    Runs the pipeline on a document and returns the summary metrics.
    Returns:
        tuple: (metrics_dict, processing_time_seconds)
    """
    start_time = time.time()
    
    regex_detector = RegexDetector()
    presidio_detector = PresidioDetector()
    generator = FakeDataGenerator()
    replacer = ReplacementEngine()
    
    handler = DocumentHandler(input_path)
    metrics_counter = Counter()

    for paragraph in handler.get_paragraphs():
        paragraph.text = redact_text(
            paragraph.text,
            regex_detector,
            presidio_detector,
            replacer,
            generator,
            metrics_counter
        )

    for table in handler.get_tables():
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.text = redact_text(
                        paragraph.text,
                        regex_detector,
                        presidio_detector,
                        replacer,
                        generator,
                        metrics_counter
                    )

    handler.save(output_path)
    processing_time = time.time() - start_time
    
    # Normalize ORG -> ORGANIZATION in metrics
    if "ORG" in metrics_counter:
        metrics_counter["ORGANIZATION"] += metrics_counter.pop("ORG")
        
    return dict(metrics_counter), processing_time

def main():
    import os
    
    input_file = "input/Red Herring Prospectus.docx"
    output_file = "output/redacted_prospectus.docx"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please provide an input document.")
        return
        
    print("Starting redaction pipeline...")
    metrics, duration = run_pipeline(input_file, output_file)
    print(f"✅ Redacted document saved to {output_file}!")
    print(f"Processing time: {duration:.2f} seconds")
    print("Summary:")
    for entity_type, count in sorted(metrics.items()):
        print(f"  {entity_type}: {count}")

if __name__ == "__main__":
    main()
