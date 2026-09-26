import streamlit as st
import json
from main import get_structured_data
from eval_data import CLINICAL_NOTES, INSURANCE_CLAIMS
from evaluate import run_evaluation

st.set_page_config(page_title="MedInsight", page_icon="🩺", layout="wide")

st.title("🩺 MedInsight")
st.caption("AI-powered structured extraction for clinical notes and insurance claims")

tab1, tab2 = st.tabs(["📄 Document Extractor", "📊 Evaluation Dashboard"])

# ---- TAB 1: Live extractor ----
with tab1:
    st.subheader("Try it live")
    doc_type = st.radio("Document type", ["clinical_note", "insurance_claim"], horizontal=True)

    default_text = CLINICAL_NOTES[0] if doc_type == "clinical_note" else INSURANCE_CLAIMS[0]
    document_text = st.text_area("Paste document text:", value=default_text, height=150)

    if st.button("Extract Structured Data", type="primary"):
        with st.spinner("Calling LLM and validating output..."):
            result = get_structured_data(document_text, doc_type=doc_type)
        st.json(result)

# ---- TAB 2: Evaluation dashboard ----
with tab2:
    st.subheader("Reliability Evaluation")
    st.write("Runs the pipeline across a fixed test set and reports extraction reliability.")

    if st.button("Run Evaluation"):
        with st.spinner("Running evaluation across test set..."):
            results = run_evaluation()

        cn = results["clinical_notes"]
        ic = results["insurance_claims"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Clinical Notes Success", f"{cn['success']}/{cn['total']}")
        col2.metric("Claims Success", f"{ic['success']}/{ic['total']}")
        col3.metric("Claims Flagged", ic["flagged"])

        overall_total = cn["total"] + ic["total"]
        overall_success = cn["success"] + ic["success"]
        overall_rate = (overall_success / overall_total) * 100 if overall_total else 0
        st.metric("Overall Reliability", f"{overall_rate:.1f}%")