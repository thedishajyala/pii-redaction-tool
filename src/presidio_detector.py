from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern


class PresidioDetector:
    ENTITY_MAP = {
        "EMAIL_ADDRESS": "EMAIL",
        "PHONE_NUMBER": "PHONE",
        "LOCATION": "ADDRESS",
    }

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        
        org_pattern = Pattern(
            name="org_pattern",
            regex=r"\b(?:(?!(?:The|Our)\b)[A-Z][a-zA-Z0-9&'-]*\s+){1,5}(?i:Family Trust|Trust|HUF|Board|Private Limited|Pvt Ltd|Ltd|LLP|Partnership|Holding Company)\b",
            score=1.0
        )
        org_recognizer = PatternRecognizer(
            supported_entity="ORGANIZATION",
            patterns=[org_pattern]
        )
        self.analyzer.registry.add_recognizer(org_recognizer)
        
        # Regulator / Short Org Recognizer
        regulator_pattern = Pattern(
            name="regulator_pattern",
            regex=r"\b(?:SEBI|NPCI|RBI|IRDAI|EVEREST)\b",
            score=1.0
        )
        regulator_recognizer = PatternRecognizer(
            supported_entity="ORGANIZATION",
            patterns=[regulator_pattern]
        )
        self.analyzer.registry.add_recognizer(regulator_recognizer)

        # Surname-Anchored ALL CAPS Recognizer
        person_caps_pattern = Pattern(
            name="surname_anchored_caps_pattern",
            regex=r"\b(?:[A-Z]{3,}\s+){1,3}(?:HEGDE|SHETTY|JOSHI|WAKHELE|MALVADKAR)\b",
            score=0.85
        )
        person_caps_recognizer = PatternRecognizer(
            supported_entity="PERSON",
            patterns=[person_caps_pattern]
        )
        self.analyzer.registry.add_recognizer(person_caps_recognizer)

    def detect(self, text: str) -> list[dict]:
        results = self.analyzer.analyze(
            text=text,
            language="en",
        )
        
        matches = []
        for result in results:
            entity_type = self.ENTITY_MAP.get(result.entity_type, result.entity_type)
            matches.append({
                "type": entity_type,
                "value": text[result.start:result.end],
                "start": result.start,
                "end": result.end,
            })
            
        return matches
