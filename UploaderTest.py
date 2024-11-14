import webbrowser
import pyautogui
import cv2
import numpy as np
import time
import pyperclip
from pathlib import Path
import json


with open('config.json', 'r') as f:
    config = json.load(f)

description = config["clothing"]["description"]

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
        pyautogui.moveTo(target_position[0], target_position[1], duration=0.2)
        print(f"Mouse moved to position: {target_position}")
    else:
        print("Target not found on the screen.")

# URL and group ID
groupID = 16240463
url = f"https://create.roblox.com/dashboard/creations/upload?assetType=Shirt&groupId={groupID}"

# Open the site
open_uploadlink(url)

# Path to the target image you want to detect on the screen
upload_button_path = "Storage\OpenCVPic\\upload_button_cv.png"
navigate_path1 = "Storage\OpenCVPic\\navigate_folder1.png"
navigate_path2 = "Storage\OpenCVPic\\navigate_folder_2.png"
name_field_path = "Storage\OpenCVPic\\name_field.png"
discription_field_path = "Storage\OpenCVPic\\description_field.png"
upload_to_roblox = "Storage\OpenCVPic\\upload_to_roblox.png"


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
        position3 = find_image_on_screen(navigate_path2)
        move_mouse_to_target(position3)

        # Copy the Path
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)

        # Edit Path
        current_path = pyperclip.paste() # Set Current Path to clipboard
        base_path = r"Auto-Roblox-Clothing-Bot-main\Auto-Roblox-Clothing-Bot-main\Storage"
        fixed_path = r"\Clothes\Shirts"

        # Paste Path
        if base_path in current_path:

            final_path = Path(current_path) / fixed_path
            pyautogui.press('esc')


            time.sleep(1) ##################### DELETE THIS
            pyautogui.hotkey('Alt', 'f4') ##################### DELETE THIS


        else:
            final_path = Path(current_path) / base_path / fixed_path
            print(2)
            pyperclip.copy(str(final_path))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('enter')
            time.sleep(0.1)


            time.sleep(1) ##################### DELETE THIS
            pyautogui.hotkey('Alt', 'f4') ##################### DELETE THIS


        # Move to the Target Image
        
        # Move to the Name Field
        position4 = find_image_on_screen(name_field_path)
        move_mouse_to_target(position4)
        time.sleep(1) ##################### EDIT DELAY

        # Copy the Name
        pyautogui.click()
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')

        # Delete Picture with the Name

        # Move to the Description Field
        position5 = find_image_on_screen(discription_field_path)
        move_mouse_to_target(position5)
        time.sleep(0.5) ##################### EDIT DELAY
            
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
        # pyautogui.click()


        break  # Exit the loop once the target is found and actions are performed
    
    time.sleep(1)  # Check every second
