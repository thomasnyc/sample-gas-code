import json
import datetime
import random

def get_gas_prices():
    """
    To use real data, sign up for a free tier gas API (like CollectAPI) 
    and replace this block with your requests/API fetching logic.
    """
    # Generating realistic simulated prices for Albany, NY
    base_price = round(random.uniform(3.20, 3.50), 2)
    return {
        "highest": round(base_price + random.uniform(0.20, 0.40), 2),
        "lowest": round(base_price - random.uniform(0.10, 0.20), 2),
        "average": base_price
    }

if __name__ == "__main__":
    prices = get_gas_prices()
    now = datetime.datetime.now().strftime("%B %d, %Y")

    data = {
        "location": "Albany, NY",
        "date": now,
        "prices": prices
    }

    # Overwrite the data.json file with today's new prices
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
        
    print("Successfully updated data.json with new Albany prices.")
