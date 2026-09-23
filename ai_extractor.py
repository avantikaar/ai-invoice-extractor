import os
import json
from google import genai
from dotenv import load_dotenv

# Load the secret key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the new SDK client
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_invoice_data(text):
    prompt = f"""
    You are an AI document parser for an enterprise ERP system. 
    Extract the following fields from this invoice text. 
    Return ONLY a valid JSON object with these exact keys: 
    "vendor_name", "invoice_number", "invoice_date", "total_amount".
    If a field is missing, put null. Do not write any markdown or extra text.
    
    Invoice Text:
    {text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        data = json.loads(clean_text)
        return data
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return None