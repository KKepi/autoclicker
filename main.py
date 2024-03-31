import customtkinter as ctk
from pynput.mouse import Button, Controller 
from pynput.keyboard import Key as KKey
from pynput.keyboard import Controller as KController
import time
import threading

app = ctk.CTk()
app.geometry("700x400")
ctk.set_appearance_mode("dark")

# prvotni select frame
select_frame = ctk.CTkFrame(app)
select_frame.pack(fill="both", expand=True)
select_frame.place(relx=0.5, rely=0.15, anchor="center")

selected_option = ctk.StringVar(value="mouse")

global keyboard_status, mouse_status, mouse_clicker_frame, keyboard_clicker_count_frame, keyboard_clicker_wait_frame, keyboard_clicker_key_frame

def mouse_clicker_select():
    # show mouse clicker
    mouse_clicker_frame.pack(fill="x", pady=5)
    # close keyboard clicker
    keyboard_clicker_count_frame.pack_forget()
    keyboard_clicker_wait_frame.pack_forget()
    keyboard_clicker_key_frame.pack_forget()

def keyboard_clicker_select():
    # close mouse clicker
    mouse_clicker_frame.pack_forget()
    # show keyboard clicker
    keyboard_clicker_count_frame.pack(fill="x", pady=5)
    keyboard_clicker_wait_frame.pack(fill="x", pady=5)
    keyboard_clicker_key_frame.pack(fill="x", pady=5)  
    
radio_button1 = ctk.CTkRadioButton(select_frame, text="Mouse clicker", variable=selected_option, value="mouse", command=mouse_clicker_select)
radio_button1.pack(anchor=ctk.W)

radio_button2 = ctk.CTkRadioButton(select_frame, text="Keyboard clicker", variable=selected_option, value="keyboard", command=keyboard_clicker_select)
radio_button2.pack(anchor=ctk.W)

# settings

settings_frame = ctk.CTkFrame(app)
settings_frame.pack(fill="both", expand=True)
settings_frame.place(relx=0.5,rely=0.5, anchor="center")

# Mouse clicker nastavení
mouse_clicker_frame = ctk.CTkFrame(settings_frame)
mouse_clicker_frame.pack(fill="x", pady=5)

mouse_clicker_count_label = ctk.CTkLabel(mouse_clicker_frame, text="Wait between clicks:  ")
mouse_clicker_count_label.pack(side="left")

mouse_clicker_count_field = ctk.CTkEntry(mouse_clicker_frame)
mouse_clicker_count_field.pack(side="left", fill="x", expand=True)

# Keyboard clicker count nastavení
keyboard_clicker_count_frame = ctk.CTkFrame(settings_frame)
keyboard_clicker_count_frame.pack(fill="x", pady=5)

keyboard_clicker_count_label = ctk.CTkLabel(keyboard_clicker_count_frame, text="Wait between clicks:  ")
keyboard_clicker_count_label.pack(side="left")

keyboard_clicker_count_field = ctk.CTkEntry(keyboard_clicker_count_frame)
keyboard_clicker_count_field.pack(side="left", fill="x", expand=True)

# Keyboard clicker wait nastavení
keyboard_clicker_wait_frame = ctk.CTkFrame(settings_frame)
keyboard_clicker_wait_frame.pack(fill="x", pady=5)

keyboard_clicker_wait_label = ctk.CTkLabel(keyboard_clicker_wait_frame, text="Wait after x clicks: ")
keyboard_clicker_wait_label.pack(side="left")

keyboard_clicker_wait_field = ctk.CTkEntry(keyboard_clicker_wait_frame)
keyboard_clicker_wait_field.pack(side="left", fill="x", expand=True)

# Keyboard clicker key nastavení
keyboard_clicker_key_frame = ctk.CTkFrame(settings_frame)
keyboard_clicker_key_frame.pack(fill="x", pady=5)

keyboard_clicker_key_label = ctk.CTkLabel(keyboard_clicker_key_frame, text="Key: ")
keyboard_clicker_key_label.pack(side="left")

keyboard_clicker_key_field = ctk.CTkEntry(keyboard_clicker_key_frame)
keyboard_clicker_key_field.pack(side="left", fill="x", expand=True)

# Start / End

def mouse_clicker_run(clicker_count=1):
    global mouse_status

    mouse = Controller()
    button = Button.left
    mouse_status = True

    while mouse_status == True:
        mouse.click(button)
        time.sleep(float(clicker_count))
    
def keyboard_clicker_run(clicker_count=1, clicker_wait=1, clicker_key="w"):
    global keyboard_status
    
    keyboard = KController()
    keyboard_status = True
    
    if clicker_key == "space":
        clicker_key = KKey.enter

    while keyboard_status == True:
        for i in range(int(clicker_count)):
            keyboard.press(clicker_key)
            keyboard.release(clicker_key)
        time.sleep(float(clicker_wait))
    
    
def shutdown():
    global mouse_status
    global keyboard_status
    mouse_status = False
    keyboard_status = False
    

def on_button_click():
    global mouse_status

    if selected_option.get() == "mouse":
        clicker_count = mouse_clicker_count_field.get()
        threading.Thread(target=mouse_clicker_run, args=(clicker_count,)).start()
        
    else:
        clicker_count = keyboard_clicker_count_field.get()
        clicker_wait = keyboard_clicker_wait_field.get()
        clicker_key = keyboard_clicker_key_field.get()
        
        threading.Thread(target=keyboard_clicker_run, args=(clicker_count, clicker_wait, clicker_key,)).start()

def off_button_click():
    shutdown()

button_frame = ctk.CTkFrame(app)
button_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)

on_button = ctk.CTkButton(button_frame, text="On", command=on_button_click)
on_button.pack(side=ctk.LEFT, padx=5, pady=5)

off_button = ctk.CTkButton(button_frame, text="Off", command=off_button_click)
off_button.pack(side=ctk.RIGHT, padx=5, pady=5)

# Countdown

countdown_frame = ctk.CTkFrame(app)
countdown_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)

countdown = ctk.CTkLabel(countdown_frame, text="START ZA :  ")
countdown.pack()


if __name__ == "__main__":
    mouse_clicker_select()
    app.mainloop()
