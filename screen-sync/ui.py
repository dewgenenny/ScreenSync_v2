import tkinter as tk
from tkinter import PhotoImage
from tkinter import Toplevel, Label, Entry, Button, Listbox,LabelFrame, END
from tkinter import ttk

from screen_sync.config_manager import ConfigManager
from screen_sync.bulb_factory import BulbFactory
from screen_sync.coordinator import Coordinator
import screen_sync.color_processing as color_processing
from screen_sync.stats import runtime_stats
from screen_sync.graph import create_embedded_graph

# Initialize necessary objects
config_manager = ConfigManager('./config.ini')
bulb_factory = BulbFactory(config_manager)
bulbs = bulb_factory.create_bulbs()
coordinator = Coordinator(bulbs, color_processing)

# Define the main window
root = tk.Tk()
root.title("ScreenSync V2")
root.geometry('245x255')  # Width x Height
root.configure(bg='#404957')
root.resizable(False, False)
root.overrideredirect(False)



# Global flag to track Shooter Mode state
shooter_mode_active = False

def toggle_shooter_mode():

    global shooter_mode_active, coordinator

    if shooter_mode_active:
        # Disable Shooter Mode by setting it back to 'normal' or any other default mode
        coordinator.set_mode('normal')
        add_new_button.config(text="Enable Shooter")
    else:
        # Enable Shooter Mode
        coordinator.set_mode('shooter')
        add_new_button.config(text="Disable Shooter")

    # Toggle the flag
    shooter_mode_active = not shooter_mode_active


# Define a function to be called when the window is closed
def on_closing():
    if coordinator.running:
        coordinator.stop()  # Make sure to stop the coordinator
    root.destroy()  # Destroy the main window

# Bind the on_closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)


# Function to reinitialize bulbs
def reinitialize_bulbs():
    global config_manager
    config_manager = ConfigManager('./config.ini')
    global bulbs  # If bulbs are defined globally
    bulbs = bulb_factory.create_bulbs()  # Recreate bulbs with new settings
    global coordinator
    coordinator = Coordinator(bulbs, color_processing)
    print(bulbs)


def add_new_clicked():
    toggle_shooter_mode()
    print("Toggle shooter mode clicked")

def start_stop_button_clicked():
    if coordinator.running:
        coordinator.stop()
        start_stop_button.config(text="Start")
    else:
        coordinator.start()
        start_stop_button.config(text="Stop")



def save_general_settings(saturation_var, capture_size_var):
    # Here you'll save the general settings back to config.ini
    # This function will need to be implemented with the actual save logic
    print(f"Saving Saturation: {saturation_var.get()}, Capture Size: {capture_size_var.get()}")

def open_general_settings(config_manager):
    general_settings_window = Toplevel(root)
    general_settings_window.title("General Settings")
    general_settings_window.geometry('300x200')
    general_settings_window.configure(bg='#404957')

    general_settings = config_manager.get_general_settings()

    # Saturation Factor Setting
    Label(general_settings_window, text="Saturation Factor:").grid(row=0, column=0, sticky='e')
    saturation_var = tk.StringVar(value=general_settings.get('saturation_factor', '1.5'))
    Entry(general_settings_window, textvariable=saturation_var).grid(row=0, column=1)

    # Screen Capture Size Setting
    Label(general_settings_window, text="Screen Capture Size:").grid(row=1, column=0, sticky='e')
    capture_size_var = tk.StringVar(value=general_settings.get('screen_capture_size', '100, 100'))
    Entry(general_settings_window, textvariable=capture_size_var).grid(row=1, column=1)

    # Save Button
    save_button = Button(general_settings_window, text="Save",
                         command=lambda: save_general_settings(saturation_var, capture_size_var))
    save_button.grid(row=2, column=0, columnspan=2)


