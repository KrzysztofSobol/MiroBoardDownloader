import pyautogui, time, os, pyvips
from PIL import ImageGrab
import pygetwindow as gw

def Screenshot(i, path):
    file_name = f"screenshot_{i}.png"
    ss = ImageGrab.grab(bbox=(57,58,1910,1020))  
    ss.save(f"{path}{file_name}")

def GoDown(ssID, path):
    Screenshot(ssID, path)
    pyautogui.moveTo(1500, 1020)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(1500, 58)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left')
    time.sleep(1)

def GoRight(ssID, path):
    Screenshot(ssID, path)
    pyautogui.moveTo(1910, 542)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(57, 542)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left')
    time.sleep(1)

def GoLeft(ssID, path):
    Screenshot(ssID, path)
    pyautogui.moveTo(57, 542)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(1910, 542)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left') 
    time.sleep(1)

# function that finds a border in a screenshot
def Border(ss, colors):
    screenshot_array = ss.load()
    colors_found = set()
    for y in range(ss.size[1]):
        for x in range(ss.size[0]):
            pixel_color = screenshot_array[x, y]
            if pixel_color in colors:
                colors_found.add(pixel_color)
    if colors_found:
        return 1
    else:
        return 0

# Read a certian x line from a file
def get_line_from_file(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                return lines[line_number - 1].strip()
            else:
                return "Line number out of range."
    except FileNotFoundError:
        return "File not found."

# function for uploading and sorting all the screenshots into an array
def Upload_images_from_folder(path):
    input_images = []
    files = os.listdir(path)

    sorted_files = sorted(files, key=lambda x: int(x.split("screenshot_")[1].split(".png")[0]) if "screenshot_" in x else 0)

    for file in sorted_files:
        if file.endswith(".png"):
            image_path = os.path.join(path, file)
            image = pyvips.Image.new_from_file(image_path)
            input_images.append(image)
    return input_images

# function that checks if MBD is overlapping with https://miro.com
def DoesOverlap(URL):
    window_list = gw.getWindowsWithTitle(URL)
    if len(window_list) > 0:
        time.sleep(1)
        return True
    else:
        return False

# function to scan an X by Y area on the board
def ScanManual(width, height, path):
    ssID = 0
    for h in range(0, height):
        for w in range(1, width):
            if h % 2 == 0:
                GoRight(ssID, path)
            else:
                GoLeft(ssID, path)
            ssID += 1
        if h < height:
            GoDown(ssID, path)
            ssID += 1

# function to merge all the screenshots into one big image
def FinalMerge(height, width, path, path_final):
    input_images = Upload_images_from_folder(path)

    # Rearrange the images in a snake lookin pattern
    rearranged_images = []
    for h in range(height):
        for w in range(width):
            if h % 2 == 0:
                # Even rows: left-to-right
                index = h * width + w
            else:
                # Odd rows: right-to-left
                index = (h + 1) * width - (w + 1)
            rearranged_images.append(input_images[index])

    output_image = f"{path_final}FinalScan.png"
    output_vimage = pyvips.Image.arrayjoin(rearranged_images, across=width, shim=0, background=[0, 0, 0])
    output_vimage.write_to_file(output_image)









