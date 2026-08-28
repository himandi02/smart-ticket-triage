# 🎫 Smart Customer Support Ticket Triage

## Overview
This project is a Generative AI application built for a Data Science Internship. It solves a common business problem in customer support: the manual triage of incoming emails. 

When a customer submits a support ticket, this application uses a Large Language Model (LLM) to automatically analyze the text, extract key metrics (urgency, issue category, and sentiment), and draft a personalized, professional reply. 

## Business Value
Customer support teams spend countless hours reading and categorizing unstructured text. By automating the initial triage step, this tool allows agents to prioritize high-urgency issues immediately and respond faster using the AI-drafted replies.

## Technologies Used
*   **Python:** Core application logic.
*   **Google Gemini API (`gemini-3.6-flash`):** The LLM used for natural language processing and JSON generation.
*   **Streamlit:** Used to build the interactive web dashboard.

## Setup Instructions
To run this project locally:

1. Clone the repository and navigate to the project folder.
2. Create a virtual environment: `python -m venv venv` and activate it.
3. Install the required packages: `pip install google-genai streamlit python-dotenv`
4. Create a `.env` file in the root directory and add your API key: `GEMINI_API_KEY=your_key_here`
5. Run the web app: `streamlit run app.py`

## Example Output
When given the following input: 
> *"I've been trying to reset my password for two days and your app keeps crashing every time I click the link. I need this fixed NOW, I have work to do!"*

The AI successfully generates this structured JSON response:
```json
{
  "urgency": "High",
  "category": "Technical Bug",
  "sentiment": "Angry",
  "drafted_reply": "Hello, I sincerely apologize for the frustration caused by the app crashing during your password reset. I understand you need immediate access for your work. Our technical team is prioritizing this issue right away. In the meantime, please try opening the password reset link using a web browser instead of the mobile app. If you still experience issues, please let us know so we can assist you directly."
}
```

## Demo Video

[https://github.com/user-attachments/assets/c2920926-2066-4f38-b258-b5b75313414c](https://github.com/user-attachments/assets/c2920926-2066-4f38-b258-b5b75313414c)


