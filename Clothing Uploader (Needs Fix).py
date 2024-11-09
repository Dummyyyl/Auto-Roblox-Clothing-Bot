import json
import os
import time
from cleantext import clean
import requests
from colorama import init, Fore, Back

init()

try:
    with open("config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("[ERROR] Configuration file 'config.json' not found. Please ensure it's in the same directory.")
    input()

# Extract variables from config.json
cookie = str(config["auth"]["cookie"])
group = str(config["clothing"]["group"])
description = str(config["clothing"]["description"])
priceconfig = int(config["clothing"]["price"])
ratelimz = int(config["optional"]["ratelimitwaitseconds"])
maxrobux = int(config["optional"]["maxrobuxtospend"])
debugmode = config["optional"].get("debugmode", False)

# Set up path and initialize session for Roblox authentication
path = os.getcwd()
try:
    os.remove(f"{path}/Storage/Clothes/Shirts/deleteme.png")
except FileNotFoundError:
    pass

# Authentication into Roblox account
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
req = session.post(url="https://auth.roblox.com/")
if "X-CSRF-Token" in req.headers:
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

req2 = session.post(url="https://auth.roblox.com/")
try:
    getuser = session.get("https://users.roblox.com/v1/users/authenticated")
    getuser2 = getuser.json()
    getuser3 = getuser2['id']
    getuser4 = getuser2['name']
    print(f"{Back.CYAN}{Fore.BLACK}[Authentication]{Back.BLACK}{Fore.WHITE} Logged in as {getuser4}")
except:
    print(f"{Back.RED}{Fore.BLACK}[Error]{Back.BLACK}{Fore.WHITE} Invalid cookie")
    print(f"{Back.YELLOW}{Fore.BLACK}[Info]{Back.BLACK}{Fore.WHITE} Please restart the program with a valid cookie")
    input()

# Main program setup
brokie = session.get("https://economy.roblox.com/v1/user/currency")
brokie = brokie.json()["robux"]
print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}\n")

assetid = "1"
robuxspent = 0

# Define the function for uploading shirts
def shirts():
    global group, description, priceconfig, assetid, robuxspent, maxrobux

    if robuxspent >= maxrobux:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Max robux spent reached, stopping program")
        input()
        return

    try:
        path = os.getcwd()
        pathz = f"{path}/Storage/Clothes/Shirts"
        name = os.listdir(pathz)[0].split(".")[0]
        name = clean(name, no_emoji=True)
        creator = group
        creatortype = "Group"
    except IndexError:
        print(f"{Back.MAGENTA}{Fore.BLACK}[Shirts]{Back.BLACK}{Fore.WHITE} All shirts uploaded. You may close the program.")
        input()
        return

    # Save config data to JSON format in file
    with open("Storage/Json/config.json", "w") as json_file:
        json.dump({
            "name": name,
            "description": description,
            "creatorTargetId": creator,
            "creatorType": creatortype
        }, json_file)

    # Set link for shirt upload
    link = "https://itemconfiguration.roblox.com/v1/avatar-assets/11/upload"
    files = {
        'media': open(f"{pathz}/{os.listdir(pathz)[0]}", 'rb'),
        'config': open('Storage/Json/config.json', 'rb')
    }
    s = session.post(link, files=files)
    if debugmode:
        print(f"Status: {s.status_code}\nResponse: {s.text}")
    files["media"].close()

    sd = s.json()
    try:
        assetid = sd['assetId']
    except KeyError:
        error_handling(sd, pathz)
        return

    set_price(assetid)

    brokie = session.get("https://economy.roblox.com/v1/user/currency").json()["robux"]
    print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}\n")
    shirts()

def error_handling(sd, pathz):
    code = sd['errors'][0]['code']
    name = os.listdir(pathz)[0].split(".")[0]

    if code == 16 or code == 11:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Invalid name/description, removing: {name}")
    elif code == 8:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Invalid file type, removing: {name}")
    elif code == 0:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Ratelimited. Retrying in {ratelimz}s: {name}")
        time.sleep(ratelimz)
    elif code == 6:
        print(f"{Back.RED}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Insufficient robux to upload: {name}")
        input()
    elif code == 7:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Invalid template, removing: {name}")
    elif code == 9:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Permission denied for group upload.")
    
    os.remove(f"{pathz}/{name}.png")
    shirts()

def set_price(assetid):
    pricefiles = {
        "price": priceconfig,
        "priceConfiguration": {"priceInRobux": priceconfig},
        "saleStatus": "OnSale"
    }
    priceupdate = f"https://itemconfiguration.roblox.com/v1/assets/{assetid}/release"
    price = session.post(priceupdate, json=pricefiles)

    if price.status_code == 200:
        print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully set price to R$ {priceconfig}")
    else:
        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to set price.")

shirts()
