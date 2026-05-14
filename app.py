import streamlit as st
import google.generativeai as genai
import os
import re
import json
from datetime import datetime

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="SentinelAI 🛡️", layout="wide")

# 2. THE PII SCRUBBER (Local Security Layer)
def pii_scrubber(text):
    # Basic regex for Email and Phone (Demonstration version)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL_REDACTED]", text)
    text = re.sub(r'\b\d{10,}\b', "[PHONE_REDACTED]", text)
    return text

# 3. GEMINI 1.5 PRO SETUP
# Make sure to add your GOOGLE_API_KEY to your Streamlit Secrets!
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")

# 4. STREAMLIT UI - SIDEBAR
with st.sidebar:
    st.title("🛡️ SentinelAI Control")
    st.info("Status: Active | Policy: HIPAA + SOC2")
    st.divider()
    st.write("First Person: Bisma Ramzan")
    st.write("SAP ID: 55699")

# 5. MAIN DASHBOARD
st.title("SentinelAI: Enterprise Compliance Agent")
st.markdown("---")

user_input = st.text_area("Enter User Prompt for AI Analysis:", 
                         placeholder="e.g., Can I email this patient report to my personal Gmail?")

if st.button("Analyze Security Risk"):
    if user_input:
        with st.spinner("Analyzing against global compliance frameworks..."):
            
            # Step A: Local PII Scrubbing
            clean_input = pii_scrubber(user_input)
            
            # Step B: Gemini 1.5 Pro Reasoning Chain
            # Note: In a production version, you would attach the HIPAA/SOC2 PDFs here.
            prompt = f"""
            You are a Security Compliance Officer. Analyze this prompt: "{clean_input}"
            
            Perform a 5-step reasoning chain:
            1. Intent Classification
            2. Sensitivity Scanning
            3. Policy Lookup (HIPAA/SOC2)
            4. Risk Scoring (0-10)
            5. Final Enforcement Decision (AUTHORIZED or BLOCKED)
            
            Return ONLY a valid JSON object with these keys: 
            'decision', 'score', 'citation', 'reasoning'.
            """
            
          try:
                # Cleaner way to extract JSON even if there is extra text
                raw_text = response.text
                clean_json = re.search(r'\{.*\}', raw_text, re.DOTALL).group()
                res_json = json.loads(clean_json)
                
                # UI Display based on Risk
                if res_json.get('decision') == "BLOCKED":
                    st.error(f"🚫 REQUEST BLOCKED: {res_json.get('reasoning')}")
                else:
                    st.success(f"✅ REQUEST AUTHORIZED: {res_json.get('reasoning')}")
