def match_entities(gt_entities, pred_entities):
    """
    Given a list of Ground Truth (GT) entities and Predicted (Pred) entities,
    computes the matches and alignment errors based on normalized text.
    
    Each entity is a dict: {"type": str, "text": str}
    
    Returns a list of match results.
    Each match result is a dict:
    {
        "status": "Exact Match" | "Boundary Match" | "Type Error" | "False Positive" | "False Negative",
        "gt": dict or None,
        "pred": dict or None
    }
    """
    
    results = []
    
    # Track which entities have been matched
    gt_used = set()
    pred_used = set()
    
    # 1. Exact Match
    for i, gt in enumerate(gt_entities):
        if i in gt_used: continue
        for j, pred in enumerate(pred_entities):
            if j in pred_used: continue
            
            if gt["type"] == pred["type"] and gt["text"] == pred["text"]:
                results.append({
                    "status": "Exact Match",
                    "gt": gt,
                    "pred": pred
                })
                gt_used.add(i)
                pred_used.add(j)
                break
                
    # 2. Boundary Match
    for i, gt in enumerate(gt_entities):
        if i in gt_used: continue
        for j, pred in enumerate(pred_entities):
            if j in pred_used: continue
            
            if gt["type"] == pred["type"]:
                # Check for overlap/containment
                if gt["text"] in pred["text"] or pred["text"] in gt["text"]:
                    results.append({
                        "status": "Boundary Match",
                        "gt": gt,
                        "pred": pred
                    })
                    gt_used.add(i)
                    pred_used.add(j)
                    break
                    
    # 3. Type Error
    for i, gt in enumerate(gt_entities):
        if i in gt_used: continue
        for j, pred in enumerate(pred_entities):
            if j in pred_used: continue
            
            # Exact text match but wrong type
            if gt["text"] == pred["text"] and gt["type"] != pred["type"]:
                results.append({
                    "status": "Type Error",
                    "gt": gt,
                    "pred": pred
                })
                gt_used.add(i)
                pred_used.add(j)
                break
                
    # 4. False Negatives (unmatched GTs)
    for i, gt in enumerate(gt_entities):
        if i not in gt_used:
            results.append({
                "status": "False Negative",
                "gt": gt,
                "pred": None
            })
            
    # 5. False Positives (unmatched Preds)
    for j, pred in enumerate(pred_entities):
        if j not in pred_used:
            results.append({
                "status": "False Positive",
                "gt": None,
                "pred": pred
            })
            
    return results
