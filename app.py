import streamlit as st
import ollama
import PyPDF2
import re

st.set_page_config(page_title="VerdictIQ", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.main { padding: 2rem; }
.risk-high { color: #ff4444; font-size: 2rem; font-weight: bold; }
.risk-medium { color: #ffaa00; font-size: 2rem; font-weight: bold; }
.risk-low { color: #00cc44; font-size: 2rem; font-weight: bold; }
.card { background: #1e1e2e; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ VerdictIQ")
st.subheader("Litigation Finance Case Screening Tool")
st.divider()

st.markdown("### Upload a Case Document")
uploaded_file = st.file_uploader("Upload a PDF case summary", type=["pdf"])

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_risk_score(analysis_text):
    match = re.search(r'RISK SCORE[:\s]+(\d+)', analysis_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def get_recommendation(analysis_text):
    if "DO NOT FUND" in analysis_text.upper():
        return "DO NOT FUND", "🔴"
    elif "NEEDS MORE INFORMATION" in analysis_text.upper():
        return "NEEDS MORE INFO", "🟡"
    elif "FUND" in analysis_text.upper():
        return "FUND", "🟢"
    return "UNCLEAR", "⚪"

def analyse_case(case_text):
    prompt = (
        "You are a litigation finance analyst. "
        "Analyse the following case summary and provide:\n\n"
        "1. CASE OVERVIEW (2-3 sentences)\n"
        "2. RISK SCORE (rate from 1-10, where 10 is highest risk)\n"
        "3. KEY RISK FACTORS (list the top 3)\n"
        "4. INVESTMENT RECOMMENDATION (Fund / Do Not Fund / Needs More Information)\n"
        "5. REASONING (2-3 sentences explaining your recommendation)\n\n"
        "Case Summary:\n" + case_text
    )
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

if uploaded_file is not None:
    st.success("Document uploaded successfully!")

    with st.spinner("Extracting text from document..."):
        case_text = extract_text(uploaded_file)

    with st.expander("Click to view raw extracted text"):
        st.write(case_text)

    st.markdown("### AI Analysis")
    with st.spinner("Mistral is analysing the case... this may take 30-60 seconds"):
        analysis = analyse_case(case_text)

    risk_score = parse_risk_score(analysis)
    recommendation, emoji = get_recommendation(analysis)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Risk Score", value=f"{risk_score}/10" if risk_score else "N/A")

    with col2:
        st.metric(label="Recommendation", value=f"{emoji} {recommendation}")

    with col3:
        if risk_score:
            if risk_score <= 3:
                st.metric(label="Risk Level", value="LOW")
            elif risk_score <= 6:
                st.metric(label="Risk Level", value="MEDIUM")
            else:
                st.metric(label="Risk Level", value="HIGH")

    st.divider()
    st.markdown("### Full Analysis")
    st.markdown(analysis)
    st.divider()
    st.caption("Analysis generated locally using Mistral via Ollama. No data sent to external servers.")
