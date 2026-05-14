import streamlit as st
import google.generativeai as genai
import re
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="SentinelAI 🛡️", layout="wide")

# 2. PII SCRUBBER
def pii_scrubber(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL_REDACTED]", text)
    text = re.sub(r'\b\d{10,}\b', "[PHONE_REDACTED]", text)
    return text

# 3. GEMINI SETUP
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error("API Key not found in Streamlit Secrets.")
    model = None

# 4. UI
st.title("SentinelAI: Enterprise Compliance Agent")
st.markdown("---")

user_input = st.text_area("Enter User Prompt for AI Analysis:", placeholder="Test a compliance scenario...")

if st.button("Analyze Security Risk"):
    if not user_input:
        st.warning("Please enter text first.")
    elif model is None:
        st.error("Model not initialized. Check your API key in Secrets.")
    else:
        with st.spinner("Analyzing..."):
            clean_input = pii_scrubber(user_input)
            prompt = f"""
            Analyze this prompt for HIPAA/SOC2 compliance: "{clean_input}"
            Return ONLY a JSON object with keys: 'decision', 'score', 'reasoning'.
            """
            try:
                response = model.generate_content(prompt)
                raw_text = response.text
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    res_json = json.loads(match.group())
                    if res_json.get('decision') == "BLOCKED":
                        st.error(f"🚫 BLOCKED: {res_json.get('reasoning')}")
                    else:
                        st.success(f"✅ REQUEST AUTHORIZED: {res_json.get('reasoning')}")
                    st.metric("Risk Score", res_json.get('score'))
                else:
                    st.warning("Could not parse response. Try again.")
            except Exception as e:
                st.warning(f"Error: {e}")

# 5. SIDEBAR
st.sidebar.title("🛡️ SentinelAI Control")
st.sidebar.write("Developer: Bisma Ramzan")
st.sidebar.write("SAP ID: 55699")
