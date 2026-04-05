import os
import json
import datetime
from google import genai
from google.genai import types

def get_gas_prices():
    # Grab the API key we hid in GitHub Secrets
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY is missing!")
        return None

    # Initialize the NEW 2026 Google GenAI Client
    client = genai.Client(api_key=api_key)
    
    prompt = (
        "What are the current estimated highest, lowest, and average regular gas prices in Albany, NY? "
        "Use your search knowledge to provide realistic current figures. "
        "Return the data using this exact JSON schema: "
        "{'highest': float, 'lowest': float, 'average': float}"
    )
    
    try:
        print("Asking Gemini for Albany gas prices...")
        
        # Use the newest, actively supported free-tier model (Gemini 2.5 Flash)
        # Force Gemini to respond ONLY with valid JSON
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Parse the JSON response provided by Gemini
        prices = json.loads(response.text)
        
        # Ensure the numbers are rounded to 2 decimal places like money
        return {
            "highest": round(float(prices["highest"]), 2),
            "lowest": round(float(prices["lowest"]), 2),
            "average": round(float(prices["average"]), 2)
        }
        
    except Exception as e:
        print(f"Error fetching data from Gemini: {e}")
        return None

if __name__ == "__main__":
    prices = get_gas_prices()
    
    if prices:
        now = datetime.datetime.now().strftime("%B %d, %Y")

        data = {
            "location": "Albany, NY",
            "date": now,
            "prices": prices
        }

        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
            
        print(f"Successfully updated data.json with new Albany prices: {prices}")
    else:
        print("Failed to get data today. Keeping the old data on the website to prevent crashing.")
