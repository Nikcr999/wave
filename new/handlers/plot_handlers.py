"""
Plot handlers module for functions related to plotting data.
Contains functions for plotting, configuring, and clearing plots.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import state
from data.file_reader import read_data_for_key, extract_block_info
from data.pattern_analysis import analyze_all_selected_data
from handlers.mark_handlers import restore_marks
from ui.table import update_percentage_row

def configure_plot():
    """
    Configure the plot with additional settings like legend
    """
    from ui.plot import configure_initial_plot
    configure_initial_plot()
    
    if state.plot_lines:
        state.ax.legend(
            bbox_to_anchor=(0.5, -0.5), 
            loc='center', 
            ncol=len(state.plot_lines),
            borderaxespad=0,
            frameon=False
        )

def plot_data():
    """
    Plot data from selected keys
    """
    # Get resolution
    try:
        resolution = int(state.resolution_var.get()) / 1000
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    # Get all selected keys from checkboxes
    selected_keys = [(key, var.get()) for key, var in state.checkboxes.items()]
    selected_keys = [key for key, checked in selected_keys if checked]
    
    if not selected_keys:
        # No popup message, just clear plots
        clear_plots()
        return
    
    # Save current marks to restore after plot
    current_marks = state.marked_points.copy()
    
    # Clear existing plot
    state.ax.clear()
    state.plot_lines.clear()
    
    # Generate colors for each line
    colors = cm.rainbow(np.linspace(0, 1, len(selected_keys)))
    
    # Track the last checked key - this will be the one that determines the table title
    last_checked_key = selected_keys[-1]  # Get the last item in the list
    state.last_selected_key = last_checked_key  # Store for pattern analysis
    
    # Update the table title with the block name of the last checked item
    if hasattr(state, 'table_title_label') and state.table_title_label:
        key_parts = last_checked_key.split('|')
        if len(key_parts) >= 2:
            file_idx = int(key_parts[0])
            if len(state.file_paths) > file_idx:
                # Find the actual block name from the file
                with open(state.file_paths[file_idx], 'r') as file:
                    for line in file:
                        if any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
                            block_name = extract_block_info(line)
                            state.table_title_label.config(text=block_name)
                            break
    
    # Calculate and display percentage for the last checked item
    data = read_data_for_key(last_checked_key)
    if data:
        # Calculate some percentage based on the data
        percentage = sum(data) / len(data) / 100
        update_percentage_row(percentage)
    
    # Plot each selected dataset
    for idx, key in enumerate(selected_keys):
        data = read_data_for_key(key)
        if data:
            x = np.arange(-2.4, -2.4 + len(data) * resolution, resolution)
            
            # Extract data key from composite key (file_idx|data_key)
            key_parts = key.split('|')
            if len(key_parts) >= 2:
                data_key = key_parts[1]
                data_key_parts = data_key.split('_')
                
                if len(data_key_parts) >= 3:
                    key_type = data_key_parts[0]
                    if key_type == 'w':
                        label = f"WLS:{data_key_parts[1]}, SSL:{data_key_parts[2]}"
                    elif key_type == 'd':
                        label = f"DUMMY:{data_key_parts[1]}, SSL:{data_key_parts[2]}"
                    else:
                        label = f"CDUMMY:{data_key_parts[1]}, SSL:{data_key_parts[2]}"
                else:
                    label = data_key
            else:
                label = key
            
            line, = state.ax.plot(x, data, '-', label=label, color=colors[idx])
            state.plot_lines[key] = line
    
    # Configure plot with legend
    configure_plot()
    
    # Restore marked points
    state.marked_points = []
    restore_marks(current_marks)
    
    # Draw the plot
    state.canvas_plot.draw()
    
    # Analyze all selected data for pattern analysis
    analyze_all_selected_data(selected_keys)

def clear_plots():
    """
    Clear all plots and related data
    """
    state.ax.clear()
    state.plot_lines.clear()
    state.marked_points.clear()
    
    from ui.plot import configure_initial_plot
    configure_initial_plot()
    
    # Reset the last selected key
    state.last_selected_key = None
    
    # Clear the pattern analysis table
    from ui.table import clear_pattern_analysis
    clear_pattern_analysis()
    
    # Update the table title to default
    if hasattr(state, 'table_title_label') and state.table_title_label:
        state.table_title_label.config(text="Table Title")
    
    # Update the percentage row to show empty or default message
    update_percentage_row(None)
        
    # Clear all checkbox selections
    for var in state.checkboxes.values():
        var.set(False)