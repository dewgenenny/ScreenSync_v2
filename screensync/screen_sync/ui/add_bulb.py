
import tkinter as tk
from tkinter import ttk
from screensync.screen_sync.bulb_types import BULB_TYPES


def create_add_bulb_window(root, config_manager, refresh_callback):
    # Styles
    style = ttk.Style()
    style.configure('TLabel', background='#404957', foreground='white')
    style.configure('TButton', background='#404957', foreground='white', font=('Helvetica', 10))
    style.configure('TRadiobutton', background='#404957', foreground='white', font=('Helvetica', 10))
    style.map('TButton',
              background=[('active', '#50597A'), ('disabled', '#404957')],
              foreground=[('active', 'white'), ('disabled', 'white')])


    entries = {}
    placement_var = tk.StringVar()

    def update_config_fields(event):
        # Clear previous fields and reset entries
        for widget in config_frame.winfo_children():
            widget.destroy()
        entries.clear()

        bulb_type = bulb_type_var.get()

        # Common placement radio buttons for all bulb types
        ttk.Label(config_frame, text="Placement:").pack()
        placement_frame = tk.Frame(config_frame, bg='#404957')
        placement_frame.pack()

        placements = ['top-left', 'top-center', 'top-right',
                      'center-left', 'center', 'center-right',
                      'bottom-left', 'bottom-center', 'bottom-right']
        for i, placement in enumerate(placements):
            row = i // 3
            column = i % 3
            radio = ttk.Radiobutton(placement_frame, text=placement, variable=placement_var, value=placement, style='TRadiobutton')
            radio.grid(row=row, column=column, sticky='w', padx=5, pady=5)

        # Additional fields based on bulb type
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

        elif bulb_type == 'MagicHome':
            ttk.Label(config_frame, text="IP Address:").pack()
            entries['ip_address'] = ttk.Entry(config_frame)
            entries['ip_address'].pack()

        elif bulb_type == 'MQTT':
            ttk.Label(config_frame, text="MQTT Topic:").pack()
            entries['mqtt_topic'] = ttk.Entry(config_frame)
            entries['mqtt_topic'].pack()


    def on_add_bulb():
        bulb_type = bulb_type_var.get()
        placement = placement_var.get()

        if bulb_type == 'Tuya':
            device_id = entries['device_id'].get() if 'device_id' in entries else None
            local_key = entries['local_key'].get() if 'local_key' in entries else None
            ip_address = entries['ip_address'].get() if 'ip_address' in entries else None
            config_manager.add_bulb(bulb_type, device_id=device_id, local_key=local_key, ip_address=ip_address, placement=placement)

        elif bulb_type == 'MagicHome':
            ip_address = entries['ip_address'].get() if 'ip_address' in entries else None
            config_manager.add_bulb(bulb_type, ip_address=ip_address, placement=placement)

        elif bulb_type == 'MQTT':
            mqtt_topic = entries['mqtt_topic'].get() if 'mqtt_topic' in entries else None
            config_manager.add_bulb(bulb_type, mqtt_topic=mqtt_topic, placement=placement)

        refresh_callback()
        add_bulb_window.destroy()


    add_bulb_window = tk.Toplevel(root)
    add_bulb_window.title("Add New Bulb")
    add_bulb_window.geometry("400x400")
    add_bulb_window.configure(bg='#404957')

    # Dropdown for selecting the bulb type
    bulb_type_label = ttk.Label(add_bulb_window, text="Select Bulb Type:", style='TLabel')
    bulb_type_label.pack(pady=(10, 0))

    bulb_type_var = tk.StringVar()
    bulb_type_dropdown = ttk.Combobox(add_bulb_window, textvariable=bulb_type_var, state='readonly', style='TCombobox')
    bulb_type_dropdown['values'] = BULB_TYPES
    bulb_type_dropdown.pack(pady=(0, 10))

    bulb_type_dropdown.bind("<<ComboboxSelected>>", update_config_fields)

    config_frame = tk.Frame(add_bulb_window, bg='#404957')
    config_frame.pack(fill='both', expand=True, padx=20, pady=10)

    add_button = ttk.Button(add_bulb_window, text="Add Bulb", command=on_add_bulb, style='TButton')
    add_button.pack(pady=(10, 10))

    return add_bulb_window
