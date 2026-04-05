import json
import datetime
import re
import requests
from bs4 import BeautifulSoup

def get_gas_prices():
    url = "https://www.gasbuddy.com/gasprices/new-york/albany"
    
    # We must use standard browser headers, otherwise GasBuddy will block us immediately
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all text on the page that matches a gas price format (e.g. $3.29)
        prices = []
        for text in soup.stripped_strings:
            if re.match(r'^\$\d\.\d{2}$', text):
                prices.append(float(text.replace('$', '')))
                
        if not prices:
            print("Warning: No prices found. GasBuddy may have blocked the request.")
            return None
            
        # Calculate our numbers based on the scraped prices
        highest = max(prices)
        lowest = min(prices)
        average = round(sum(prices) / len(prices), 2)
        
        return {
            "highest": highest,
            "lowest": lowest,
            "average": average
        }
        
    except Exception as e:
        print(f"Error scraping GasBuddy: {e}")
        return None

if __name__ == "__main__":
    prices = get_gas_prices()
    
    # Only update the JSON file if scraping was successful
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
        print("Scraping failed today. Keeping the old data on the website to prevent crashing.")
