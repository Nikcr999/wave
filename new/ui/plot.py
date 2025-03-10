"""
Plot module for setting up and configuring the plot area.
Contains functions for creating and configuring the matplotlib plot.
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import state
from handlers.plot_handlers import plot_data, clear_plots
from handlers.mark_handlers import onclick
from handlers.hover_handlers import on_hover

def setup_plot_area(content_frame):
    """
    Set up the plot area in the given container
    
    Args:
        content_frame: The container frame for the plot
        
    Returns:
        tuple: (paned_window, upper_frame, lower_frame)
    """
    # Create paned window for plot and table
    paned_window = ttk.PanedWindow(content_frame, orient=tk.VERTICAL)
    paned_window.pack(fill=tk.BOTH, expand=True)
    
    upper_frame = ttk.Frame(paned_window)
    lower_frame = ttk.Frame(paned_window)
    paned_window.add(upper_frame, weight=2)
    paned_window.add(lower_frame, weight=8)
    
    # Create plot title
    state.plot_title = ttk.Label(
        upper_frame,
        text="Cell Distribution",
        font=('Helvetica', 12, 'bold')
    )
    state.plot_title.pack(pady=(5,0))
    
    # Create matplotlib figure and canvas
    state.fig, state.ax = plt.subplots(figsize=(16, 1.8))
    state.canvas_plot = FigureCanvasTkAgg(state.fig, master=upper_frame)
    state.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Connect event handlers
    state.fig.canvas.mpl_connect("button_press_event", onclick)
    state.fig.canvas.mpl_connect("motion_notify_event", on_hover)
    state.fig.subplots_adjust(left=0.08, right=0.98, bottom=0.4, top=0.85)
    
    # Create lower box for table
    state.lower_box = ttk.Frame(lower_frame, style='Bordered.TFrame')
    state.lower_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Configure initial plot
    configure_initial_plot()
    
    return paned_window, upper_frame, lower_frame

def configure_initial_plot():
    """
    Configure the initial plot with default settings
    """
    state.ax.grid(True, which='major', linestyle='-', alpha=0.8)
    state.ax.grid(True, which='minor', linestyle=':', alpha=0.5)
    state.ax.minorticks_on()
    state.ax.set_xlim(-2.4, 4.6)
    x_ticks_major = np.arange(-2.4, 4.8, 1.0)
    x_ticks_minor = np.arange(-2.4, 4.8, 0.5)
    state.ax.set_xticks(x_ticks_major)
    state.ax.set_xticks(x_ticks_minor, minor=True)
    x_labels = [f'+{x:.2f}' if x > 0 else f'{x:.2f}' for x in x_ticks_major]
    state.ax.set_xticklabels(x_labels, fontsize=8)
    state.ax.set_yscale('log')
    state.ax.set_ylim(1, 1e7)
    y_ticks = [10**i for i in range(8)]
    state.ax.set_yticks(y_ticks)
    state.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1E}'))
    state.ax.yaxis.set_minor_formatter(plt.NullFormatter())
    state.ax.set_xlabel('')
    state.ax.set_ylabel('')
    state.ax.tick_params(axis='y', labelsize=6)
    state.ax.grid(True, which='minor', linestyle='-', alpha=0.4)
    state.canvas_plot.draw()