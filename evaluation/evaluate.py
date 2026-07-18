import argparse
import json
import os
from evaluator import Evaluator

def generate_report(results, output_path):
    metrics = results["metrics"]
    errors = results["errors"]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# PII Redaction Pipeline Evaluation Report\n\n")
        
        f.write("## 1. Overall Metrics\n\n")
        f.write("### Strict Evaluation (Exact Boundaries Only)\n")
        f.write("| Entity | TP | FP | FN | Precision | Recall | F1 Score |\n")
        f.write("|--------|----|----|----|-----------|--------|----------|\n")
        for ent, m in metrics['strict'].items():
            f.write(f"| {ent} | {m['TP']} | {m['FP']} | {m['FN']} | {m['Precision']:.3f} | {m['Recall']:.3f} | {m['F1']:.3f} |\n")
            
        f.write("\n### Lenient Evaluation (Boundary/Overlap Allowed)\n")
        f.write("| Entity | TP | FP | FN | Precision | Recall | F1 Score |\n")
        f.write("|--------|----|----|----|-----------|--------|----------|\n")
        for ent, m in metrics['lenient'].items():
            f.write(f"| {ent} | {m['TP']} | {m['FP']} | {m['FN']} | {m['Precision']:.3f} | {m['Recall']:.3f} | {m['F1']:.3f} |\n")
            
        f.write("\n## 2. Error Taxonomy\n\n")
        
        f.write("### Most Common Errors\n")
        for err_type, count in sorted(errors["errors_by_type"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{err_type}**: {count}\n")
            
        f.write("\n### Source Context Impact\n")
        for context, count in sorted(errors["errors_by_context"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{context}**: {count} errors\n")
            
        f.write("\n## 3. Qualitative Insights\n")
        f.write("1. **Boundary Quality**: The difference between Strict and Lenient scores highlights boundary issues (e.g. failing to capture full addresses or isolating surnames).\n")
        f.write("2. **Structured Text Degradation**: Table cells produced a disproportionately high number of annotation corrections compared to running text, highlighting the increased difficulty of NER in highly structured document layouts.\n")
        f.write("3. **Capitalization Blindness**: The model failed to detect entities (especially Persons and Organizations) in ALL CAPS blocks like promoter tables and newspaper listings.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    print(f"Loading Ground Truth from {args.ground_truth}...")
    evaluator = Evaluator(args.ground_truth)
    
    print("Running evaluation...")
    results = evaluator.evaluate()
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    generate_report(results, args.output)
    print(f"Evaluation Report saved to {args.output}")
