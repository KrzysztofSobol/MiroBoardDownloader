from tkinter import filedialog, messagebox
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton, CTkEntry, CTkLabel



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
    select_folder()
    print("Auto button clicked!")

# Button function for "Start" button
def start_button_clicked():
    def update_text(count):
        button_start.configure(text=f"Starting a scan in {count}")
        if count > 0:
            app.after(1000, update_text, count - 1)
        else:
            # countdown is finished, minimize the window
            app.iconify()
    # start the countdown
    update_text(3)

# Folder selection
def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        print("Selected folder path:", folder_path)
        # You can do further processing with the selected folder path here

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

# Flag to track visibility state
fields_visible = False

# Run app
app.mainloop()
