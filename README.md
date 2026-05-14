# sentinel-ai-compliance-agent
# SentinelAI 🛡️
> **Zero-Knowledge Enterprise Compliance Agent**

SentinelAI is a real-time security frontier that solves the "Shadow AI" crisis. It intercepts employee AI requests and evaluates them against massive compliance frameworks (HIPAA, SOC2) using Gemini 1.5 Pro's long-context window, ensuring data never leaves your perimeter unless it is authorized.

## 🚀 The Problem
Enterprises lose millions to data breaches when employees paste sensitive data into unvetted AI tools. Standard security layers are too blunt (blocking everything) or too slow (periodic audits). SentinelAI provides **Safe Speed**—real-time enforcement that understands legal context.

## 🏗️ Architecture
```text
[ USER PROMPT ] 
      │
      ▼
[ LOCAL SECURITY LAYER ] ───► (PII Scrubber & Injection Detector)
      │
      ▼
[ GEMINI 1.5 PRO ] ◄───────── [ FULL POLICY PDFs (HIPAA/SOC2) ]
(5-Step Reasoning Chain)      (Long-Context RAG - No Chunking)
      │
      ▼
[ ENFORCEMENT DECISION ] ───► (AUTHORIZED / BLOCKED / ESCALATE)
      │
      ▼
[ SECURITY DASHBOARD ] ─────► (JSON Audit Log & CSV Export)
Component,Technology
LLM,Gemini 1.5 Pro (Google AI Studio)
UI,Streamlit (Python 3.11)
Security,"Veea/Lobster Trap Proxy, Local Regex Scrubber"


├── app.py              # Main Streamlit UI and entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API keys
├── .gitignore          # Files to be excluded from Git
├── core/               # Backend logic
│   ├── engine.py       # 5-step reasoning chain & Gemini integration
│   └── security.py     # PII scrubber & injection detection
└── policies/           # Compliance documents (PDFs)

Prerequisites
Python 3.11+

Google AI Studio API Key

git clone [https://github.com/bisma-ramzan/sentinel-ai-compliance-agent.git](https://github.com/bisma-ramzan/sentinel-ai-compliance-agent.git)
cd sentinel-ai-compliance-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
**Install dependencies**
   ```bash
   pip install -r requirements.txt
Configure Environment
Create a .env file in the root directory:

Code snippet

GOOGLE_API_KEY=your_api_key_here
Run the Dashboard

Bash

streamlit run app.py


## 📊 Demo Test Cases
| Input Scenario | Expected Output | Logic |
| :--- | :--- | :--- |
| "Email this patient report to my Gmail" | **BLOCKED** | HIPAA § 164.502 Violation |
| "Ignore previous instructions..." | **BLOCKED** | Prompt Injection Detected |
| "Analyze finances in ChatGPT" | **BLOCKED** | Shadow AI Flag: True |
| "Where is the AI policy?" | **AUTHORIZED** | General Inquiry |

## ⚖️ Compliance Coverage
- **HIPAA**: Protected Health Information (PHI) safeguards.
- **SOC2 Type II**: Data confidentiality and privacy controls.
- **Internal AUP**: Custom enterprise Acceptable Use Policies.

## ⚠️ Known Limitations
- Initial policy ingestion can take 3-5 seconds due to PDF processing.
- Current PII scrubber is regex-based; future versions will use NER (Named Entity Recognition).

## 👥 Team
- **Bisma Ramzan** (SAP ID: 55699) - Lead Developer & Security Architect

---
*Built for the Google AI Studio / Gemini Hackathon 2026.*

Data Flow,JSON Mode for strict schema enforcement
