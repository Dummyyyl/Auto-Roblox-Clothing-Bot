# NEXT LINE IS RUN IN Clothing Downloader.py
# This Function will Take the Names (from GetKeyWord.py) that are given to it in Clothing Downloader.py
# Then it will send it over to the ChatGPT Api and it Returns the 3 most used keywords

import requests
import json
from datetime import datetime

today_date = datetime.today().strftime("%B %d, %Y")

with open('config.json', 'r') as f:
    config = json.load(f)

api_token = config["auth"]["api_key"]

headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

def getFilterWord(content):
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You will get Names of Roblox Clothes. Out of that, create 1-3 words that are mostly used, and only answer that. "
                    "Don't use commas or periods, and the words should fit together, like 'Emo Y2k' or 'Hello Kitty'. "
                    "Do not combine mismatched themes, such as 'Y2k Hello Kitty'. Answer in three different words, like: "
                    "Word1: Emo Y2k Word2: Hello Kitty, etc. "
                    "Consider the season or upcoming holidays for relevance. But only if its mentioned."
                    f"Today is {today_date}."
                )
            },
            {
                "role": "user",
                "content": content
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"
