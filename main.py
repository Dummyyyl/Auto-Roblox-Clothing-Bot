from Src.Send_to_Discord import group_sale_notifier, upload_log, status_log
from Src.Clothing_Downloader import download_clothing
from Src.Uploader_Test import upload_clothing
from Src.Check_Account import check_cookie
from datetime import datetime
import time
import json
import os
import threading

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Configuration and state
full_path = config["optional"]["shirt_folder"]
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}
last_run = None
upload_in_progress = False
check_cookie_interval = 60

# Log the initial status
status_log("🔄 **The Program is now running.**")

# Run group_sale_notifier in a separate thread
def run_group_sale_notifier():
    group_sale_notifier()

notifier_thread = threading.Thread(target=run_group_sale_notifier, daemon=True)
notifier_thread.start()

# Main loop
last_check_cookie_time = time.time()  # Track the last time check_cookie was called

while True:
    current_time = datetime.now().strftime("%H:%M")
    current_time_seconds = time.time()

    # Check if it's time to run the check_cookie function
    if current_time_seconds - last_check_cookie_time >= check_cookie_interval:
        check_cookie()  # Run check_cookie every few minutes
        last_check_cookie_time = current_time_seconds  # Update the last check time

    # Run download_clothing at the specified time
    if current_time == "16:30" and (last_run is None or last_run.date() != datetime.now().date()):
        status_log("🔄 **The Program is still running.**")
        download_clothing()
        last_run = datetime.now()

    # Upload clothing if there are images in the folder
    elif os.path.isdir(full_path) and any(file.lower().endswith(ext) for ext in image_extensions for file in os.listdir(full_path)) and not upload_in_progress:
        upload_in_progress = True
        upload_clothing()
        upload_in_progress = False
    
    time.sleep(5)
