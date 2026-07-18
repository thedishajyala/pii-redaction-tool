# Ground Truth Annotation Guidelines (Version 1.2)

To ensure our evaluation metrics are scientifically reproducible and accurate, we must be consistent when assigning ground truth labels. This document answers common edge cases based on our calibration session.

## General Rules
1. **Punctuation**: Trailing punctuation (like a period at the end of a sentence or a comma) should **NOT** be part of the entity span.
2. **Context Matters**: A word that is a name in one context might be a normal noun in another. Only annotate if it refers to a specific PII entity.
3. **Span Boundaries vs Detection**: We evaluate *detection* primarily. If a predicted span partially overlaps the ground truth (e.g., "John Smith" vs "Mr. John Smith"), it is considered a correct detection with a boundary issue, NOT a complete failure. False Positives are reserved for predictions that are completely wrong (e.g., "Fiscals" as PERSON).

## Entity-Specific Guidelines

### 1. ORGANIZATION / ORG
- **Do annotate**: Specific, named legal, corporate or governmental entities (e.g., "Reserve Bank of India", "OpenAI Inc.", "ICICI Bank", "Maharashtra Pollution Control Board").
- **Do NOT annotate**: Generic words or pronouns referring to an organization (e.g., "the Company", "the Board", "the Promoters", "Department") unless they uniquely refer to a specific named entity in context.
- **Rule 16 (Legal Entities)**: Named legal entities such as Trusts and Funds (e.g., "Dhaulagiri Family Trust", "Everest Family Trust", "ABC LLP") are annotated as `ORGANIZATION`. Do not create a new entity class for them.

### 2. ADDRESS (Highly Calibrated)
- **What counts**: Physical locations that identify a place. This includes full street addresses ("Plot No. F-223", "221B Baker Street") as well as geographic components used as part of a location ("Pune", "Mumbai", "Ahmednagar", "Maharashtra", "India").
- **Facility Names**: Do **NOT** annotate internal facility names (e.g., "Supa Facility", "Manufacturing Facility", "Corporate Office", "Unit 2", "Plant") by themselves. They are not postal addresses. However, if they are followed by a geographic location (e.g., "Supa, Ahilyanagar, Maharashtra"), the geographic components **ARE** annotated.
- **Span Merging**: If multiple components form one continuous physical address (e.g., "Plot No. F-223, Supa Parner Industrial Park, Taluka Parner"), annotate the complete address span rather than isolated fragments if possible.

### 3. PERSON
- **Do annotate**: Full names or distinct surnames (e.g., "John Smith", "Sarthak Malvadkar").
- **Do NOT annotate**: 
  - Generic titles or job roles if they are standalone (e.g., "Director", "CEO", "Company Secretary", "Compliance Officer").
  - Honorifics inside the span (e.g., in "Mr. John Smith", only "John Smith" is the span. Exclude "Mr.", "Mrs.", "Dr.", "Shri").
  - Single surnames unless they clearly identify a specific person.
  - Initials alone (e.g., "A.Y.").

### 4. EMAIL
- Must be a fully qualified email address. Exclude `mailto:` or other HTML/URL artifacts.

### 5. PHONE
- Only actual phone numbers. Do NOT annotate ISO numbers (e.g., "16949"), registration IDs, metric values ("MT"), or years.
- Exclude surrounding contextual text like "Tel:" or "Telephone:" from the span.

### 6. DOB
- Only dates representing actual dates of birth. Do NOT annotate fiscal years ("Fiscals 2025"), agreement dates, issue dates, or balance sheet dates.

### 7. CREDIT CARD / SSN / IP
- Only actual instances of these identifiers.
