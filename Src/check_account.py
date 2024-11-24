import requests
import json
from Src.Send_to_Discord import error_log

def check_cookie():
    with open('config.json', 'r') as f:
        cookie = json.load(f)["auth"]["cookie"]

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    req = session.post("https://auth.roblox.com/")

    if "X-CSRF-Token" in req.headers:
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

    try:
        user_info = session.get("https://users.roblox.com/v1/users/authenticated").json()
        if not user_info.get("id"):
            raise Exception("Invalid login")
    except:
        error_log("Failed to log in with the provided cookie.")

if __name__ == "__main__":
    check_cookie()
