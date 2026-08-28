import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Setup the client
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

print("Starting batch processing...")

# 2. Open and read our dummy dataset file
with open("sample_tickets.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# 3. Split the text document into individual emails
# This looks for our "--- TICKET 1 ---" headers and splits the text there
ticket_list = re.split(r'--- TICKET \d+ ---', raw_text)
# Clean up empty spaces and empty list items
ticket_list = [ticket.strip() for ticket in ticket_list if ticket.strip()]

all_results = []

# 4. Loop through each email, send to Gemini, and save the result
for index, email_text in enumerate(ticket_list, start=1):
    print(f"\nAnalyzing Ticket #{index}...")
    
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=PROMPT_TEMPLATE.format(email=email_text),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Convert the AI's string response into a real JSON object
        ticket_data = json.loads(response.text)
        
        # Add the original email to our data so we have the full context
        ticket_data["original_email"] = email_text 
        all_results.append(ticket_data)
        
        print(f"  -> Successfully triaged as: {ticket_data['category']} ({ticket_data['urgency']})")
        
    except Exception as e:
        print(f"  -> Error processing Ticket #{index}: {e}")

# 5. Save all the combined results into a final JSON file
with open("results.json", "w", encoding="utf-8") as outfile:
    json.dump(all_results, outfile, indent=4)

print("\nAll done! Check your folder for the new 'results.json' file.")