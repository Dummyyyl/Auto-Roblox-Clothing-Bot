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
    # Get the name of the clothing image from the clipboard
    partial_name = pyperclip.paste().strip()
    
    # Get a list of all files in the directory
    files_in_directory = os.listdir(full_path)
    
    # Find a file that contains the clipboard content (case-insensitive match)
    matching_files = [file for file in files_in_directory if partial_name.lower() in file.lower()]
    
    if matching_files:
        for matching_file in matching_files:
            file_path = os.path.join(full_path, matching_file)
            try:
                # Delete the matching file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"No file matching '{partial_name}' found in the directory.")
        


        
#--------------------------- Uploader ---------------------------

# Open the site
open_uploadlink(url)

time.sleep(5)

# Now, continuously check for the target image on the screen
while True:
    position1 = find_image_on_screen(upload_button_path)
    # Move to Upload Button
    if position1:
        move_mouse_to_target(position1)
        pyautogui.click()
        time.sleep(2)
        
        # Move to the Path in the Explorer
        position2 = find_image_on_screen(navigate_path)
        move_mouse_to_target(position2)

        # Copy the Path
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)

        # Get the current path from clipboard
        current_path = pyperclip.paste()
        
        # Compare with the desired full path
        if current_path == full_path:
            print("Path matches the desired path. Pressing ESC...")
            pyautogui.press('esc')
        else:
            print(f"Current path ({current_path}) does not match. Setting to desired path...")
            pyperclip.copy(full_path)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('enter')
            time.sleep(0.1)

        find_image1 = find_image_on_screen(first_image_path)
        find_image2 = find_image_on_screen(find_image_path)
        find_image3 = find_image_on_screen(find_image_backup_path)
        if find_image1:
            move_mouse_to_target(find_image1)
        elif find_image2:
            move_mouse_to_target(find_image2)
        else:
            move_mouse_to_target(find_image3)
        current_x, current_y = pyautogui.position()
        pixels_to_move_down = 150  # Change this value as needed
        pyautogui.moveTo(current_x, current_y + pixels_to_move_down, duration=0.1)

        time.sleep(0.2)
        pyautogui.doubleClick()
        
        time.sleep(0.)
        
        # Move to the Name Field
        position4 = find_image_on_screen(name_field_path)
        position5 = find_image_on_screen(name_field_inputted_path)
        if position4:
            move_mouse_to_target(position4)
        else:
            move_mouse_to_target(position5)
        time.sleep(0.2)  # Delay to ensure it's ready for input

        # Copy the Name
        pyautogui.doubleClick()
        time.sleep(0.01)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.01)
        pyautogui.hotkey('ctrl', 'c')

        # Delete Image from Name in clipboard
        name_delete = pyperclip.paste()
        delete_clothing_image()

        # Move to the Description Field
        position6 = find_image_on_screen(description_field_path)
        move_mouse_to_target(position6)
        time.sleep(0.5)  # Edit delay
            
        # Paste the Description
        pyperclip.copy(str(description))
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'v')

        # Scroll Down
        time.sleep(0.2)
        pyautogui.scroll(-500)
        time.sleep(0.2)

        # Move to the Upload field and Upload It
        position7= find_image_on_screen(upload_to_roblox)
        move_mouse_to_target(position7)
        pyautogui.click()
        
        position8 = find_image_on_screen(final_upload_path)
        move_mouse_to_target(position8)
        

        break  # Exit the loop once the target is found and actions are performed
    
    time.sleep(1)  # Check every second
