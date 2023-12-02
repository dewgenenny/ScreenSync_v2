import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import tkinter as tk
from screensync.screen_sync.stats import runtime_stats

def create_embedded_graph(runtime_stats, parent_widget):
    # Convert target size to inches (1 inch = 96 pixels)
    inches_width = 227 / 96
    inches_height = 83 / 96
    # Create a Figure with the converted size
    fig = Figure(figsize=(inches_width, inches_height), dpi=96)
    ax = fig.add_subplot(111)
    updates_text = fig.text(0.8, 0.5, '', fontsize=26, va='center', ha='center', color='white')
    fig.text(0.8, 0.15, 'Updates/Sec', fontsize=6, va='center', ha='center', color='white')
    fig.text(0.33, 0.044, 'Performance past 5 minutes', fontsize=6, va='center', ha='center', color='white')
    # Function to update the graph
    def update_graph():
        ax.clear()

        # Set the background color for the axes and the figure
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        # Remove padding and margins around the plot
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Hide the axes frame which may have padding
        ax.set_frame_on(False)
        fig.subplots_adjust(left=0.05, right=0.65, top=0.95, bottom=0.05)
        # Optionally, hide the axes ticks as well
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        last_update = runtime_stats.get_last_n_stats(1)[-1][1] if runtime_stats.get_last_n_stats(1) else 0
        # Using text() to place large numbers on the right side of the figure
        #fig.text(0.7, 0.5, str(last_update), fontsize=26, va='center', ha='center', color='white')
        updates_text.set_text(str(last_update))



        # Get last 300 data points
        data = runtime_stats.get_last_n_stats(300)

        # Separate timestamps and values
        timestamps = [datetime.fromtimestamp(ts) for ts, _ in data]
        values = [val for _, val in data]

        # Plot the data
        ax.plot(timestamps, values, color='red', linewidth=1)
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors='white', labelsize=6)  # Format x-axis ticks
        ax.tick_params(axis='y', colors='white', labelsize=6)  # Format y-axis ticks
        ax.spines['bottom'].set_color('white')  # Set the color of the bottom spine
        ax.spines['left'].set_color('white')   # Set the color of the left spine





        # Redraw the canvas
        canvas.draw()

    # Create the matplotlib canvas and pack it into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=parent_widget)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return update_graph
