import pystray
from pystray import MenuItem as item
from PIL import Image
import tkinter as tk
import threading
import os
import psutil
import sys
import subprocess

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

AHK_PATH = resource_path("etrus_tran.ahk")
EXE_PATH = resource_path("etrus_tran.exe")
KEYBOARD_ACTIVATED_NAME = "No Keyboard Enabled"

ETRUSCAN_TRANSLITT_KEYBOARD = False

def toggle_window(icon, item):
    global window_visible
    if window_visible:
        root.withdraw()
    else:
        root.deiconify()
    window_visible = not window_visible

def quit_app(icon, item):
    disabled_keyboard(icon, item)
    icon.stop()
    root.destroy()

def on_closing():
    global window_visible
    root.withdraw()
    window_visible = False

def disabled_keyboard(icon, item):
    if ETRUSCAN_TRANSLITT_KEYBOARD:
        disable_etruscanTranslitt(icon, item)

def activate_etruscanTranslitt(icon, item):
    global KEYBOARD_ACTIVATED_NAME
    global ETRUSCAN_TRANSLITT_KEYBOARD

    if ETRUSCAN_TRANSLITT_KEYBOARD:
        icon.notify('Etruscan Translitt ALREADY Enabled')
        return

    ETRUSCAN_TRANSLITT_KEYBOARD = True
    icon.notify('Etruscan Translitt Enabled')
    subprocess.Popen([EXE_PATH, AHK_PATH])
    KEYBOARD_ACTIVATED_NAME = "Disabled Etruscan Translitt"
    icon.update_menu()

def disable_etruscanTranslitt(icon, item):
    global KEYBOARD_ACTIVATED_NAME
    global ETRUSCAN_TRANSLITT_KEYBOARD

    ETRUSCAN_TRANSLITT_KEYBOARD = False
    icon.notify('Etruscan Translitt Disabled')
    KEYBOARD_ACTIVATED_NAME = "No Keyboard Enabled"
    icon.update_menu()

    for proc in psutil.process_iter(['name', 'cmdline']):
        if 'etrus_tran.exe' in proc.info['name'] and AHK_PATH in ' '.join(proc.info['cmdline']):
            proc.terminate()

def activate_etruscanEpigr(icon, item):
    icon.notify('Etruscan Epigr Activated')

# MAIN WINDOW
root = tk.Tk()
root.title("Settings - EtruKey 1.0.0")
root.resizable(False, False)
root.geometry("700x400")
root.config(bg="#ecf0f1")
root.protocol("WM_DELETE_WINDOW", on_closing)

if getattr(sys, 'frozen', False): base_path = sys._MEIPASS
else: base_path = os.path.abspath(".")

root.iconbitmap(os.path.join(base_path, "Icon.ico"))

settings = tk.Label(master=root, text="SETTINGS", font=("Helvetica", 40, 'bold'))
settings.config(bg="#ecf0f1", fg="#2c3e50")
settings.place(x=8, y=18, height=45)

name = tk.Label(master=root, text="ETRUKEY VERSION 1.0.0", font=("Helvetica", 8))
name.config(bg="#ecf0f1", fg="#34495e")
name.place(x=6, y=380, height=12)

credit = tk.Label(master=root, text="MADE BY CHURCAPS", font=("Helvetica", 8))
credit.config(bg="#ecf0f1", fg="#34495e")
credit.place(x=585, y=380, height=12)

# GLOBAL VARIABLE TO TRACK WINDOW VISIBLITY
window_visible = False
root.withdraw()

icon = pystray.Icon("EtruKey")
icon.icon = Image.open(os.path.join(base_path, "Icon.png"))

keyboards_submenu = pystray.Menu(
    item(text='Etruscan Translitt', action=activate_etruscanTranslitt),
    item(text='Etruscan Epigr', action=activate_etruscanEpigr)
)

icon.menu = pystray.Menu(
    item(lambda text:KEYBOARD_ACTIVATED_NAME, action=disabled_keyboard),
    pystray.Menu.SEPARATOR,
    item('Enable Keyboard', keyboards_submenu),
    item(text='Settings', action=toggle_window, default=True),
    item("Quit EtruKey", quit_app)
)

# RUN APP ON OTHER THREAD
icon_thread = threading.Thread(target=icon.run, daemon=True)
icon_thread.start()

root.mainloop()