def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x600")  # Adjust the size as needed
    settings_window.configure(bg='#404957')
    settings_window.resizable(False, False)

    # General settings frame
    general_settings_frame = tk.LabelFrame(settings_window, text="General", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    general_settings_frame.pack(padx=10, pady=10, fill='x')
    # MQTT settings frame
    mqtt_settings_frame = tk.LabelFrame(settings_window, text="MQTT Server", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    mqtt_settings_frame.pack(padx=10, pady=10, fill='x')
    # Tuya settings frame
    tuya_settings_frame = tk.LabelFrame(settings_window, text="Tuya Specific", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    tuya_settings_frame.pack(padx=10, pady=10, fill='x')
    # MQTT settings frame
    mqtt_specific_settings_frame = tk.LabelFrame(settings_window, text="MQTT Specific", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    mqtt_specific_settings_frame.pack(padx=10, pady=10, fill='x')

    # Retrieve general settings and create a label and entry for each setting
    general_settings = config_manager.get_general_settings()
    for setting, value in general_settings.items():
        row = tk.Frame(general_settings_frame, bg='#404957')
        row.pack(side='top', fill='x', padx=5, pady=5)

        label = tk.Label(row, text=setting.replace('_', ' ').title() + ":", bg='#404957', fg='white')
        label.pack(side='left')

        entry = tk.Entry(row, bg='white', fg='black')
        entry.pack(side='right', expand=True, fill='x')
        entry.insert(0, value)

    mqtt_settings = config_manager.get_mqtt_settings()

    for setting, value in mqtt_settings.items():
        row = tk.Frame(mqtt_settings_frame, bg='#404957')
        row.pack(side='top', fill='x', padx=5, pady=5)

        label = tk.Label(row, text=setting.replace('_', ' ').title() + ":", bg='#404957', fg='white')
        label.pack(side='left')

        entry = tk.Entry(row, bg='white', fg='black')
        entry.pack(side='right', expand=True, fill='x')
        entry.insert(0, value)

    tuya_settings = config_manager.get_config_by_section("TuyaSettings")

    for setting, value in tuya_settings.items():
        row = tk.Frame(tuya_settings_frame, bg='#404957')
        row.pack(side='top', fill='x', padx=5, pady=5)

        label = tk.Label(row, text=setting.replace('_', ' ').title() + ":", bg='#404957', fg='white')
        label.pack(side='left')

        entry = tk.Entry(row, bg='white', fg='black')
        entry.pack(side='right', expand=True, fill='x')
        entry.insert(0, value)

    mqtt_specific_settings = config_manager.get_config_by_section("MQTTSettings")

    for setting, value in mqtt_specific_settings.items():
        row = tk.Frame(mqtt_specific_settings_frame, bg='#404957')
        row.pack(side='top', fill='x', padx=5, pady=5)

        label = tk.Label(row, text=setting.replace('_', ' ').title() + ":", bg='#404957', fg='white')
        label.pack(side='left')

        entry = tk.Entry(row, bg='white', fg='black')
        entry.pack(side='right', expand=True, fill='x')
        entry.insert(0, value)


    # Bulbs listbox with a scrollbar
    bulbs_frame = tk.LabelFrame(settings_window, text="Bulbs", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    bulbs_frame.pack(padx=10, pady=10, fill='both', expand=True)

    scrollbar = ttk.Scrollbar(bulbs_frame, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    bulbs_listbox = tk.Listbox(bulbs_frame, yscrollcommand=scrollbar.set, bg='#D9D9D9', fg='black')
    bulbs_listbox.pack(side='left', fill='both', expand=True)

    scrollbar.config(command=bulbs_listbox.yview)

    # Assuming bulbs are a list of dictionaries each with a 'type' and 'device_id' key
    bulbs = config_manager.get_bulbs()
    for bulb in bulbs:
        bulbs_listbox.insert(tk.END, f"{bulb['config_id']} - {bulb['device_id']}")

    def on_bulb_select(event):
        selected_bulb = bulbs_listbox.get(bulbs_listbox.curselection())
        open_bulb_settings(selected_bulb.split(' - ')[0])  # Assuming device_id is after '-'

    bulbs_listbox.bind('<<ListboxSelect>>', on_bulb_select)


    # Button to close the settings window
    close_button = tk.Button(settings_window, text="Close", command=settings_window.destroy, bg='#D9D9D9', fg='black')
    close_button.pack(pady=10)

    # Center the settings window on the screen
    center_window_on_screen(settings_window)

def center_window_on_screen(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))



def open_bulb_settings(config_section):
    bulb_window = Toplevel(root)
    bulb_window.title(f"Settings for Bulb: {config_section}")
    bulb_window.configure(bg='#404957')
    bulb_window.geometry("400x300")  # Adjust size as needed

    bulb_settings_frame = LabelFrame(bulb_window, text="Bulb Settings for "+config_section, bg='#404957', fg='white', labelanchor='n')
    bulb_settings_frame.pack(padx=10, pady=10, fill='both', expand=True)

    bulb_settings = config_manager.get_config_by_section(config_section)

    entries = {}
    for row, (setting, value) in enumerate(bulb_settings.items()):
        # Creating a consistent label style
        label = Label(bulb_settings_frame, text=setting.replace("_", " ").capitalize(), bg='#404957', fg='white')
        label.grid(row=row, column=0, sticky='e', padx=40, pady=10, )

        # Styling the entry widgets
        entry = Entry(bulb_settings_frame, bd=1)
        entry.insert(0, value)
        entry.grid(row=row, column=1, sticky='we', ipadx=40, pady=10)
        entries[setting] = entry
    def save_bulb_settings():
        for setting, entry in entries.items():
            config_manager.config[config_section][setting] = entry.get()
        config_manager.save_config()
        new_bulbs = bulb_factory.create_bulbs()
        coordinator.update_bulbs(new_bulbs)
        print("Settings saved!")


    # Save Button
    save_button = Button(bulb_window, text="Save", command=save_bulb_settings)
    save_button.pack(pady=10)

    # Place focus on the window (optional)
    bulb_window.focus_force()

# You might want to periodically update the graph. Set up a mechanism to do so:
def refresh_graph():
    update_graph()
    root.after(500, refresh_graph)  # Update the graph every second


# Stats graph frame
stats_frame = tk.Frame(root, bg='#2C2828', width=227, height=83)
stats_frame.place(x=9, y=50)

update_graph = create_embedded_graph(runtime_stats, stats_frame)
refresh_graph()  # Start the periodic update


# Settings Button
settings_button = tk.Button(root,bg='#D9D9D9',text='Settings', command=open_settings_window)
settings_button.place(x=11, y=150)

# Add New Button
add_new_button = tk.Button(root,bg='#D9D9D9',text='Enable Shooter'
                                           , command=add_new_clicked)
add_new_button.place(x=133, y=150)

# Start/Stop Button
start_stop_button = tk.Button(root, text="Start", bg='#D9D9D9', width=31, height=3, command=start_stop_button_clicked)
start_stop_button.place(x=9, y=190)

root.mainloop()
