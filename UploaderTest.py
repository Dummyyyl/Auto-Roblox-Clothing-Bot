#--------------------------- Imports ---------------------------

import webbrowser
import pyautogui
import cv2
import numpy as np
import time
import pyperclip
from pathlib import Path
import json
import os
import random

#--------------------------- Variables ---------------------------

with open('config.json', 'r') as f:
    config = json.load(f)

description = config["clothing"]["description"]
groupID = config["clothing"]["group"]

file_to_delete = None
full_path = r"C:\Users\MarkusEisenmann\Documents\Code\Auto-Roblox-Clothing-Bot-main\Auto-Roblox-Clothing-Bot-main\Storage\Clothes\Shirts"
url = f"https://create.roblox.com/dashboard/creations/upload?assetType=Shirt&groupId={groupID}"

# Variables for the CV Path
upload_button_path = "Storage\OpenCVPic\\upload_button_cv.png"
navigate_path = "Storage\OpenCVPic\\navigate_folder.png"
name_field_path = "Storage\OpenCVPic\\name_field.png"
name_field_inputted_path = "Storage\OpenCVPic\\name_field_inputted.png"
description_field_path = "Storage\OpenCVPic\\description_field.png"
upload_to_roblox = "Storage\OpenCVPic\\upload_to_roblox.png"
find_image_path = "Storage\OpenCVPic\\find_image.png"
find_image_backup_path = "Storage\OpenCVPic\\find_image_backup.png"
first_image_path = "Storage\OpenCVPic\\first_find_image.png"
final_upload_path = "Storage\OpenCVPic\\final_upload.png"
file_name = "Storage\OpenCVPic\\file_name_field.png"
choose_picture = "Storage\OpenCVPic\\choose_picture.png"

#--------------------------- Functions ---------------------------

# Function to open the link in the default web browser
def open_uploadlink(link):
    webbrowser.open(link)

# Function to find a target image on the screen
def find_image_on_screen(image_path, confidence=0.8):
    # Take a screenshot and convert it to a format OpenCV can work with
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load the target image
    target = cv2.imread(image_path)
    if target is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Perform template matching to find the target image on the screen
    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the best match exceeds the confidence threshold
    if max_val >= confidence:
        target_height, target_width = target.shape[:2]
        center_x = max_loc[0] + target_width // 2
        center_y = max_loc[1] + target_height // 2
        return (center_x, center_y)
    else:
        return None

# Function to move the mouse to the target position
def move_mouse_to_target(target_position):
    if target_position:
        pyautogui.moveTo(target_position[0], target_position[1], duration=0.1)
        print(f"Mouse moved to position: {target_position}")
    else:
        print("Target not found on the screen.")
        
        
        
# Function to delete an image file based on partial name match
def delete_clothing_image():
    partial_name = pyperclip.paste().strip()
    files_in_directory = os.listdir(full_path)
    matching_files = [file for file in files_in_directory if partial_name.lower() in file.lower()]
    
    if matching_files:
        # Delete only the first matching file
        file_path = os.path.join(full_path, matching_files[0])
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"No file matching '{partial_name}' found in the directory.")

        
# Function to wait until an image is found on the screen
def wait_for_image(image_path, confidence=0.8, timeout=30):
    start_time = time.time()
    while True:
        position = find_image_on_screen(image_path, confidence)
        if position:
            return position
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout while waiting for image: {image_path}")
        time.sleep(0.1)  # Avoid excessive CPU usage
        

#--------------------------- Uploader ---------------------------

# Open the site
open_uploadlink(url)

# Continuously check for the target images and perform actions
try:
    # # Wait for the Upload button and click
    # position1 = wait_for_image(upload_button_path)
    # move_mouse_to_target(position1)
    # pyautogui.click()

    # # Wait for the file explorer navigation path
    # position2 = wait_for_image(navigate_path)
    # move_mouse_to_target(position2)
    # pyautogui.click()
    # time.sleep(0.1)
    # pyautogui.hotkey('ctrl', 'c')  # Copy the path from file explorer
    # time.sleep(0.1)
    
    # # Get the current path from clipboard and compare
    # current_path = pyperclip.paste()
    # if current_path == full_path:
    #     print("Path matches the desired path. Pressing ESC...")
    #     pyautogui.press('esc')
    # else:
    #     print(f"Current path ({current_path}) does not match. Setting to desired path...")
    #     pyperclip.copy(full_path)
    #     pyautogui.hotkey('ctrl', 'v')
    #     pyautogui.press('enter')
    
    # # Wait for one of the target images in the file explorer and double click
    # position = None
    # for image_path in [first_image_path, find_image_path, find_image_backup_path]:
    #     position = find_image_on_screen(image_path)
    #     if position:
    #         move_mouse_to_target(position)
    #         break
    # if not position:
    #     raise FileNotFoundError("None of the target images were found in the file explorer.")
    
    # current_x, current_y = pyautogui.position()
    # pyautogui.moveTo(current_x, current_y + 150, duration=0.1)  # Adjust position down
    # pyautogui.click()

    # # Wait for the Name field and copy its contents
    # position4 = wait_for_image(file_name)
    # move_mouse_to_target(position4)
    # pyautogui.click()
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('ctrl', 'c')

    # # Store the filename in a variable
    # file_to_delete = pyperclip.paste().strip()
    # print(f"File to delete: {file_to_delete}")
    
    # # Choose Picture
    # position5 = wait_for_image(choose_picture)
    # move_mouse_to_target(position5)
    # pyautogui.click()
    
    # # Wait for the Description field and paste the description
    # position6 = wait_for_image(description_field_path)
    # move_mouse_to_target(position6)
    # pyautogui.click()
    # pyperclip.copy(str(description))
    # pyautogui.hotkey('ctrl', 'v')
    
    # # Scroll down and click the Upload button
    # time.sleep(0.1)
    # position7 = wait_for_image(upload_to_roblox)
    # move_mouse_to_target(position7)
    # pyautogui.click()
    # time.sleep(0.2)

    # # Wait for the final upload button and click
    # position8 = wait_for_image(final_upload_path)
    # move_mouse_to_target(position8)
    # pyautogui.click()
    
    time.sleep(5)
    open_uploadlink("https://create.roblox.com/dashboard/creations?activeTab=TShirt&groupId=16240463&filterIndex=1")
    
    

except TimeoutError as e:
    print(f"Error: {e}")
finally:
    # Delete the clothing image based on the stored variable
    print(file_to_delete)
    pyperclip.copy(file_to_delete)
    delete_clothing_image()
    file_to_delete = None
    print("Cleared the file_to_delete variable.")
