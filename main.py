from Send_to_Discord import group_sale_notifier, upload_log, error_log, status_log
from Clothing_Downloader import download_clothing
from UploaderTest import upload_clothing
from datetime import datetime
import time
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

full_path = config["optional"]["shirt_folder"]
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}

status_log()

last_run = None

# Flag to track if upload is in progress
upload_in_progress = False

while True:
    current_time = datetime.now().strftime("%H:%M")
    
    # Check if it's time to download clothing and run the function
    if current_time == "10:48" and (last_run is None or last_run.date() != datetime.now().date()):
        status_log()
        download_clothing()
        last_run = datetime.now()
    
    elif os.path.isdir(full_path) and any(file.lower().endswith(ext) for ext in image_extensions for file in os.listdir(full_path)) and not upload_in_progress:
        upload_in_progress = True
        upload_clothing()
        upload_in_progress = False
    
    time.sleep(5)
