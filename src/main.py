from document_handler import DocumentHandler
from detector import RegexDetector
from presidio_detector import PresidioDetector
from fake_data import FakeDataGenerator
from replacer import ReplacementEngine


def redact_text(text, regex_detector, presidio_detector, replacer, generator):
    if not text.strip():
        return text

    regex_matches = regex_detector.detect(text)
    nlp_matches = presidio_detector.detect(text)
    
    all_matches = regex_matches + nlp_matches
    
    unique_matches = []
    seen = set()
    for m in all_matches:
        identifier = (m["start"], m["end"])
        if identifier not in seen:
            seen.add(identifier)
            unique_matches.append(m)

    if not unique_matches:
        return text

    return replacer.replace(
        text,
        unique_matches,
        generator,
    )


def test_hybrid(regex_detector, presidio_detector, replacer, generator):
    text = "John Smith works at OpenAI and his email is john.smith@gmail.com. He lives at 221B Baker Street."
    print("=" * 50)
    print("HYBRID DETECTION TEST")
    print("=" * 50)
    print(f"Original Text:\n{text}\n")
    redacted = redact_text(text, regex_detector, presidio_detector, replacer, generator)
    print(f"Redacted Text:\n{redacted}\n")


def main():
    regex_detector = RegexDetector()
    presidio_detector = PresidioDetector()
    generator = FakeDataGenerator()
    replacer = ReplacementEngine()

    test_hybrid(regex_detector, presidio_detector, replacer, generator)

    handler = DocumentHandler("input/Red Herring Prospectus.docx")

    paragraphs = handler.get_paragraphs()
    tables = handler.get_tables()

    for paragraph in paragraphs:
        paragraph.text = redact_text(
            paragraph.text,
            regex_detector,
            presidio_detector,
            replacer,
            generator,
        )

    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.text = redact_text(
                        paragraph.text,
                        regex_detector,
                        presidio_detector,
                        replacer,
                        generator,
                    )

    handler.save("output/redacted_prospectus.docx")
    print("✅ Redacted document (paragraphs + tables) saved!")


if __name__ == "__main__":
    main()
