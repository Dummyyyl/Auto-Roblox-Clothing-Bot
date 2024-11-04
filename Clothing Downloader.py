import requests
import os
import json
import re  # Importing the re module for regular expressions
from PIL import Image
from colorama import init
import emoji

# Initialize colorama
init()

# Load configuration from JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Extract specific configurations
cookie = config["auth"]["cookie"]
templatechanger = config["optional"]["templatechanger"]
debugmode = config["optional"]["debugmode"]
ratelimitwaitseconds = config["optional"]["ratelimitwaitseconds"]
maxrobuxtospend = config["optional"]["maxrobuxtospend"]
price = config["clothing"]["price"]
group = config["clothing"]["group"]
description = config["clothing"]["description"]

# Set up session with cookie
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie

# Set up session with CSRF token for authentication
req = session.post("https://auth.roblox.com/")
if "X-CSRF-Token" in req.headers:
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

try:
    user_info = session.get("https://users.roblox.com/v1/users/authenticated").json()
    user_id = user_info['id']
    user_name = user_info['name']
    print(f"Logged in as {user_name}")
except:
    print("Invalid cookie. Please check your credentials.")
    exit()

# Prompt for clothing type and keyword input
cltype = input("Enter clothing type (Shirts or Pants): ").strip().lower()
if cltype in ["s", "shirts", "shirt"]:
    cltype = "Shirts"
elif cltype in ["p", "pants", "pant"]:
    cltype = "Pants"
else:
    print("Invalid clothing type input. Exiting.")
    exit()
keywords = input("Enter keywords for search (e.g., emo goth y2k): ").strip().replace(" ", "+").lower()

# Define API endpoints for different sorting methods
base_url = f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keywords}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&subcategory=Classic{cltype}"
sort_options = {
    "1": base_url,
    "2": f"{base_url}&sortAggregation=5&sortType=1",
    "3": f"{base_url}&sortAggregation=3&sortType=1",
    "4": f"{base_url}&sortAggregation=5&sortType=1",
    "5": f"{base_url}&sortAggregation=5&sortType=2",
    "6": f"{base_url}&sortAggregation=3&sortType=2",
    "7": f"{base_url}&sortAggregation=1&sortType=1",
    "8": f"{base_url}&sortType=3"
}

# Prompt for sorting method
print("Catalog Sorts\n-[1] Relevance\n-[2] Most Favourited (all time)\n-[3] Most Favourited (past week)\n-[4] Most Favourited (past day)")
print("-[5] Bestselling (all time)\n-[6] Bestselling (weekly)\n-[7] Bestselling (past day)\n-[8] Recently Updated")
sortby = input("Choose a sort option (1-8): ").strip()
api_url = sort_options.get(sortby)
if not api_url:
    print("Invalid sort option selected. Exiting.")
    exit()

# Collect clothing IDs from search results
clothing_ids = []
page_count = 0
while True:
    response = session.get(api_url)
    data = response.json()
    page_ids = [item["id"] for item in data.get("data", [])]
    if not page_ids:
        print("No more results found or an error occurred.")
        break
    clothing_ids.extend(page_ids)
    next_cursor = data.get("nextPageCursor")
    if not next_cursor:
        break
    api_url = f"{api_url}&cursor={next_cursor}"
    page_count += 1

print(f"Collected {len(clothing_ids)} IDs over {page_count} pages")

# Function to sanitize filenames
def sanitize_filename(name):
    return ''.join(char for char in name if char.isalnum() or char in " -_.()")

# Download and process each clothing item
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

print(f"Downloaded and processed {len(clothing_ids)} items.")
