import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Setup the environment and client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are a customer support triage assistant. Given a customer email, return
ONLY valid JSON with these exact keys:
- "urgency": one of "High", "Medium", "Low"
- "category": one of "Technical Bug", "Billing", "Account Access", "Other"
- "sentiment": one of "Angry", "Confused", "Neutral", "Satisfied"
- "drafted_reply": a short, polite, professional reply addressing the specific issue

Customer email:
\"\"\"{email}\"\"\"
"""

# 2. Build the Streamlit UI
st.set_page_config(page_title="AI Ticket Triage", page_icon="🎫")
st.title("Smart Customer Support Ticket Triage")
st.write("Paste a customer email below and let AI triage it instantly.")

# Create a text area for the user to paste an email
email_input = st.text_area("Customer Email", height=150, placeholder="Paste the customer's message here...")

# Create a button to trigger the analysis
if st.button("Analyze Ticket"):
    if not email_input.strip():
        st.warning("Please paste an email first.")
    else:
        # Show a loading spinner while waiting for Gemini
        with st.spinner("Analyzing..."):
            try:
                # 3. Call Gemini
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=PROMPT_TEMPLATE.format(email=email_input),
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    )
                )
                
                # Parse the JSON response
                result = json.loads(response.text)
                
                # 4. Display the results beautifully using Streamlit columns
                st.success("Analysis Complete!")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Urgency", result["urgency"])
                col2.metric("Category", result["category"])
                col3.metric("Sentiment", result["sentiment"])
                
                st.subheader("Drafted Reply")
                st.info(result["drafted_reply"])
                
            except Exception as e:
                st.error(f"An error occurred: {e}")