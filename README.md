# ⚖️ VerdictIQ — Litigation Finance Case Screening Tool

An AI-powered case screening tool for litigation finance, built using open source LLMs running entirely on-device. No data is sent to external servers — critical for legal confidentiality.

## The Problem
Litigation finance firms screen hundreds of cases manually. Early-stage triage relies on human judgment with no scalable, consistent analytical layer — leading to slow decisions and missed opportunities.

## The Solution
VerdictIQ allows analysts to upload a case summary PDF and receive an instant structured analysis including risk scoring, key risk factors, and a funding recommendation — generated locally using Mistral via Ollama.

## Features
- PDF document ingestion and text extraction
- Local AI analysis via Mistral (runs entirely on-device)
- Structured risk scoring (1-10)
- Investment recommendation (Fund / Do Not Fund / Needs More Information)
- Risk level classification (Low / Medium / High)
- No data sent to external APIs — full confidentiality

## Tech Stack
- Python
- Streamlit (UI)
- Ollama + Mistral 7B (local LLM)
- PyPDF2 (PDF extraction)
- Regex (LLM output parsing)

## How to Run
1. Install Ollama from ollama.com and run: `ollama pull mistral`
2. Clone this repository
3. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
4. Install dependencies: `pip install streamlit ollama pypdf2`
5. Run the app: `streamlit run app.py`

## Why Open Source LLMs?
Legal documents are confidential. Sending case summaries to OpenAI or Anthropic APIs creates data privacy risks. Running Mistral locally via Ollama means sensitive case data never leaves the machine — a real constraint in legal tech that this project directly addresses.

## Author
Shruti M — github.com/shruti154
