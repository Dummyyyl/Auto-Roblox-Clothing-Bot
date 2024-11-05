import requests
import os
import json
import re
from PIL import Image
from colorama import init
from Ai_Filter import getFilterWord
from GetKeyWord import fetch_titles

print("Running... please wait 20-30 Seconds")
# Call the function and retrieve keywords
result = fetch_titles()
if result:
    response = getFilterWord(result)
    
    # Split the response by lines to get each keyword
    lines = response.splitlines()
    keyword1 = lines[0].split(": ", 1)[1] if len(lines) > 0 else None
    keyword2 = lines[1].split(": ", 1)[1] if len(lines) > 1 else None
    keyword3 = lines[2].split(": ", 1)[1] if len(lines) > 2 else None
else:
    print("No paid titles found or failed to fetch data.")
    exit()

# Initialize colorama
init()

# Load configuration from JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

cookie = config["auth"]["cookie"]
templatechanger = config["optional"]["templatechanger"]
debugmode = config["optional"]["debugmode"]
ratelimitwaitseconds = config["optional"]["ratelimitwaitseconds"]
maxrobuxtospend = config["optional"]["maxrobuxtospend"]
price = config["clothing"]["price"]
group = config["clothing"]["group"]
description = config["clothing"]["description"]

# Set up session with cookie and CSRF token
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
req = session.post("https://auth.roblox.com/")
if "X-CSRF-Token" in req.headers:
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

# Check authentication
try:
    user_info = session.get("https://users.roblox.com/v1/users/authenticated").json()
    user_id = user_info['id']
    user_name = user_info['name']
    print(f"Logged in as {user_name}")
except:
    print("Invalid cookie. Please check your credentials.")
    exit()

# Define the keywords to search
keywords = [keyword1, keyword2, keyword3]
cltype = "Shirts"

# Define URL template to search for clothing items, allowing us to replace `{}` with each keyword
base_url_template = "https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&subcategory=ClassicShirts"

# Function to sanitize filenames
def sanitize_filename(name):
    return ''.join(char for char in name if char.isalnum() or char in " -_.()")

# Loop through each keyword and download up to 3 items for each
for keyword in keywords:
    if keyword:
        api_url = base_url_template.format(keyword.replace(" ", "+").lower())
        
        # Collect clothing IDs from search results for each keyword, limit to 3 items
        response = session.get(api_url)
        data = response.json()
        clothing_ids = [item["id"] for item in data.get("data", [])][:3]  # Limit to 3 items per keyword

        print(f"Collecting IDs for keyword '{keyword}': {clothing_ids}")

        # Download and process each clothing item for the keyword
        for clothing_id in clothing_ids:
            try:
                # Download XML to extract image ID
                xml_url = f"https://assetdelivery.roblox.com/v1/asset/?id={clothing_id}"
                xml_response = session.get(xml_url)
                if xml_response.status_code != 200:
                    print(f"Failed to download XML for ID {clothing_id}")
                    continue

                # Extract image ID from XML
                xml_content = xml_response.text
                match = re.search(r'<url>.*\?id=(\d+)</url>', xml_content)
                if not match:
                    print(f"Could not find image ID in XML for {clothing_id}")
                    continue
                image_id = match.group(1)

                # Get item name and sanitize it for filename
                name_response = session.get(f"https://economy.roblox.com/v2/assets/{image_id}/details")
                name = name_response.json().get("Name", f"Item_{clothing_id}")
                filename = sanitize_filename(name)

                # Download the clothing image
                img_url = f"https://assetdelivery.roblox.com/v1/asset/?id={image_id}"
                img_response = session.get(img_url)
                if img_response.status_code != 200 or len(img_response.content) < 7500:
                    print(f"Failed to download or image too small for ID {clothing_id}")
                    continue

                # Save image
                folder = f"Storage/Clothes/{cltype}"
                os.makedirs(folder, exist_ok=True)
                img_path = os.path.join(folder, f"{filename}.png")
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Downloaded {filename}")

                # Apply template overlay if enabled
                if templatechanger:
                    img = Image.open(img_path)
                    template = Image.open(f"Storage/Json/{cltype.lower()}.png")
                    img.paste(template, (0, 0), template)
                    img.save(img_path)
                    print(f"Applied template to {filename}")

            except Exception as e:
                print(f"Error processing ID {clothing_id}: {e}")

print(f"Downloaded and processed items for keywords: {', '.join(keywords)}")
