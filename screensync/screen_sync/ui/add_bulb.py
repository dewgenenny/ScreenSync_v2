
import tkinter as tk
from tkinter import ttk
from screensync.screen_sync.bulb_types import BULB_TYPES


def create_add_bulb_window(root, config_manager, refresh_callback):
    entries = {}
    placement_var = tk.StringVar()

    def update_config_fields(event):
        # Clear previous fields and reset entries
        for widget in config_frame.winfo_children():
            widget.destroy()
        entries.clear()

        bulb_type = bulb_type_var.get()
        if bulb_type == 'Tuya':
            ttk.Label(config_frame, text="Device ID:").pack()
            entries['device_id'] = ttk.Entry(config_frame)
            entries['device_id'].pack()

            ttk.Label(config_frame, text="Local Key:").pack()
            entries['local_key'] = ttk.Entry(config_frame)
            entries['local_key'].pack()

            ttk.Label(config_frame, text="IP Address:").pack()
            entries['ip_address'] = ttk.Entry(config_frame)
            entries['ip_address'].pack()

            # Placement radio buttons
            ttk.Label(config_frame, text="Placement:").pack()
            placement_frame = tk.Frame(config_frame)
            placement_frame.pack()

            placements = ['top-left', 'top-center', 'top-right',
                          'center-left', 'center', 'center-right',
                          'bottom-left', 'bottom-center', 'bottom-right']
            for i, placement in enumerate(placements):
                row = i // 3
                column = i % 3
                ttk.Radiobutton(placement_frame, text=placement, variable=placement_var, value=placement).grid(row=row, column=column, sticky='w')


#         elif bulb_type == 'MagicHome':
#             # Add fields specific to MagicHome bulbs
#         elif bulb_type == 'MQTT':
#             # Add fields specific to MQTT bulbs
#         # Add elif blocks for other bulb types

    def on_add_bulb():
        bulb_type = bulb_type_var.get()
        if bulb_type == 'Tuya':
            device_id = entries['device_id'].get() if 'device_id' in entries else None
            local_key = entries['local_key'].get() if 'local_key' in entries else None
            ip_address = entries['ip_address'].get() if 'ip_address' in entries else None
            placement = placement_var.get()
            config_manager.add_bulb(bulb_type, device_id=device_id, local_key=local_key, ip_address=ip_address, placement=placement)
#         elif bulb_type == 'MagicHome':
#             # Collect and process data for MagicHome bulbs
#         elif bulb_type == 'MQTT':
#             # Collect and process data for MQTT bulbs
#         # Add elif blocks for other bulb types

        refresh_callback()
        add_bulb_window.destroy()

    add_bulb_window = tk.Toplevel(root)
    add_bulb_window.title("Add New Bulb")
    add_bulb_window.geometry("400x300")
    add_bulb_window.configure(bg='#404957')

    # Dropdown for selecting the bulb type
    ttk.Label(add_bulb_window, text="Select Bulb Type:").pack()
    bulb_type_var = tk.StringVar()
    bulb_type_dropdown = ttk.Combobox(add_bulb_window, textvariable=bulb_type_var)
    bulb_type_dropdown['values'] = BULB_TYPES
    bulb_type_dropdown['state'] = 'readonly'
    bulb_type_dropdown.pack()
    bulb_type_dropdown.bind("<<ComboboxSelected>>", update_config_fields)

    config_frame = tk.Frame(add_bulb_window)
    config_frame.pack()

    add_button = tk.Button(add_bulb_window, text="Add Bulb", command=on_add_bulb)
    add_button.pack()

    return add_bulb_window
