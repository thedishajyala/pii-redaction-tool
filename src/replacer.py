class ReplacementEngine:
    """
    Replaces detected PII with generated fake values.
    """

    def replace(self, text: str, matches: list[dict], generator) -> str:
        """
        Replace all detected entities in the text.

        Replacements are applied from right to left so earlier indices
        remain valid.
        """
        # Process from the end of the string
        matches = sorted(matches, key=lambda m: m["start"], reverse=True)

        for match in matches:
            fake_value = generator.generate(
                match["type"],
                match["value"]
            )

            text = (
                text[:match["start"]]
                + fake_value
                + text[match["end"]:]
            )

        return text
