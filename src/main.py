from document_handler import DocumentHandler
from detector import RegexDetector
from fake_data import FakeDataGenerator
from replacer import ReplacementEngine


def main():
    handler = DocumentHandler("input/Red Herring Prospectus.docx")

    detector = RegexDetector()
    generator = FakeDataGenerator()
    replacer = ReplacementEngine()

    paragraphs = handler.get_paragraphs()

    for paragraph in paragraphs:
        text = paragraph.text

        if not text.strip():
            continue

        matches = detector.detect(text)

        if not matches:
            continue

        redacted = replacer.replace(
            text,
            matches,
            generator,
        )

        paragraph.text = redacted

    handler.save("output/redacted_prospectus.docx")

    print("✅ Redacted document saved!")


if __name__ == "__main__":
    main()
