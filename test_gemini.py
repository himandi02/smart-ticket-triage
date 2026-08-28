import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load the API key from your .env file
load_dotenv()

# 2. Initialize the modern GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Define the prompt (the instructions for the AI)
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

# 4. Our test email
sample_email = "I've been trying to reset my password for two days and your app keeps crashing, I need this fixed now!"

print("Sending to Gemini... Please wait.\n")

# 5. Call the API using the current stable model name
response = client.models.generate_content(
    model="gemini-3.6-flash",  # current stable model as of Aug 2026
    contents=PROMPT_TEMPLATE.format(email=sample_email),
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
    )
)

# 6. Print the result
print("--- Raw JSON Output from AI ---")
print(response.text)

# 7. Convert the JSON text into a Python dictionary
result = json.loads(response.text)
print("\n--- Extracted Data ---")
print(f"Urgency Level: {result['urgency']}")
print(f"Issue Category: {result['category']}")
print(f"Sentiment: {result['sentiment']}")
print(f"Drafted Reply: {result['drafted_reply']}")
