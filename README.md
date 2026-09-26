# MedInsight

AI-powered structured extraction pipeline for healthcare data that turns unstructured clinical notes and insurance claims into structured, actionable JSON.

## Why this matters

Hospitals and insurers deal with mountains of unstructured text - doctors' notes, claim descriptions that computers can't act on directly. This pipeline bridges that gap: it extracts structured fields (symptoms, medications, claim amounts, review flags) so downstream systems can search, dashboard, and automate on the data.

## Features

- **Schema-adaptive prompt engineering** - one pipeline, two document types (clinical notes, insurance claims), each with its own extraction schema
- **Reliability via retry logic** - validates LLM output as JSON, retries on malformed responses instead of failing silently
- **Confidence flagging** - the model self-reports extraction confidence (high/medium/low) based on source-text clarity
- **Automatic review flagging** - insurance claims are auto-flagged when they contain incomplete or unusual information
- **Evaluation harness** - measures extraction reliability across a test set (currently 100% across 10 documents)
- **Streamlit dashboard** - live document extraction + evaluation metrics in a browser UI

## Tech Stack

Python · Groq LLM API (`openai/gpt-oss-20b`) · Streamlit

## Design decisions

- **`temperature=0`** - structured extraction needs consistency, not creativity
- **Explicit "return only JSON" instruction** - prevents chatty preamble breaking the parser
- **Retry-on-malformed-JSON** - real reliability engineering, not just "hope the API behaves"

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Run the CLI test:
```bash
python main.py
```

Run the evaluation:
```bash
python evaluate.py
```

Run the dashboard:
```bash
streamlit run app.py
```

## Example

Input:
> "Patient reports persistent headache and mild fever for 3 days. Prescribed paracetamol 500mg twice daily."

Output:
```json
{
  "symptoms": ["persistent headache", "mild fever"],
  "medications": ["paracetamol 500mg twice daily"],
  "follow_up": "follow-up in one week if symptoms persist",
  "confidence": "high"
}
```
