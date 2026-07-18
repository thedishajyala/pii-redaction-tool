from collections import defaultdict

def analyze_errors(match_results_with_context):
    """
    Expects match results augmented with "source" (e.g. Table Cell, Running text)
    Returns a dictionary summarizing error patterns.
    """
    
    summary = {
        "errors_by_type": defaultdict(int),
        "errors_by_context": defaultdict(int),
        "boundary_issues": 0,
        "type_errors": 0,
        "false_positives": defaultdict(int),
        "false_negatives": defaultdict(int)
    }
    
    for res in match_results_with_context:
        status = res["status"]
        source = res.get("source", "Unknown")
        
        if status == "Exact Match":
            continue
            
        # Log that an error occurred in this context
        summary["errors_by_context"][source] += 1
        
        if status == "Boundary Match":
            summary["boundary_issues"] += 1
            summary["errors_by_type"]["BOUNDARY"] += 1
            
        elif status == "Type Error":
            summary["type_errors"] += 1
            summary["errors_by_type"]["TYPE_ERROR"] += 1
            
        elif status == "False Positive":
            ent_type = res["pred"]["type"]
            summary["false_positives"][ent_type] += 1
            summary["errors_by_type"][f"FP-{ent_type}"] += 1
            
        elif status == "False Negative":
            ent_type = res["gt"]["type"]
            summary["false_negatives"][ent_type] += 1
            summary["errors_by_type"][f"FN-{ent_type}"] += 1
            
    # Convert defaultdicts to dicts for clean JSON serialization
    summary["errors_by_type"] = dict(summary["errors_by_type"])
    summary["errors_by_context"] = dict(summary["errors_by_context"])
    summary["false_positives"] = dict(summary["false_positives"])
    summary["false_negatives"] = dict(summary["false_negatives"])
    
    return summary
