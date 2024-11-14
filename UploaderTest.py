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

#--------------------------- Variables ---------------------------

with open('config.json', 'r') as f:
    config = json.load(f)

description = config["clothing"]["description"]
groupID = config["clothing"]["group"]

full_path = r"C:\Users\MarkusEisenmann\Documents\Code\Auto-Roblox-Clothing-Bot-main\Auto-Roblox-Clothing-Bot-main\Storage\Clothes\Shirts"
url = f"https://create.roblox.com/dashboard/creations/upload?assetType=Shirt&groupId={groupID}"

# Variables for the CV Path
upload_button_path = "Storage\OpenCVPic\\upload_button_cv.png"
navigate_path1 = "Storage\OpenCVPic\\navigate_folder1.png"
name_field_path = "Storage\OpenCVPic\\name_field.png"
description_field_path = "Storage\OpenCVPic\\description_field.png"
upload_to_roblox = "Storage\OpenCVPic\\upload_to_roblox.png"

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
        position2 = find_image_on_screen(navigate_path1)
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

        # Select image to upload

        # DELETE THIS WHEN DONE
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'f4')
        
        # Move to the Name Field
        position4 = find_image_on_screen(name_field_path)
        move_mouse_to_target(position4)
        time.sleep(1)  # Delay to ensure it's ready for input

        # Copy the Name
        pyautogui.click()
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')

        # Delete Image from Name in clipboard

        # Move to the Description Field
        position5 = find_image_on_screen(description_field_path)
        move_mouse_to_target(position5)
        time.sleep(0.5)  # Edit delay
            
        # Paste the Description
        pyperclip.copy(str(description))
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'v')

        # Scroll Down
        time.sleep(0.2)
        pyautogui.scroll(-500)

        # Move to the Upload field and Upload It
        position6 = find_image_on_screen(upload_to_roblox)
        move_mouse_to_target(position6)
        # pyautogui.click()                                                 ################# Remove When done

        break  # Exit the loop once the target is found and actions are performed
    
    time.sleep(1)  # Check every second
