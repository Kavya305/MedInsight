import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads .env file, loads GROQ_API_KEY into environment

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_medical_info(document_text, doc_type="clinical_note"):
    """
    Sends a document to the LLM with a structured prompt,
    asking it to extract specific fields as JSON.
    """

    if doc_type == "clinical_note":
        schema_instruction = """
        Extract the following fields from the clinical note as JSON:
        - symptoms: list of symptoms mentioned
        - medications: list of medications mentioned
        - follow_up: any follow-up action mentioned (or null if none)
        - confidence: "high", "medium", or "low" — how clearly the source text 
            stated these fields (low confidence if the text is vague or ambiguous)
        """
    else:  # insurance_claim
        schema_instruction = """
        Extract the following fields from the insurance claim as JSON:
        - claim_type: type of claim (e.g. "medical", "dental", "vision")
        - amount: the claim amount as a number (or null if not mentioned)
        - flagged_for_review: true if the claim mentions anything unusual or incomplete, else false
        - confidence: "high", "medium", or "low" — how clearly the source text 
            stated these fields (low confidence if the text is vague or ambiguous)
        """

    prompt = f"""You are a precise data-extraction assistant.
{schema_instruction}

Return ONLY valid JSON, no extra text, no explanation.

Document:
{document_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # low temperature = more consistent, less "creative"
    )

    raw_output = response.choices[0].message.content
    return raw_output


def get_structured_data(document_text, doc_type="clinical_note", max_retries=2):
    """
    Calls extract_medical_info, validates the JSON, retries on failure.
    """
    for attempt in range(max_retries + 1):
        raw_output = extract_medical_info(document_text, doc_type)

        try:
            data = json.loads(raw_output)
            return data  # success!
        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1}: got invalid JSON, retrying...")
            continue

    # all retries failed
    return {"error": "Failed to get valid JSON after retries", "raw_output": raw_output}


if __name__ == "__main__":
    sample_note = """
    Patient reports persistent headache and mild fever for 3 days.
    Prescribed paracetamol 500mg twice daily.
    Advised follow-up in one week if symptoms persist.
    """

    result = get_structured_data(sample_note, doc_type="clinical_note")
    print(json.dumps(result, indent=2))

    print("\n--- Testing insurance claim ---")
    sample_claim = """
    Claim submitted for dental checkup and cleaning.
    Amount billed: $150. No prior authorization on file - flagging for manual review.
    """
    claim_result = get_structured_data(sample_claim, doc_type="insurance_claim")
    print(json.dumps(claim_result, indent=2))