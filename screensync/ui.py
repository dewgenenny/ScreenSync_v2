import tkinter as tk
from tkinter import PhotoImage, Toplevel, Label, Entry, Button, Listbox,LabelFrame, ttk, messagebox, END
from PIL import Image, ImageTk
import PIL
from platformdirs import *
import os
from screensync.screen_sync.ui.add_bulb import create_add_bulb_window
from screensync.screen_sync.ui.remove_bulb import create_remove_bulb_button

import pkg_resources

appname = 'ScreenSync_v2'
appauthor = 'Tom George'



from screensync.screen_sync.config_manager import ConfigManager
from screensync.screen_sync.bulb_factory import BulbFactory
from screensync.screen_sync.coordinator import Coordinator
import screensync.screen_sync.color_processing as color_processing
from screensync.screen_sync.stats import runtime_stats
from screensync.screen_sync.graph import create_embedded_graph
# Global flag to track Shooter Mode state
shooter_mode_active = False



def main():

    global config_manager, bulb_factory, bulbs, coordinator

    # Check if config directory exists and if not create
    os.makedirs(user_data_dir(appname, appauthor), exist_ok=True)
    #print(user_data_dir(appname, appauthor) + '/config.ini')
    # Initialize necessary objects
    config_manager = ConfigManager(user_data_dir(appname, appauthor) + '/config.ini')

    bulb_factory = BulbFactory(config_manager)
    bulbs = bulb_factory.create_bulbs()
    coordinator = Coordinator(bulbs, color_processing)
    icon_path = pkg_resources.resource_filename('screensync', 'assets/ScreenSync.ico')
    banner_path = pkg_resources.resource_filename('screensync', 'assets/screensync-banner.png')
    # Define the main window
    root = tk.Tk()
    root.title("ScreenSync V2")
    root.geometry('245x265')  # Width x Height
    root.configure(bg='#000000')
    root.resizable(False, False)
    root.overrideredirect(False)
    root.iconbitmap(icon_path)

    # Load and resize the banner image
    banner_image = Image.open(banner_path)
    banner_image = banner_image.resize((200, 55),  PIL.Image.Resampling.LANCZOS)

    banner_photo = ImageTk.PhotoImage(banner_image)
    # Create a Label to display the image
    banner_label = tk.Label(root, image=banner_photo, bg='#000000')
    banner_label.image = banner_photo  # Keep a reference to avoid garbage collection
    banner_label.place(x=20, y=5)  # Place at the top of the window


    # Stats graph frame
    stats_frame = tk.Frame(root, bg='#000000', width=227, height=83)
    stats_frame.place(x=9, y=60)

    update_graph = create_embedded_graph(runtime_stats, stats_frame)
    refresh_graph(root, update_graph)  # Start the periodic update


    # Settings Button
    settings_button = tk.Button(root, bg='#D9D9D9', text='Settings',
                                command=lambda: open_settings_window(root, coordinator, config_manager, bulb_factory))
    settings_button.place(x=11, y=160)


    # Add New Button
    shooter_button = tk.Button(root,bg='#D9D9D9',text='Enable Shooter'
                                               ,command=lambda: shooter_clicked(shooter_button, coordinator))
    shooter_button.place(x=133, y=160)

    # Bind the on_closing function to the window's close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, coordinator))

    # Start/Stop Button
    # Start/Stop Button
    start_stop_button = tk.Button(root, text="Start", bg='#D9D9D9', width=31, height=3,
                                  command=lambda: start_stop_button_clicked(start_stop_button, coordinator))
    start_stop_button.place(x=9, y=200)




    root.mainloop()




def toggle_shooter_mode(shooter_button, coordinator):

    global shooter_mode_active

    if shooter_mode_active:
        # Disable Shooter Mode by setting it back to 'normal' or any other default mode
        coordinator.set_mode('normal')
        shooter_button.config(text="Enable Shooter")
    else:
        # Enable Shooter Mode
        coordinator.set_mode('shooter')
        shooter_button.config(text="Disable Shooter")

    # Toggle the flag
    shooter_mode_active = not shooter_mode_active


# Define a function to be called when the window is closed
def on_closing(root, coordinator):
    if coordinator.running:
        coordinator.stop()  # Make sure to stop the coordinator
    root.destroy()  # Destroy the main window



# Function to reinitialize bulbs
def reinitialize_bulbs():
    global config_manager
    config_manager = ConfigManager('./config.ini')
    global bulbs
    bulbs = bulb_factory.create_bulbs()  # Recreate bulbs with new settings
    global coordinator
    coordinator = Coordinator(bulbs, color_processing)



def shooter_clicked(shooter_button, coordinator):
    toggle_shooter_mode(shooter_button, coordinator)
    print("Toggle shooter mode clicked")

def start_stop_button_clicked(start_stop_button, coordinator):
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

#     # Screen Capture Size Setting
#     Label(general_settings_window, text="Screen Capture Size:").grid(row=1, column=0, sticky='e')
#     capture_size_var = tk.StringVar(value=general_settings.get('screen_capture_size', '100, 100'))
#     Entry(general_settings_window, textvariable=capture_size_var).grid(row=1, column=1)

    # Save Button
    save_button = Button(general_settings_window, text="Save",
                         command=lambda: save_general_settings(saturation_var, capture_size_var))
    save_button.grid(row=2, column=0, columnspan=2)


