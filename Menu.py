import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton, CTkEntry, CTkLabel
from tkinter import filedialog
import MiroSystem, os

# Load in the paths to the folders from a txt file
def load_paths():
    global path, path_final, data_path
    data_path = "D:/a little bit of programming/programming/studia/semestr III/1_PROJECTS/MiroBoardDownloader/data.txt"
    path = MiroSystem.get_line_from_file(data_path, 1) # Path to the "screenshots" folder
    path_final = MiroSystem.get_line_from_file(data_path, 2) # Path to the folder containing a final scan

# Save data to the txt file
def write_to_txt_file():
    current_directory = os.getcwd()
    filename = "data.txt"
    file_path = os.path.join(current_directory, filename)

    screenshotpath = MiroSystem.get_line_from_file(file_path, 1)
    finalpath = MiroSystem.get_line_from_file(file_path, 2)

    # open file in write mode to update the content
    with open(file_path, 'w') as file:
        if len(InputText_screenshotpath.get()) > 0:
            screenshotpath = InputText_screenshotpath.get()

        if len(InputText_finalpath.get()) > 0:
            finalpath = InputText_finalpath.get()

        file.write(screenshotpath + '\n')
        file.write(finalpath + '\n')

# Button function for "Manual" button
def manual_button_clicked():
    global fields_visible

    if fields_visible:
        x_label.place_forget()
        x_entry.place_forget()
        y_label.place_forget()
        y_entry.place_forget()
        fields_visible = False
        button_auto.place(y=50)

    else:
        x_label.place(x=10, y=50)
        x_entry.place(x=55, y=50)
        y_label.place(x=10, y=82)
        y_entry.place(x=55, y=82)
        fields_visible = True
        button_auto.place(y=124)

# Button function for "Auto" button
def auto_button_clicked():
    print("if1" + MiroSystem.get_line_from_file(data_path, 1))
    print("Auto button clicked!")

# Button function for "Start" button
def start_button_clicked():
    def update_text(count):
        button_start.configure(text=f"Starting a scan in {count}")
        if count > 0:
            app.after(1000, update_text, count - 1)
        else:
            # countdown is finished
            if MiroSystem.DoesOverlap("https://miro.com/"):
                app.iconify()
            x_str = x_entry.get()
            y_str = y_entry.get()
            try:
                x = int(x_str)
                y = int(y_str)
            except ValueError:
                print("ERROR: enter valid integers for x and y.")
                return
            print(path)
            MiroSystem.ScanManual(x, y, path)
            MiroSystem.FinalMerge(x, y, path, path_final)
            return
    # start the countdown
    update_text(3)

# Button function for "Settings" button
def settings_button_clicked():
    open_settings_window()

# Open settings window
def open_settings_window():
    # Settings functions
    # Folder selection
    def select_folder():
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            folder_path += "/"
            return folder_path

    # Button function for "accept" button in settings window
    def accept_button_clicked():
        write_to_txt_file()
        load_paths()
        settings_window.destroy()

    # Button function for "cancle" button in settings window
    def cancle_button_clicked():
        settings_window.destroy()

    # Button function for "cancle"
    def findpath_button_clicked():
        InputText_screenshotpath.insert(0,select_folder())
    def findpath_button_clicked2():
        InputText_finalpath.insert(0,select_folder())

    # "Settings" app frame and settings
    settings_window = ctk.CTkToplevel()
    settings_window.geometry("410x480")
    settings_window.title("Settings")
    settings_window.transient(app)
    settings_window.grab_set()

    # "Settings" app frame text input fields
    global InputText_screenshotpath, InputText_finalpath
    # text field for "screenshot" path
    InputText_screenshotpath = CTkEntry(settings_window, width=340, height=40, placeholder_text=MiroSystem.get_line_from_file(data_path,1))
    InputText_screenshotpath.place(x=10, y=40)
    # text field for "final" path
    InputText_finalpath = CTkEntry(settings_window, width=340, height=40, placeholder_text=MiroSystem.get_line_from_file(data_path,2))
    InputText_finalpath.place(x=10, y=120)

    # "Settings" app frame buttons
    # "Accept" button
    button_accept = CTkButton(settings_window, text="Accept", command=accept_button_clicked)
    button_accept.place(x=10, y=440)
    # "Cancle" button
    button_cancle = CTkButton(settings_window, text="Cancle", command=cancle_button_clicked)
    button_cancle.place(x=260, y=440)
    # "Find Path" button
    button_findpath = CTkButton(settings_window, width=50, height=40, text="set", command=findpath_button_clicked)
    button_findpath.place(x=350, y=40)
    button_findpath2 = CTkButton(settings_window, width=50, height=40, text="set", command=findpath_button_clicked2)
    button_findpath2.place(x=350, y=120)

    # "Settings" app frame text
    # text field for screenshots
    text_screenshot = CTkLabel(settings_window, text="Path to the folder that will store all of the single screenshots")
    text_screenshot.place(x=10, y=10)
    # text field for final merged screenshot
    text_final = CTkLabel(settings_window, text="Path to the folder that will store a final scan")
    text_final.place(x=10, y=90)

# System settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# App frame
app = ctk.CTk()
app.geometry("720x480")
app.title("Miro Board Downloader")

# Create the X and Y input fields
x_label = CTkLabel(app, text="Width")
x_entry = CTkEntry(app)
y_label = CTkLabel(app, text="Height")
y_entry = CTkEntry(app)

# "Manual" button
button_manual = CTkButton(app, text="Manual", command=manual_button_clicked)
button_manual.place(x=10, y=10)

# "Auto" button
button_auto = CTkButton(app, text="Auto", command=auto_button_clicked)
button_auto.place(x=10, y=50)

# "Start" button
button_start = CTkButton(app, text="Start", command=start_button_clicked)
button_start.place(x=570, y=440)

# "Settings" button
button_settings = CTkButton(app, text="Settings", command=settings_button_clicked)
button_settings.place(x=10, y=440)

# Flag to track visibility state
fields_visible = False

# Run app
def on_app_start():
    load_paths()
    app.mainloop()

on_app_start()
