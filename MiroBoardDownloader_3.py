import pyautogui, time, os, pyvips, tkinter as tk
from PIL import ImageGrab, Image
from tkinter import filedialog

path = f"d:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/screenshot/"
path_board = f"D:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/BoardDownload/"
path_final = f"D:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/BDT/"
move_time = 0.5
#colors_vertical = [(138, 1, 249), (1, 253, 126), (251, 1, 164), (3, 233, 251), (255, 249, 1)]
#colors_parallel = [(0, 0, 255), (99, 111, 51), (255, 196, 255), (255, 18, 65), (192, 255, 65)]

def screenshot(i):
    file_name = f"screenshot_{i}.png"
    ss = ImageGrab.grab(bbox=(57,58,1910,1020))  
    ss.save(f"{path}{file_name}")

def GoDown(ssID):
    pyautogui.moveTo(1500, 1020)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(1500, 58)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left')
    time.sleep(1)
    screenshot(ssID)

def GoRight(ssID):
    pyautogui.moveTo(1910, 542)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(57, 542)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left')
    time.sleep(1)
    screenshot(ssID)

def GoLeft(ssID):
    pyautogui.moveTo(57, 542)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(1910, 542)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left') 
    time.sleep(1)
    screenshot(ssID)

def border(ss, colors):
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

def upload_images_from_folder(path_board):
    input_images = []
    files = os.listdir(path_board)
    sorted_files = sorted(files, key=lambda x: int(x.split("_")[0].replace("BoardDownloadTest", "")))

    for file in sorted_files:
        if file.endswith(".png"):
            image_path = os.path.join(path_board, file)
            image = pyvips.Image.new_from_file(image_path)
            input_images.append(image)
    return input_images


def scan_manual(width, height):
    w = 1
    h = 1
    ssID = 0
    screenshot(ssID)
    ssID+=1
    while True:
        while True:
            if(w==width):
                w = 1
                break
            if((h-1)%2)==0:
                GoRight(ssID)
            else:
                GoLeft(ssID)
            ssID=ssID+1
            w = w + 1
        if(h==height):
            break
        GoDown(ssID)
        ssID=ssID+1
        h = h + 1
    #print("Scan finished succesfully!")
    # width=int(math.sqrt(width))
    # print(f"height is {height}")
    # print(f"width is {width}")

def stirpes_merge(width, height): # screenshot merge - stripes
    ssID = 0
    ss = Image.open(f"{path}screenshot_{ssID}.png")
    ss_size = ss.size
    BoardDownload = Image.new('RGB',(width*ss_size[0], ss_size[1]), (250,250,250))
    for i in range(0,height):
        for j in range(0,width):
            if(i%2)==0:
                ss = Image.open(f"{path}screenshot_{ssID}.png")
                BoardDownload.paste(ss,(j*ss_size[0],0))
            else:
                ss = Image.open(f"{path}screenshot_{ssID}.png")
                BoardDownload.paste(ss,((width-1-j)*ss_size[0],0))
            ssID=ssID+1
        BoardDownload.save(f"{path_board}BoardDownloadTest{i}.png","PNG")
    print("Stripes merge finished succesfully!")

def final_merge(height): # Screenshot merge - final
    input_images = upload_images_from_folder(path_board)
    output_image = f"{path_final}FinalScan.png"
    input_images.append(pyvips.Image.new_from_file(f"{path_board}BoardDownloadTest{height}_.png"))
    output_vimage = pyvips.Image.arrayjoin(input_images, across=1, shim=0, background=[0, 0, 0])
    output_vimage.write_to_file(output_image)
    print("Done!")

def save_path():









