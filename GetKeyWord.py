# This Code gets the top 20 best sold shirts in the last week
# Then it saves the names of them in the function fech_titles
# Then it will give it over to Clothing Downloader.py


import requests
import json

def fetch_titles():
    # Load configuration from JSON file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Extract specific configurations
    cookie = config["auth"]["cookie"]

    # Set up session with cookie
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    # Set up session with CSRF token for authentication
    req = session.post("https://auth.roblox.com/")
    if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

    # Check authentication
    try:
        user_info = session.get("https://users.roblox.com/v1/users/authenticated").json()
        if user_info.get("id") is None:
            print("Authentication failed. Please check your cookie.")
            return None
    except Exception as e:
        print(f"Error checking authentication: {e}")
        return None

    # Define the API URL for the top 120 bestselling shirts this week
    shirts_url = "https://catalog.roblox.com/v1/search/items?category=Clothing&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&sortAggregation=3&sortType=2&subcategory=ClassicShirts"

    # Initialize variables to hold titles
    paid_titles = []

    # Fetch data from the shirts URL
    response = session.get(shirts_url)
    data = response.json()

    if 'data' in data and data['data']:
        # Collect asset IDs
        asset_ids = [item['id'] for item in data['data']]
        
        # Fetch details for each asset ID
        for asset_id in asset_ids:
            details_url = f"https://economy.roblox.com/v2/assets/{asset_id}/details"
            details_response = session.get(details_url)
            details_data = details_response.json()
            
            # Check if 'Name' exists and 'PriceInRobux' is not None or 0
            price_in_robux = details_data.get('PriceInRobux')
            if 'Name' in details_data:
                title = details_data['Name']
                if price_in_robux not in [None, 0]:
                    paid_titles.append(title)
                
                # Stop once we have 20 paid titles
                if len(paid_titles) == 20:
                    break

    # Return the list of paid titles joined by commas
    return ", ".join(paid_titles) if len(paid_titles) == 20 else None
