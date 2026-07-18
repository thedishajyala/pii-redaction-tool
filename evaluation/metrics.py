from collections import defaultdict

def compute_metrics(match_results):
    """
    Computes Strict and Lenient metrics overall and per entity type.
    
    Strict: Only 'Exact Match' counts as True Positive.
    Lenient: 'Exact Match' and 'Boundary Match' count as True Positive.
    
    Returns a dictionary of metrics.
    """
    
    # Structure: stats[mode][entity_type] = {"TP": 0, "FP": 0, "FN": 0}
    # mode is 'strict' or 'lenient'
    stats = {
        'strict': defaultdict(lambda: {"TP": 0, "FP": 0, "FN": 0}),
        'lenient': defaultdict(lambda: {"TP": 0, "FP": 0, "FN": 0})
    }
    
    for res in match_results:
        status = res["status"]
        gt = res.get("gt")
        pred = res.get("pred")
        
        gt_type = gt["type"] if gt else None
        pred_type = pred["type"] if pred else None
        
        if status == "Exact Match":
            # Strict & Lenient TP
            stats['strict'][gt_type]["TP"] += 1
            stats['strict']['OVERALL']["TP"] += 1
            
            stats['lenient'][gt_type]["TP"] += 1
            stats['lenient']['OVERALL']["TP"] += 1
            
        elif status == "Boundary Match":
            # Strict: Count as FN for GT and FP for Pred
            stats['strict'][gt_type]["FN"] += 1
            stats['strict']['OVERALL']["FN"] += 1
            
            stats['strict'][pred_type]["FP"] += 1
            stats['strict']['OVERALL']["FP"] += 1
            
            # Lenient: TP!
            stats['lenient'][gt_type]["TP"] += 1
            stats['lenient']['OVERALL']["TP"] += 1
            
        elif status == "Type Error":
            # GT was missed (FN), Pred was wrong type (FP)
            stats['strict'][gt_type]["FN"] += 1
            stats['strict']['OVERALL']["FN"] += 1
            
            stats['strict'][pred_type]["FP"] += 1
            stats['strict']['OVERALL']["FP"] += 1
            
            stats['lenient'][gt_type]["FN"] += 1
            stats['lenient']['OVERALL']["FN"] += 1
            
            stats['lenient'][pred_type]["FP"] += 1
            stats['lenient']['OVERALL']["FP"] += 1
            
        elif status == "False Negative":
            stats['strict'][gt_type]["FN"] += 1
            stats['strict']['OVERALL']["FN"] += 1
            
            stats['lenient'][gt_type]["FN"] += 1
            stats['lenient']['OVERALL']["FN"] += 1
            
        elif status == "False Positive":
            stats['strict'][pred_type]["FP"] += 1
            stats['strict']['OVERALL']["FP"] += 1
            
            stats['lenient'][pred_type]["FP"] += 1
            stats['lenient']['OVERALL']["FP"] += 1
            
    # Calculate Precision, Recall, F1
    report = {
        'strict': {},
        'lenient': {}
    }
    
    for mode in ['strict', 'lenient']:
        for ent_type, counts in stats[mode].items():
            tp = counts["TP"]
            fp = counts["FP"]
            fn = counts["FN"]
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            
            report[mode][ent_type] = {
                "TP": tp,
                "FP": fp,
                "FN": fn,
                "Precision": precision,
                "Recall": recall,
                "F1": f1
            }
            
    return report
