# remove_bulb.py

import tkinter as tk
from tkinter import messagebox

def create_remove_bulb_button(bulb_window, config_manager, config_section, refresh_callback):
    def remove_bulb():
        if messagebox.askyesno("Remove Bulb", "Are you sure you want to remove this bulb?"):
            config_manager.remove_bulb(config_section)
            refresh_callback()
            bulb_window.destroy()

    remove_button = tk.Button(bulb_window, text="Remove", command=remove_bulb, bg='red', fg='white')
    return remove_button
