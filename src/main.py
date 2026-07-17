from document_handler import DocumentHandler
from detector import RegexDetector


def main():
    handler = DocumentHandler("input/Red Herring Prospectus.docx")
    detector = RegexDetector()

    paragraphs = handler.get_paragraphs()

    print("=" * 50)
    print("EMAILS FOUND")
    print("=" * 50)

    total = 0

    for paragraph in paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        matches = detector.detect(text)

        if matches:
            print(f"\nParagraph:")
            print(text)

            print("Detected:")

            for match in matches:
                print(f"   ✅ {match}")
                total += 1

    print("\n" + "=" * 50)
    print(f"Total entities found: {total}")


if __name__ == "__main__":
    main()
