from Send_to_Discord import group_sale_notifier, upload_log, status_log
from Clothing_Downloader import download_clothing
from UploaderTest import upload_clothing
from datetime import datetime
import threading
import time
import json
import os

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Configuration and state
full_path = config["optional"]["shirt_folder"]
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}
last_run = None
upload_in_progress = False

# Log the initial status
status_log("🔄 **The Program is now running.**")

# Run group_sale_notifier in a separate thread
def run_group_sale_notifier():
    group_sale_notifier()

notifier_thread = threading.Thread(target=run_group_sale_notifier, daemon=True)
notifier_thread.start()

# Main loop
while True:
    current_time = datetime.now().strftime("%H:%M")
    if current_time == "00:07" and (last_run is None or last_run.date() != datetime.now().date()):
        status_log("🔄 **The Program is still running.**")
        download_clothing()
        last_run = datetime.now()
    
    elif os.path.isdir(full_path) and any(file.lower().endswith(ext) for ext in image_extensions for file in os.listdir(full_path)) and not upload_in_progress:
        upload_in_progress = True
        upload_clothing()
        upload_in_progress = False
    else:
        print("tested")
    
    time.sleep(5)