def create_settings_frame(parent, title, settings, entries_dict):
    frame = tk.LabelFrame(parent, text=title, bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    frame.pack(padx=10, pady=10, fill='x')

    for setting, value in settings.items():
        row = tk.Frame(frame, bg='#404957')
        row.pack(side='top', fill='x', padx=5, pady=5)

        label = tk.Label(row, text=setting.replace('_', ' ').title() + ":", bg='#404957', fg='white')
        label.pack(side='left')

        entry = tk.Entry(row, bg='white', fg='black')
        entry.pack(side='right', expand=True, fill='x')
        entry.insert(0, value)
        entries_dict[setting] = entry

    return frame

def open_settings_window(root, coordinator, config_manager , bulb_factory):


    # This dictionary will hold the entry widgets for settings
    settings_entries = {
        'General': {},
        'MQTT': {},
        'TuyaSettings': {},
        'MQTTSettings': {},
        'MagicHomeSettings': {}
    }

    def save_settings():
        # Iterate over each settings section and update the configuration
        for section, entries in settings_entries.items():
            for setting, entry in entries.items():
                config_manager.config[section][setting] = entry.get()

        # Save the updated configuration to the file
        config_manager.save_config()

        # Refresh the bulbs and UI if necessary
        refresh_bulb_list()

        # Provide feedback that settings have been saved
        messagebox.showinfo("Settings", "Settings have been saved successfully.")


    def refresh_bulb_list():
        bulbs_listbox.delete(0, tk.END)  # Clear the existing list
        bulbs = config_manager.get_bulbs()  # Retrieve updated list of bulbs
        for bulb in bulbs:
            bulbs_listbox.insert(tk.END, f"{bulb['config_id']} - {bulb['device_id']} - {bulb['placement']}")
        reinitialize_bulbs()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x700")  # Adjust the size as needed
    settings_window.configure(bg='#404957')
    settings_window.resizable(False, False)

    # General settings frame
    general_settings_frame = create_settings_frame(settings_window, "General", config_manager.get_general_settings(), settings_entries['General'])
    # MQTT settings frame
    mqtt_settings_frame = create_settings_frame(settings_window, "MQTT Server", config_manager.get_mqtt_settings(), settings_entries['MQTT'])
    # Tuya settings frame
    tuya_settings_frame = create_settings_frame(settings_window, "Tuya Specific", config_manager.get_config_by_section("TuyaSettings"), settings_entries['TuyaSettings'])
    # MQTT specific settings frame
    mqtt_specific_settings_frame = create_settings_frame(settings_window, "MQTT Specific", config_manager.get_config_by_section("MQTTSettings"), settings_entries['MQTTSettings'])
    # MagicHome settings frame
    magichome_specific_settings_frame = create_settings_frame(settings_window, "MagicHome Specific", config_manager.get_config_by_section("MagicHomeSettings"), settings_entries['MagicHomeSettings'])

    # Add "Save Settings" Button
    save_button = tk.Button(settings_window, text="Save Settings", command=save_settings, bg='green', fg='white')
    save_button.pack(side='bottom', pady=10)

    add_new_frame = tk.LabelFrame(settings_window, text="Add New Bulb", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    add_new_frame.pack(padx=10, pady=10, fill='x')

    # Bulbs listbox with a scrollbar
    bulbs_frame = tk.LabelFrame(settings_window, text="Bulbs", bg='#404957', fg='white', font=("TkDefaultFont", 12, "bold"))
    bulbs_frame.pack(padx=10, pady=10, fill='both', expand=True)

    scrollbar = ttk.Scrollbar(bulbs_frame, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    bulbs_listbox = tk.Listbox(bulbs_frame, yscrollcommand=scrollbar.set, bg='#D9D9D9', fg='black')
    bulbs_listbox.pack(side='left', fill='both', expand=True)

    scrollbar.config(command=bulbs_listbox.yview)

    #add_bulb_window = create_add_bulb_window(root, config_manager, refresh_ui)

    # Add New Button
    add_new_button = tk.Button(add_new_frame,bg='#D9D9D9',text='    Add    '
                                               ,command=lambda: create_add_bulb_window(root, config_manager, refresh_bulb_list))
    #shooter_button.place(x=133, y=160)

    add_new_button.pack()
    # Assuming bulbs are a list of dictionaries each with a 'type' and 'device_id' key
    bulbs = config_manager.get_bulbs()
    for bulb in bulbs:
        bulbs_listbox.insert(tk.END, f"{bulb['config_id']} - {bulb['device_id']}")

    def on_bulb_select(event):
        selected_bulb = bulbs_listbox.get(bulbs_listbox.curselection())
        open_bulb_settings(root, coordinator,config_manager, bulb_factory,refresh_bulb_list, selected_bulb.split(' - ')[0])  # Assuming device_id is after '-'

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



def open_bulb_settings(root, coordinator, config_manager, bulb_factory,refresh_bulb_list, config_section):


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
    # Create and place the Remove Button
    remove_button = create_remove_bulb_button(bulb_window, config_manager, config_section, refresh_bulb_list)
    remove_button.pack(pady=(0, 10))  # Adjust padding as needed
    # Place focus on the window (optional)
    bulb_window.focus_force()

# You might want to periodically update the graph. Set up a mechanism to do so:
def refresh_graph(root, update_graph):
    update_graph()
    root.after(500, lambda: refresh_graph(root, update_graph))  # Update the graph every second

if __name__ == "__main__":
    main()
