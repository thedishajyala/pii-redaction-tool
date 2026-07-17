from presidio_analyzer import AnalyzerEngine


class PresidioDetector:
    ENTITY_MAP = {
        "EMAIL_ADDRESS": "EMAIL",
        "LOCATION": "LOCATION",
    }

    def __init__(self):
        self.analyzer = AnalyzerEngine()

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
