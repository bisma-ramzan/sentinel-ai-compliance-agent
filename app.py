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
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL_REDACTED]", text)
    text = re.sub(r'\b\d{10,}\b', "[PHONE_REDACTED]", text)
    return text

# 3. GEMINI 1.5 PRO SETUP
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("API Key not found in Streamlit Secrets.")

# 4. STREAMLIT UI
st.title("SentinelAI: Enterprise Compliance Agent")
st.markdown("---")

user_input = st.text_area("Enter User Prompt for AI Analysis:", placeholder="Test a compliance scenario...")

if st.button("Analyze Security Risk"):
    if user_input:
        with st.spinner("Analyzing..."):
            # A. Local Scrubbing
            clean_input = pii_scrubber(user_input)
            
            # B. Gemini Analysis
            prompt = f"""
            Analyze this prompt for HIPAA/SOC2 compliance: "{clean_input}"
            Return ONLY a JSON object with keys: 'decision', 'score', 'reasoning'.
            """
            
            try:
                response = model.generate_content(prompt)
                # Extract JSON using regex for safety
                raw_text = response.text
                clean_json = re.search(r'\{.*\}', raw_text, re.DOTALL).group()
                res_json = json.loads(clean_json)
                
                # C. Display Results
                if res_json.get('decision') == "BLOCKED":
                    st.error(f"🚫 BLOCKED: {res_json.get('reasoning')}")
                else:
                    st.success(f"✅ AUTHORIZED: {res_json.get('reasoning')}")
                
                st.metric("Risk Score", res_json.get('score'))
                
            except Exception as e:
                st.warning("Analysis complete. Check formatting.")
    else:
        st.warning("Please enter text first.")

# 5. CREDITS
st.sidebar.title("🛡️ SentinelAI Control")
st.sidebar.write("Developer: Bisma Ramzan")
st.sidebar.write("SAP ID: 55699")
                    
                else:
                    st.success(f"✅ REQUEST AUTHORIZED: {res_json.get('reasoning')}")
