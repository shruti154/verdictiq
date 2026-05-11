import streamlit as st
import ollama
import PyPDF2
import re

st.set_page_config(page_title="VerdictIQ", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0a0a0f; }

.hero { text-align: center; padding: 3rem 0 2rem 0; }
.hero h1 { font-size: 3rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem; }
.hero p { font-size: 1.1rem; color: #888; margin-bottom: 0; }
.badge { display: inline-block; background: #1a1a2e; color: #4ade80; border: 1px solid #4ade80; border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.8rem; margin: 0.5rem 0.2rem; }

.metric-card { background: #111118; border: 1px solid #222; border-radius: 16px; padding: 1.5rem; text-align: center; }
.metric-label { font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.metric-value { font-size: 2rem; font-weight: 700; color: #ffffff; }
.metric-sub { font-size: 0.8rem; color: #555; margin-top: 0.3rem; }

.risk-low { color: #4ade80; }
.risk-medium { color: #facc15; }
.risk-high { color: #f87171; }

.analysis-card { background: #111118; border: 1px solid #222; border-radius: 16px; padding: 1.5rem; margin: 0.5rem 0; }
.analysis-card h4 { color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.8rem; }
.analysis-card p { color: #ccc; font-size: 0.95rem; line-height: 1.6; }

.fund-yes { color: #4ade80; font-size: 1.5rem; font-weight: 700; }
.fund-no { color: #f87171; font-size: 1.5rem; font-weight: 700; }
.fund-maybe { color: #facc15; font-size: 1.5rem; font-weight: 700; }

.footer { text-align: center; color: #333; font-size: 0.75rem; padding: 2rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>⚖️ VerdictIQ</h1>
    <p>AI-powered litigation finance case screening</p>
    <span class="badge">🔒 Runs locally</span>
    <span class="badge">⚡ Mistral 7B</span>
    <span class="badge">🆓 Open source</span>
</div>
""", unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader("Upload a case summary PDF to begin analysis", type=["pdf"])

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_risk_score(text):
    match = re.search(r'RISK SCORE[:\s]+(\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def get_recommendation(text):
    upper = text.upper()
    if "DO NOT FUND" in upper:
        return "DO NOT FUND", "fund-no", "🔴"
    elif "NEEDS MORE INFORMATION" in upper:
        return "NEEDS MORE INFO", "fund-maybe", "🟡"
    elif "FUND" in upper:
        return "FUND", "fund-yes", "🟢"
    return "UNCLEAR", "fund-maybe", "⚪"

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

    with st.spinner("Extracting text..."):
        case_text = extract_text(uploaded_file)

    with st.expander("View raw extracted text"):
        st.write(case_text)

    st.markdown("### Analysing case...")
    with st.spinner("Mistral is reviewing the case... this may take 30-60 seconds"):
        analysis = analyse_case(case_text)

    risk_score = parse_risk_score(analysis)
    recommendation, css_class, emoji = get_recommendation(analysis)

    if risk_score:
        if risk_score <= 3:
            risk_class = "risk-low"
            risk_label = "LOW RISK"
        elif risk_score <= 6:
            risk_class = "risk-medium"
            risk_label = "MEDIUM RISK"
        else:
            risk_class = "risk-high"
            risk_label = "HIGH RISK"
    else:
        risk_class = ""
        risk_label = "N/A"

    st.divider()
    st.markdown("### Case Screening Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk Score</div>
            <div class="metric-value {risk_class}">{risk_score}/10</div>
            <div class="metric-sub">{risk_label}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Recommendation</div>
            <div class="{css_class}">{emoji} {recommendation}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Jurisdiction Risk</div>
            <div class="metric-value" style="color:#888">Review</div>
            <div class="metric-sub">Manual check advised</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Full Analysis")
    st.markdown(analysis)

    st.markdown("""
    <div class="footer">
        Analysis generated locally using Mistral 7B via Ollama · No data sent to external servers · VerdictIQ
    </div>
    """, unsafe_allow_html=True)
