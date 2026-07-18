# PII Redaction Pipeline Architecture

```mermaid
graph TD
    %% Styling
    classDef user fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef pipeline fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef outputs fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef eval fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef utility fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px;

    %% ----------------------------------------------------
    %% Main Pipeline
    %% ----------------------------------------------------
    User([User]) ::: user -->|Input DOCX File| Handler(DocumentHandler <br/> Paragraphs + Tables) ::: utility

    subgraph Detection Layer
        direction TB
        Handler --> Regex(Regex Detector <br/> EMAIL • PHONE • SSN • IP • Credit Card) ::: pipeline
        Handler --> NLP(Presidio Detector <br/> PERSON • ORG • ADDRESS) ::: pipeline
        
        Regex --> Merge(Merge Results) ::: utility
        NLP --> Merge
        
        Merge --> Filter(Filter Supported Types) ::: utility
        Filter --> Dedup(Deduplicate) ::: utility
    end

    subgraph Redaction Layer
        direction TB
        Dedup --> Replace(Replacement Engine) ::: pipeline
        Replace --> Fake(Fake Data Generator) ::: pipeline
    end
    
    Fake --> Out([Redacted DOCX]) ::: outputs

    %% ----------------------------------------------------
    %% Evaluation Pipeline (Separate Workflow)
    %% ----------------------------------------------------
    subgraph Evaluation Workflow
        direction TB
        EvalDoc([Document]) ::: eval --> GT([Ground Truth]) ::: eval
        EvalDoc --> Preds([Model Predictions]) ::: eval
        
        GT --> Matcher(Matcher) ::: eval
        Preds --> Matcher
        
        Matcher --> Metrics(Metrics) ::: eval
        Matcher --> Errors(Error Analysis) ::: eval
        
        Metrics --> Report([Evaluation Report]) ::: outputs
        Errors --> Report
    end
```
