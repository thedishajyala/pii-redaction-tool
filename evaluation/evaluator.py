import json
import sys
import os

# Ensure src is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from detector import RegexDetector
from presidio_detector import PresidioDetector
from matcher import match_entities
from metrics import compute_metrics
from error_analysis import analyze_errors

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

class Evaluator:
    def __init__(self, ground_truth_path):
        with open(ground_truth_path, 'r', encoding='utf-8') as f:
            self.ground_truth = json.load(f)
            
        self.regex_detector = RegexDetector()
        self.presidio_detector = PresidioDetector()
        
    def evaluate(self):
        all_matches = []
        
        for item in self.ground_truth:
            text = item["text"]
            source = item.get("source", "Unknown")
            gt_entities = item["entities"]
            
            # Predict
            r_matches = self.regex_detector.detect(text)
            p_matches = self.presidio_detector.detect(text)
            
            # Filter unsupported
            combined = [m for m in (r_matches + p_matches) if m["type"] in SUPPORTED_ENTITY_TYPES]
            
            # Format predictions for matching
            pred_entities = []
            seen = set()
            for m in combined:
                identifier = (m["start"], m["end"])
                if identifier not in seen:
                    seen.add(identifier)
                    
                    # Normalize ORG -> ORGANIZATION for metrics
                    ent_type = "ORGANIZATION" if m["type"] == "ORG" else m["type"]
                    pred_entities.append({
                        "type": ent_type,
                        "text": m["value"]
                    })
                    
            # Match
            matches = match_entities(gt_entities, pred_entities)
            
            # Augment with source context
            for m in matches:
                m["source"] = source
                
            all_matches.extend(matches)
            
        metrics = compute_metrics(all_matches)
        errors = analyze_errors(all_matches)
        
        return {
            "metrics": metrics,
            "errors": errors,
            "total_entities_evaluated": len(all_matches)
        }
