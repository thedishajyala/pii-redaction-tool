import re


class RegexDetector:
    """
    Detect structured PII using regular expressions.
    """

    PATTERNS = {
        "EMAIL": re.compile(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        ),
        "PHONE": re.compile(
            r"(?:\+91[- ]?)?[6-9]\d{9}"
        ),
        "IP_ADDRESS": re.compile(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ),
        "SSN": re.compile(
            r"\b\d{3}-\d{2}-\d{4}\b"
        ),
        "CREDIT_CARD": re.compile(
            r"\b(?:\d{4}[- ]?){3}\d{4}\b"
        ),
    }

    def detect(self, text: str) -> list[dict]:
        """
        Detect all supported PII entities.
        """
        matches = []

        for entity_type, pattern in self.PATTERNS.items():
            for match in pattern.finditer(text):
                matches.append(
                    {
                        "type": entity_type,
                        "value": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

        return matches
