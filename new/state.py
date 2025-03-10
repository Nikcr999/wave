"""
Global state module for the Cell Distribution Analysis application.
Contains all shared state variables used across the application.
"""
import tkinter as tk

# Data state
plot_lines = {}  
marked_points = []
hover_elements = {'text': None, 'line': None}
file_paths = []
data_point_length = None  # Length of data points for optimization
pattern_data = {}  # Pattern analysis data
last_selected_key = None  # Last selected key for analysis

# UI state
checkboxes = {}
sidebar_expanded = True
input_dialog = None

# UI tkinter variables
resolution_var = None
wls_var = None
dummy_var = None
cdummy_var = None
ssl_var = None

# Configuration
wls_max_value = 175  # Default max WLS value
debug_mode = False

# UI element references
root = None
fig = None
ax = None
canvas_plot = None
sidebar = None
toggle_btn = None
canvas = None
scrollable_frame = None
main_container = None
tab1 = None
tab2 = None
tab3 = None
table_title_label = None
analysis_frame = None
analysis_container = None
plot_title = None
lower_box = None
notebook = None

def init():
    """Initialize or reset the global state"""
    global plot_lines, marked_points, hover_elements, file_paths
    global checkboxes, sidebar_expanded, pattern_data, last_selected_key
    global resolution_var, wls_var, dummy_var, cdummy_var, ssl_var
    
    # Reset data state
    plot_lines = {}
    marked_points = []
    hover_elements = {'text': None, 'line': None}
    file_paths = []
    data_point_length = None
    pattern_data = {}
    last_selected_key = None
    
    # Reset UI state
    checkboxes = {}
    sidebar_expanded = True
    
    # Initialize tkinter variables
    if root is not None:  # Only if tk.Tk() has been initialized
        resolution_var = tk.StringVar(value="40")
        wls_var = tk.StringVar()
        dummy_var = tk.StringVar()
        cdummy_var = tk.StringVar()
        ssl_var = tk.StringVar()

def cleanup():
    """Clean up resources when application is closing"""
    global fig, ax, canvas_plot
    
    # Clean up matplotlib resources if they exist
    if fig is not None:
        import matplotlib.pyplot as plt
        plt.close(fig)
        fig = None
        ax = None
        canvas_plot = None