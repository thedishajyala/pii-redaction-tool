from presidio_analyzer import AnalyzerEngine


class PresidioDetector:
    def __init__(self):
        self.analyzer = AnalyzerEngine()

    def detect(self, text: str) -> list[dict]:
        results = self.analyzer.analyze(
            text=text,
            language="en",
        )
        
        matches = []
        for result in results:
            matches.append({
                "type": result.entity_type,
                "value": text[result.start:result.end],
                "start": result.start,
                "end": result.end,
            })
            
        return matches
