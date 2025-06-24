import pystray
from pystray import MenuItem as item
from PIL import Image
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import psutil
import sys
import subprocess
import winreg
import ctypes
import shutil

# ________________________________________ UTILITY FUNCTIONS ________________________________________ 

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def is_first_run():
    global FLAG_FILE
    FLAG_FILE = resource_path('config.flag')
    return not os.path.exists(FLAG_FILE)

def write_first_run(flag_file):
    with open(flag_file, 'w') as f:
            f.write('Install_Font : TRUE')

def save_font():
    # Ask user where to save the font file
    save_path = filedialog.asksaveasfilename(
        defaultextension=".ttf",
        filetypes=[("TrueType Font", "*.ttf")],
        initialfile="Etruscan-Translitt.ttf",
        title="Save Font As"
    )
    
    if save_path:
        try:
            shutil.copyfile(FONT_BUNDLED_PATH, save_path)
            messagebox.showinfo("DOWNLOAD COMPLETE", f"Font saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to save font:\n{e}")


            
def ask_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Request elevation
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, ' '.join(sys.argv), None, None)

        if int(ret) <= 32:
            # User refused or failed to elevate
            messagebox.showerror("ADMIN REQUIRED", "Administrator privileges are required to install the font. The application will now exit.")
            sys.exit(1)

        # Relaunch initiated successfully, exit current process
        sys.exit()
    else:
        print("Elevated privilege acquired")

def install_font(font_file_path):
    ask_admin()

    try:
        # Open the registry key where the font information is stored
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0,
                            winreg.KEY_ALL_ACCESS)

        # Get the name of the font file
        font_file_name = os.path.basename(font_file_path)

        # Set the font information in the registry
        winreg.SetValueEx(key, font_file_name, 0, winreg.REG_SZ, font_file_path)

        # Close the registry key
        winreg.CloseKey(key)

        messagebox.showinfo("FONT INSTALLED", "Font installed. Be sure to use the matching keyboard.\n\ne.g., Etruscan Translitt Keyboard goes with 'Etruscan Translitt' font.")
        write_first_run(FLAG_FILE)
        return True
    
    except Exception as e:
        messagebox.showerror("ERROR",  f"Failed to install the font: {e}")
        return False

# ________________________________________ VARIABLES ________________________________________ 

FONT_BUNDLED_PATH = resource_path("Etruscan-Translitt.ttf")
FLAG_FILE = resource_path('config.flag')
FONT_PATH = resource_path("Etruscan-Translitt.ttf")
AHK_PATH = resource_path("etrus_tran.ahk")
EXE_PATH = resource_path("etrus_tran.exe")
KEYBOARD_ACTIVATED_NAME = "No Keyboard Enabled"

ETRUSCAN_TRANSLITT_KEYBOARD = False

# ________________________________________ APP ________________________________________ 

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
        icon.notify('Etruscan Translitt ALREADY Enabled\n(e.g., use with the "Etruscan Translitt" font for correct display).')
        return

    ETRUSCAN_TRANSLITT_KEYBOARD = True
    icon.notify('Etruscan Translitt Enabled\n(e.g., use with the "Etruscan Translitt" font for correct display).')
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

download_button = tk.Button(root, text="DOWNLOAD FONT HERE", command=save_font)
download_button.place(x=8, y=100, height=25)

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

if is_first_run(): install_font(FONT_PATH)

# RUN APP ON OTHER THREAD
icon_thread = threading.Thread(target=icon.run, daemon=True)
icon_thread.start()

root.mainloop()