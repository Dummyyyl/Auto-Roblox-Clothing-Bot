import requests
import os
import json
import re
from PIL import Image
from colorama import init
from Ai_Filter import getFilterWord
from GetKeyWord import fetch_titles
from Send_to_Discord import error_log
import random

def download_clothing():
    print("Running... please wait 20-30 Seconds")

    # Define the file path
    file_path = r"C:\Users\MarkusEisenmann\Documents\Code\Clothing Bot\Auto-Roblox-Clothing-Bot\Storage\Clothes\Shirts\Deleteme.png"

    # Attempt to delete the file
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")

    result = fetch_titles()
    if result:
        response = getFilterWord(result)

        # Use a regular expression to match the format "WordX: Keyword"
        matches = re.findall(r'Word\d+: (.+?)(?=$|\sWord\d+:)', response)
        
        # Assign the keywords to variables (ensure we handle cases where there are fewer than 3 matches)
        keyword1 = matches[0] if len(matches) > 0 else None
        keyword2 = matches[1] if len(matches) > 1 else None
        keyword3 = matches[2] if len(matches) > 2 else None
    else:
        error_log("No Keywords found or failed to fetch data.")
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
    download_amount = config["optional"]["download_amount"]
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
    except:
        error_log("Invalid cookie. Please check your credentials.")
        exit()

    # Define the keywords to search
    keywords = [keyword1, keyword2, keyword3]
    cltype = "Shirts"

    # Define URL template to search for clothing items, allowing us to replace `{}` with each keyword
    base_url_template = "https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={}&limit=120&maxPrice=5&minPrice=5&salesTypeFilter=1&subcategory=ClassicShirts"
               
    # Function to sanitize filenames
    def sanitize_filename(name):
        return ''.join(char for char in name if char.isalnum() or char in " -_.()")

    used_clothing_ids = set()

    # Loop through each keyword and download up to `download_amount` items for each
    for keyword in keywords:
        if keyword:
            api_url = base_url_template.format(keyword.replace(" ", "+").lower())
            
            # Fetch a batch of clothing items
            response = session.get(api_url)
            data = response.json()
            clothing_ids = [item["id"] for item in data.get("data", [])]

            if not clothing_ids:
                error_log(f"No clothing IDs found for keyword '{keyword}'.")
                continue  # Skip to the next keyword if no IDs are found

            # Initialize a counter for successfully downloaded items
            downloaded_items = 0

            # Randomly pick clothing IDs until we reach `download_amount`
            while downloaded_items < download_amount:
                if len(used_clothing_ids) == len(clothing_ids):
                    error_log(f"All IDs for keyword '{keyword}' have been used.")
                    break  # Stop if all clothing IDs have already been used

                # Randomly select an ID that hasn't been used yet
                clothing_id = random.choice(clothing_ids)
                while clothing_id in used_clothing_ids:
                    clothing_id = random.choice(clothing_ids)  # Retry until a new ID is found

                # Mark the ID as used
                used_clothing_ids.add(clothing_id)

                try:
                    # Download XML to extract image ID
                    xml_url = f"https://assetdelivery.roblox.com/v1/asset/?id={clothing_id}"
                    xml_response = session.get(xml_url)
                    if xml_response.status_code != 200:
                        error_log(f"Failed to download XML for ID {clothing_id}")
                        continue

                    # Extract image ID from XML
                    xml_content = xml_response.text
                    match = re.search(r'<url>.*\?id=(\d+)</url>', xml_content)
                    if not match:
                        error_log(f"Could not find image ID in XML for {clothing_id}")
                        continue
                    image_id = match.group(1)

                    # Get item name and sanitize it for filename
                    name_response = session.get(f"https://economy.roblox.com/v2/assets/{image_id}/details")
                    name = name_response.json().get("Name", f"Item_{clothing_id}")
                    filename = sanitize_filename(name)

                    # Split the keyword into individual words and check if any of the words are in the item name
                    keyword_words = set(keyword.lower().split())  # Split and convert to set for uniqueness
                    name_words = set(name.lower().split())  # Split and convert to set for comparison

                    # Check if at least one word in the keyword is found in the item name
                    if not keyword_words.intersection(name_words):
                        print(f"Skipping '{name}' as no keyword words are found.")
                        continue  # Skip this item if no keyword word is found

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

                    # Increment the downloaded items counter
                    downloaded_items += 1

                except Exception as e:
                    error_log(f"Error processing ID {clothing_id}: {e}")

            print(f"Downloaded {downloaded_items} items for keyword '{keyword}'.")

    # Clear the used IDs set after the run
    used_clothing_ids.clear()
    print(f"Temporary used ID list cleared. Ready for the next run.")

    print(f"Downloaded and processed items for keywords: {', '.join(filter(None, keywords))}")

