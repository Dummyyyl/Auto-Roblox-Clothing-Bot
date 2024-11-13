import webbrowser
import pyautogui
import cv2
import numpy as np
import time

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
image_path1 = r"Storage\OpenCVPic\picture1.png"
image_path2 = r"Storage\OpenCVPic\picture2.png"
image_path3 = r"Storage\OpenCVPic\picture3.png"
image_path4 = r"Storage\OpenCVPic\target_image.png"

time.sleep(5)

# Continuously check for the target image on the screen
while True:
    position1 = find_image_on_screen(image_path1)
    # position2 = find_image_on_screen(image_path2)
    # position3 = find_image_on_screen()
    # position4 = find_image_on_screen()
    if position1:
        move_mouse_to_target(position1)
        pyautogui.click()
        time.sleep(0.5)
        position2 = find_image_on_screen(image_path2)
        move_mouse_to_target(position2)
        pyautogui.click()
        pyautogui.click()

        # pyautogui.hotkey('ctrl', 'v')
        break  # Exit the loop once the target is found and mouse is moved
    time.sleep(1)  # Check every second
