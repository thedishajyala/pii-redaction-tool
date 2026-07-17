from document_handler import DocumentHandler
from detector import RegexDetector
from fake_data import FakeDataGenerator
from replacer import ReplacementEngine


def redact_text(text, detector, replacer, generator):
    if not text.strip():
        return text

    matches = detector.detect(text)

    if not matches:
        return text

    return replacer.replace(
        text,
        matches,
        generator,
    )


def main():
    handler = DocumentHandler("input/Red Herring Prospectus.docx")

    detector = RegexDetector()
    generator = FakeDataGenerator()
    replacer = ReplacementEngine()

    paragraphs = handler.get_paragraphs()
    tables = handler.get_tables()

    # Process main document paragraphs
    for paragraph in paragraphs:
        paragraph.text = redact_text(
            paragraph.text,
            detector,
            replacer,
            generator,
        )

    # Process all table cells
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.text = redact_text(
                        paragraph.text,
                        detector,
                        replacer,
                        generator,
                    )

    handler.save("output/redacted_prospectus.docx")

    print("✅ Redacted document (paragraphs + tables) saved!")


if __name__ == "__main__":
    main()
