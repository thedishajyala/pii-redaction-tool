import json
import re
import os

def compile_ground_truth(input_md, output_json):
    with open(input_md, 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = content.split('### Paragraph ID: ')[1:]
    
    ground_truth = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        pid_line = lines[0].strip()
        pid = int(pid_line)
        
        # Determine source
        source = "Running text"
        if "**Source**: Table Cell" in block:
            source = "Table Cell"
            
        # Extract original text
        # Text comes after **Original**: and before **Entities**:
        try:
            original_part = block.split('**Original**:')[1].split('**Entities**:')[0].strip()
        except IndexError:
            continue
            
        # Clean up any Status log from the text if it's there
        if '**Status**:' in original_part:
            original_part = original_part.split('\n', 1)[1].strip()
            
        # Extract entities
        entities = []
        entities_part = block.split('**Entities**:')[1]
        
        # It ends at **Log**: if present, or end of block
        if '**Log**:' in entities_part:
            entities_part = entities_part.split('**Log**:')[0]
            
        entity_lines = entities_part.strip().split('\n')
        for line in entity_lines:
            line = line.strip()
            if line.startswith('- ['):
                match = re.match(r'- \[([A-Z_]+)\]\s*(.*)', line)
                if match:
                    ent_type = match.group(1)
                    ent_text = match.group(2).strip()
                    if ent_type != 'NONE':
                        entities.append({
                            "type": ent_type,
                            "text": ent_text
                        })
                        
        ground_truth.append({
            "paragraph_id": pid,
            "source": source,
            "text": original_part,
            "entities": entities
        })
        
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(ground_truth, f, indent=2, ensure_ascii=False)
        
    print(f"Compiled {len(ground_truth)} paragraphs to {output_json}")

if __name__ == "__main__":
    compile_ground_truth("evaluation/annotations/draft_annotations.md", "evaluation/ground_truth.json")
