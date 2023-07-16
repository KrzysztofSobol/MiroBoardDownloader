import pyautogui, time, subprocess, os, pyvips
from PIL import ImageGrab, Image

path = f"d:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/screenshot/"
path_board = f"D:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/BoardDownload/"
path_final = f"D:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/BDT/"
colors_vertical = [(138, 1, 249), (1, 253, 126), (251, 1, 164), (3, 233, 251), (255, 249, 1)]
colors_parallel = [(0, 0, 255), (99, 111, 51), (255, 196, 255), (255, 18, 65), (192, 255, 65)]

def screenshot(i):
    file_name = f"screenshot_{i}.png"
    ss = ImageGrab.grab(bbox=(57,58,1910,1020))  
    ss.save(f"{path}{file_name}")
    return ss

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
    ss = screenshot(ssID)  
    return ss

def GoLeft(ssID):
    pyautogui.moveTo(57, 542)
    pyautogui.mouseDown(button='left')
    time.sleep(0.5)
    pyautogui.moveTo(1910, 542)
    time.sleep(0.5)
    pyautogui.mouseUp(button='left') 
    time.sleep(1)
    ss = screenshot(ssID)
    return ss

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

# scan
width = 4
w = 1
height = 14
h = 1
ssID = 0
screenshot(ssID)
ssID=ssID+1
while True:
    while True:
        if (w==width):
            w = 1
            break
        if((h-1)%2)==0:
         ss = GoRight(ssID)
        else:
         ss = GoLeft(ssID)
        ssID=ssID+1
        w = w + 1
    if (h==height):
        break
    GoDown(ssID)
    ssID=ssID+1
    h = h + 1
print("Scan finished succesfully!")

#width=int(math.sqrt(width))
print(f"height is {height}")
print(f"width is {width}")

# screenshot merge - stripes
ssID = 0
ss = Image.open(f"{path}screenshot_{ssID}.png")
ss_size = ss.size
BoardDownload = Image.new('RGB',(width*ss_size[0], ss_size[1]), (250,250,250))
for i in range(0    ,height): #height
    for j in range(0,width): #width
        if(i%2)==0:
            ss = Image.open(f"{path}screenshot_{ssID}.png") 
            BoardDownload.paste(ss,(j*ss_size[0],0)) 
        else:
            ss = Image.open(f"{path}screenshot_{ssID}.png") 
            BoardDownload.paste(ss,((width-1-j)*ss_size[0],0))
        ssID=ssID+1
    BoardDownload.save(f"{path_board}BoardDownloadTest{i}_.png","PNG")
print("Stripes merge finished succesfully!")

# screenshot merge - final
input_images = [f"{path_board}BoardDownloadTest0_.png", f"{path_board}BoardDownloadTest1_.png"]
output_image = f"{path_final}temp0.png"
subprocess.run(['vips', 'join'] + input_images + [output_image, 'vertical'])

for i in range(0,height-2):
    input_images = [f"{path_final}temp{i}.png", f"{path_board}BoardDownloadTest{i+2}_.png"]
    output_image = f"{path_final}temp{i+1}.png"
    subprocess.run(['vips', 'join'] + input_images + [output_image, 'vertical'])
    file_path = f"{path_final}temp{i}.png"
    os.remove(file_path)
print("Done!")







