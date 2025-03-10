"""
Developer tab module for setting up the developer options tab.
Contains functions to create and set up the developer options tab.
"""
import tkinter as tk
from tkinter import ttk, messagebox

import state
from ui.sidebar import update_checkboxes

def setup_developer_tab():
    """
    Set up the developer options tab
    """
    notebook = state.tab2
    
    main_frame = ttk.Frame(notebook, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title_label = ttk.Label(
        main_frame, 
        text="Developer Options",
        font=('Helvetica', 12, 'bold')
    )
    title_label.pack(pady=10)
    
    # Debug mode checkbox
    debug_var = tk.BooleanVar(value=state.debug_mode)
    debug_check = ttk.Checkbutton(
        main_frame,
        text="Enable Debug Mode",
        variable=debug_var,
        command=lambda: toggle_debug(debug_var)
    )
    debug_check.pack(anchor=tk.W, pady=5)
    
    # Resolution adjustment
    resolution_frame = ttk.LabelFrame(main_frame, text="Resolution Settings", padding="5")
    resolution_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(resolution_frame, text="Custom Resolution (mV):").pack(side=tk.LEFT, padx=5)
    custom_resolution = ttk.Entry(resolution_frame, width=10)
    custom_resolution.pack(side=tk.LEFT, padx=5)
    custom_resolution.insert(0, state.resolution_var.get())
    
    ttk.Button(
        resolution_frame,
        text="Apply",
        command=lambda: apply_custom_resolution(custom_resolution)
    ).pack(side=tk.LEFT, padx=5)

    # WLS Range adjustment
    wls_frame = ttk.LabelFrame(main_frame, text="WLS Range Settings", padding="5")
    wls_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(wls_frame, text="Max WLS Value:").pack(side=tk.LEFT, padx=5)
    max_wls = ttk.Entry(wls_frame, width=10)
    max_wls.pack(side=tk.LEFT, padx=5)
    max_wls.insert(0, str(state.wls_max_value))
    
    ttk.Button(
        wls_frame,
        text="Apply",
        command=lambda: apply_wls_range(max_wls)
    ).pack(side=tk.LEFT, padx=5)

def toggle_debug(debug_var):
    """
    Toggle debug mode
    
    Args:
        debug_var: BooleanVar for debug mode
    """
    state.debug_mode = debug_var.get()
    if state.debug_mode:
        print("Debug mode enabled")
    else:
        print("Debug mode disabled")

def apply_custom_resolution(resolution_entry):
    """
    Apply custom resolution setting
    
    Args:
        resolution_entry: Entry widget containing resolution value
    """
    try:
        resolution = float(resolution_entry.get())
        state.resolution_var.set(str(int(resolution)))
        print(f"Resolution updated to {resolution}mV")
    except ValueError:
        messagebox.showerror("Error", "Invalid resolution value")

def apply_wls_range(max_wls_entry):
    """
    Apply WLS range setting
    
    Args:
        max_wls_entry: Entry widget containing max WLS value
    """
    try:
        max_wls = int(max_wls_entry.get())
        if max_wls <= 0:
            raise ValueError("WLS value must be positive")
            
        # Update WLS range 
        state.wls_max_value = max_wls
        
        # Update checkboxes with new range
        update_checkboxes()
        
        messagebox.showinfo("Success", f"WLS range updated to 0-{max_wls}")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid WLS value: {str(e)}")