from requests import get, post
from time import sleep, time
from datetime import datetime
import json
import requests

with open('config.json', 'r') as f:
    config = json.load(f)


cookie = config["auth"]["cookie"]
groupID = config["clothing"]["group"]
error_webhook = config["auth"]["error_webhook"]
upload_webhook = config["auth"]["upload_webhook"]
sale_webhook = config["auth"]["sale_webhook"]
status_webhook = config["auth"]["status_webhook"]

wait = 5
timeout = 10
pastids = []


def error_log(error_description):
    data = {
        "username": "Error Log",  # Replace with your desired webhook name
        "embeds": [
            {
                "title": "Error:",  # Title of the embed
                "description": error_description,  # Description
                "color": 0xFF0000,  # Red color (Hex: #FF0000)
            }
        ]
    }
    requests.post(error_webhook, json=data)


def upload_log(error):
    data = {
        "username": "Upload Log",  # Replace with your desired webhook name
        "embeds": [
            {
                "title": "Clothing Uploaded:",  # Title of the embed
                "description": error,  # Description
                "color": 0x00FF00,  # Red color (Hex: #FF0000)
            }
        ]
    }
    requests.post(upload_webhook, json=data)

def status_log():
    data = {
        "content": None,
        "embeds": [
            {
                "description": "🔄 **The Group Sale Notifier is now tracking group sales. Enjoy!**",
                "color": 0x0000FF,
                "author": {"name": "🚀 Program Loaded", "icon_url": "https://avatars.githubusercontent.com/u/99405955?v=4"},
                "footer": {"text": "Status: ONLINE", "icon_url": "https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png"},
                "thumbnail": {"url": "https://cdn-icons-png.flaticon.com/512/5537/5537993.png"}
            }
        ]
    }
    requests.post(status_webhook, json=data)





def log(text):
    print(f"[{datetime.utcfromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")

def profilePicture(id):
    try:
        r = get(f'https://www.roblox.com/users/{id}/profile').text
        return r.split('<meta property="og:image" content="')[1].split('"')[0]
    except:
        return 'https://tr.rbxcdn.com/af0be829bc4349c0b116ae36843a0a91/150/150/AvatarHeadshot/Png'

def group_sale_notifier():
    # Fetch initial pending Robux
    r = get(f'https://economy.roblox.com/v1/groups/{groupID}/revenue/summary/day', cookies={'.ROBLOSECURITY': cookie})
    pastpending = r.json().get('pendingRobux', 0)

    # Load past transaction hashes
    response = get(f'https://economy.roblox.com/v2/groups/{groupID}/transactions?cursor=&limit=10&transactionType=Sale', cookies={'.ROBLOSECURITY': cookie})
    for purchase in response.json().get('data', []):
        pastids.append(purchase['idHash'])

    log(f"Loaded with {len(pastids)} past hashes.")

    try:
        post(sale_webhook, json={
            "content": None,
            "embeds": [{
                "description": "🔄 **The Group Sale Notifier is now tracking group sales. Enjoy!**",
                "color": 0x0000FF,
                "author": {"name": "🚀 Program Loaded", "icon_url": "https://avatars.githubusercontent.com/u/99405955?v=4"},
                "footer": {"text": "Status: ONLINE", "icon_url": "https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png"},
                "thumbnail": {"url": "https://cdn-icons-png.flaticon.com/512/5537/5537993.png"}
            }]
        })
    except Exception as e:
        log(f'Failed to send notification: {e}')

    while True:
        try:
            # Fetch the current pending Robux
            r = get(f'https://economy.roblox.com/v1/groups/{groupID}/revenue/summary/day', cookies={'.ROBLOSECURITY': cookie})
            nowpending = r.json().get('pendingRobux', pastpending)

            if nowpending > pastpending:
                response = get(f'https://economy.roblox.com/v2/groups/{groupID}/transactions?cursor=&limit=10&transactionType=Sale', cookies={'.ROBLOSECURITY': cookie})
                for purchase in response.json().get('data', []):
                    if purchase['idHash'] not in pastids:
                        pastpending = nowpending
                        pastids.append(purchase['idHash'])
                        pfp = profilePicture(purchase['agent']['id'])
                        post(sale_webhook, json={
                            "content": None,
                            "embeds": [{
                                "title": ":shopping_cart: Group Sale",
                                "description": f"**[{purchase['agent']['name']}](https://www.roblox.com/users/{purchase['agent']['id']}/profile)** spent **{purchase['currency']['amount']} ⏣** on `{purchase['details']['name']}`",
                                "color": 0xFFD700,
                                "author": {"name": "💸 New Group Sale"},
                                "thumbnail": {"url": pfp},
                            }]
                        })

            sleep(wait)
        except Exception as e:
            log(f'[ERROR] {e}')
            sleep(timeout)