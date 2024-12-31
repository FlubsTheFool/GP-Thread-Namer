import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import os
import win32gui # type: ignore
from time import sleep
from PIL import Image

def capture_window(title):
    hwnd = win32gui.FindWindow(None, title)
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, 9)

    sleep(0.2) # no other way to wait for window animation ig

    window = gw.getWindowsWithTitle(title)[0]
    topbar_size = 36 #100%
    #topbar_size = 45 #125%
    img = pyautogui.screenshot(region=(window.left, window.top+topbar_size, window.width, window.height-topbar_size))
    #img.show()
    return img



def debug_boxes(img, coordinates):
    img = np.array(img) # convert to use with cv2
    img_height, img_width, _ = img.shape

    for (x_rel, y_rel) in coordinates:
        x = int(x_rel * img_width)
        y = int(y_rel * img_height)
        w = int(0.3 * img_width)
        h = int(0.25 * img_height)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    img = Image.fromarray(img) # convert back for PIL
    img.show()



def match_images(img, folder_path, coordinates):
    folder_images = [f for f in os.listdir(folder_path) if f != "Packs" and f != "_.png"]
    matched_images = []

    for file_name in folder_images:
        file_path = os.path.join(folder_path, file_name)
        template = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        
        if template is None:
            continue
        
        template = template[40:template.shape[0], 0:template.shape[1]] # cut off top 40 pixels (new tag on pack open)

        img = np.array(img) # convert to use with cv2

        # Resize template to 1/4 of the region width while keeping aspect ratio
        target_width = img.shape[1] // 4
        scale = target_width / template.shape[1]
        target_height = int(template.shape[0] * scale)
        template = cv2.resize(template, (target_width, target_height), interpolation=cv2.INTER_AREA)


        img_height, img_width, _ = img.shape
        for (x_rel, y_rel) in coordinates:
            x = int(x_rel * img_width)
            y = int(y_rel * img_height)
            w = int(0.3 * img_width)
            h = int(0.25 * img_height)


            sub_region = img[y:y+h, x:x+w]
            result = cv2.matchTemplate(sub_region, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val > 0.4:  # Adjust threshold as needed
                matched_images.append((file_name))

    return matched_images






window_title = input("Instance name: ")
folder_path = "./images"
img = capture_window(window_title)


# (x, y, from origin, relative)
coordinates = [
    (0.05, 0.25),
    (0.35, 0.25),
    (0.65, 0.25),
    (0.2, 0.5),
    (0.5, 0.5)
]

# draws boxes
#debug_boxes(img, coordinates)


matches = match_images(img, folder_path, coordinates)

if matches:
    print("Matched images:")
    for match in matches:
        print(f"- {match}")
else:
    print("No matches found.")