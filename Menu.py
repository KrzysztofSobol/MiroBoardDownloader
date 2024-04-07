import customtkinter as ctk
import MiroSystem as ms
from customtkinter import *
from threading import Thread
import os


# Load in the paths to the folders from a txt file
def load_paths():
    global path, path_final, data_path

    current_directory = os.path.dirname(__file__) # Get current directory
    filename = "data.txt"
    data_path = os.path.join(current_directory, filename)

    path = ms.get_line_from_file(data_path, 1) # Path to the "screenshots" folder
    path_final = ms.get_line_from_file(data_path, 2) # Path to the folder containing a final scan

# Save data to the txt file
def write_to_txt_file():
    current_directory = os.getcwd()
    filename = "data.txt"
    file_path = os.path.join(current_directory, filename)

    screenshotpath = ms.get_line_from_file(file_path, 1)
    finalpath = ms.get_line_from_file(file_path, 2)

    # open file in write mode to update the content
    with open(file_path, 'w') as file:
        if len(InputText_screenshotpath.get()) > 0:
            screenshotpath = InputText_screenshotpath.get()

        if len(InputText_finalpath.get()) > 0:
            finalpath = InputText_finalpath.get()

        file.write(screenshotpath + '\n')
        file.write(finalpath + '\n')

def TimeEstimate():
    if(len(x_entry.get())!=0):
        print(x_entry.get())

# Button function for "Manual" button
def manual_button_clicked():
    global fields_visible

    if fields_visible:
        frame_manual.place_forget()
        fields_visible = False

    else:
        frame_manual.place(x=0, y=48)
        fields_visible = True

# Button function for "Start" button
def start_button_clicked():
    def run_scan_manual(x, y, path, path_final):
        ms.ScanManual(x, y, path)
        ms.FinalMerge(x, y, path, path_final)
        button_start.configure(text="Start")
    def update_text(count):
        button_start.configure(text=f"Starting a scan in {count}")
        if count > 0: # keep counting
            app.after(1000, update_text, count - 1)
        else:
            # countdown is finished
            button_start.configure(text="In progress")
            if ms.DoesOverlap("https://miro.com/"): # Is Miro overlapping
                app.iconify()
            x_str = x_entry.get()
            y_str = y_entry.get()
            try:
                x = int(x_str)
                y = int(y_str)
            except ValueError:
                print("ERROR: enter valid integers for x and y.")
                return
            scan_thread = Thread(target=run_scan_manual, args=(x, y, path, path_final))
            scan_thread.start()
            return
    # start the countdown
    update_text(3)

# Button function for "Settings" button
def settings_button_clicked():
    open_settings_window()

# Slider function for a "Cooldown" slider
def slider_changed(value):
    sleep_time = value / 10

# Open settings window
def open_settings_window():
    settings_window.grab_set()
    InputText_screenshotpath.configure(placeholder_text = ms.get_line_from_file(data_path, 1))
    InputText_finalpath.configure(placeholder_text = ms.get_line_from_file(data_path, 2))
    settings_window.place(x=280, y=1)

# System settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# ======================================= App frame =======================================
app = ctk.CTk()
app.geometry("720x480") # Size of a main window
app.title("Miro Board Downloader") # Name of a main window
app.iconbitmap('icon.ico') # Icon of a main window
app.resizable(False, False)
# === Frames ===
# Right_Side Frame
frame_right_side = ctk.CTkFrame(master=app, width=440, height=665, border_width=3, fg_color='#2e2e2e', bg_color="#484444")
frame_right_side.place(x=280, y=1)

# Bottom frame
frame_bottom = ctk.CTkFrame(master=app, width=720, height=55, border_width=3, fg_color='#383838', bg_color='#484444')
frame_bottom.place(x=0, y=430)

# X and Y entrys frame
frame_manual = ctk.CTkFrame(master=app, width=210, height=61, border_width=-3, fg_color="#242424")

# Create the X and Y input fields
x_label = CTkLabel(frame_manual, text="Width")
x_entry = CTkEntry(frame_manual)
y_label = CTkLabel(frame_manual, text="Height")
y_entry = CTkEntry(frame_manual)

x_label.place(x=10, y=0)
x_entry.place(x=55, y=0)
y_label.place(x=10, y=32)
y_entry.place(x=55, y=32)

# "Progress" bar
progress_bar = ctk.CTkProgressBar(frame_right_side, mode="determinate", width=400, height=10, bg_color="#2e2e2e")
progress_bar.configure(fg_color="grey", progress_color="green")
progress_bar.set(0)
progress_bar.place(relx=0.5, rely=0.62, anchor="center")

# "Manual" button
button_manual = CTkButton(app, text="Manual", command=manual_button_clicked)
button_manual.place(x=10, y=10)

# "Start" button
button_start = CTkButton(frame_bottom, text="Start", fg_color="green", hover_color="darkgreen", command=start_button_clicked)
button_start.place(x=570, y=12)

# "Settings" button
button_settings = CTkButton(frame_bottom, text="Settings", command=settings_button_clicked)
button_settings.place(x=10, y=12)

# Flag to track visibility state
fields_visible = False


# ======================================= "Settings" app =======================================
# Settings functions

# Folder selection
def select_folder():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        folder_path += "/"
        return folder_path

# Button function for "accept" button in settings window
def accept_button_clicked():
    write_to_txt_file()
    load_paths()
    settings_window.grab_release()
    settings_window.place_forget()

# Button function for "cancle" button in settings window
def cancle_button_clicked():
    settings_window.grab_release()
    settings_window.place_forget()

# Button function for "cancle"
def findpath_button_clicked():
    InputText_screenshotpath.insert(0,select_folder())
def findpath_button_clicked2():
    InputText_finalpath.insert(0,select_folder())

# "Settings" frame
settings_window = ctk.CTkFrame(master=app, width=440, height=432, border_width=3, fg_color='#2e2e2e', bg_color="#484444")

frame_bottom_settings = ctk.CTkFrame(master=settings_window, width=434, height=55, border_width=-3, fg_color='#383838')
frame_bottom_settings.place(x=3, y=374)

# "Settings" app frame text input fields
# text field for "screenshot" path
InputText_screenshotpath = CTkEntry(settings_window, width=369, height=40)
InputText_screenshotpath.place(x=10, y=40)
# text field for "final" path
InputText_finalpath = CTkEntry(settings_window, width=369, height=40)
InputText_finalpath.place(x=10, y=120)
# "Settings" app frame buttons
# "Accept" button
button_accept = CTkButton(frame_bottom_settings, text="Accept", command=accept_button_clicked)
button_accept.place(x=10, y=12)
# "Cancle" button
button_cancle = CTkButton(frame_bottom_settings, text="Cancle", command=cancle_button_clicked)
button_cancle.place(x=287, y=12)
# "Set" button
button_findpath = CTkButton(settings_window, width=50, height=40, border_width=2, text="set", border_color="#50585c", command=findpath_button_clicked)
button_findpath.place(x=379, y=40)
button_findpath2 = CTkButton(settings_window, width=50, height=40, border_width=2, text="set", border_color="#50585c", command=findpath_button_clicked2)
button_findpath2.place(x=379, y=120)

# "Settings" app frame text
# text field for screenshots
text_screenshot = CTkLabel(settings_window, text="Path to the folder that will store all of the single screenshots")
text_screenshot.place(x=10, y=10)
# text field for final merged screenshot
text_final = CTkLabel(settings_window, text="Path to the folder that will store a final scan")
text_final.place(x=10, y=90)

# Run app
def on_app_start():
    load_paths()
    app.mainloop()

on_app_start()
