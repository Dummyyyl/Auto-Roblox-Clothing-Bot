# NEXT LINE IS RUN IN Clothing Downloader.py
# This Function will Take the Names (from ClothingD.py) that are given to it in Clothing Downloader.py
# Then it will send it over to the ChatGPT Api and it Returns the 3 most used keywords

import requests
import json

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
            {"role": "system", "content": "You will get Names of Roblox Clothes."
             + "Out of that Create 1-3 Words that are mostly used and only answer that."
             + "Dont use , or any other things like . and they should fit together so dont wite for example 'Emo, Kawaii, Y2K'"
             + "Im talking about for example: Halloween or Hello Kitty or Emo Y2k. Also answer in 3 Different words for example Word1: Emo Y2k Word2: Hello Kitty etc."
             + "And they should fit together so dont combine them like Y2k Hello Kitty or something"},
            {"role": "user", "content": content}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"
