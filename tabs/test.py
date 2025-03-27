import tkinter as tk  # Import Tkinter for GUI creation
from tkinter import ttk  # Import themed Tkinter widgets for modern look
import os  # Import OS module (though not used in this snippet)

import state  # Import a custom state management module
from data.file_reader import extract_blocks_from_file  # Import function to extract data blocks from files
from handlers.plot_handlers import plot_data  # Import function to update plot based on selected items

# Create a set to track which file paths have already been processed to prevent duplicate block creation
loaded_file_paths = set()

def create_sidebar():
    # Create the main sidebar frame within the main container
    # Uses ttk.Frame for a themed appearance with padding
    state.sidebar = ttk.Frame(state.main_container, padding="2", style='TFrame')
    
    # Add the sidebar to the main container with a fixed width of 250 pixels
    state.main_container.add(state.sidebar, width=250)
    
    # Create a header label for the sidebar
    # Anchored to the west (left) with a small horizontal padding
    ttk.Label(
        state.sidebar, 
        text="Block List", 
        style='TLabel'
    ).pack(anchor=tk.W, padx=2)
    
    # Create a content frame to hold scrollbars and canvas
    # Packed to fill both horizontal and vertical space and expand
    content_frame = ttk.Frame(state.sidebar, style='TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a vertical scrollbar
    # Packed to the right side and filled vertically
    y_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create a horizontal scrollbar
    # Packed to the bottom and filled horizontally
    x_scrollbar = ttk.Scrollbar(content_frame, orient=tk.HORIZONTAL)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Create a canvas for scrollable content
    # Uses white background, removes highlight border
    # Connects scrollbars to canvas scroll commands
    state.canvas = tk.Canvas(
        content_frame, 
        bg='white',
        highlightthickness=0,
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set
    )
    state.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure scrollbar commands to control canvas scrolling
    y_scrollbar.config(command=state.canvas.yview)
    x_scrollbar.config(command=state.canvas.xview)
    
    # Create a scrollable frame inside the canvas
    # This frame will contain the actual content (checkboxes)
    state.scrollable_frame = ttk.Frame(state.canvas, style='TFrame')
    
    # Create a window inside the canvas to host the scrollable frame
    # Anchored to the northwest (top-left) corner
    state.canvas.create_window((0, 0), window=state.scrollable_frame, anchor="nw")
    
    # Bind a configuration event to update scroll region when frame changes
    # Ensures scrollbars work correctly as content is added
    state.scrollable_frame.bind(
        "<Configure>", 
        lambda e: state.canvas.configure(scrollregion=state.canvas.bbox("all"))
    )
    
    # Return the created sidebar
    return state.sidebar

def update_checkboxes():
    # Use global to modify the loaded_file_paths set
    global loaded_file_paths
    
    # Iterate through file paths stored in state
    for file_idx, file_path in enumerate(state.file_paths):
        # Skip files that have already been processed
        if file_path in loaded_file_paths:
            continue
        
        # Extract blocks (data groups) from the current file
        blocks = extract_blocks_from_file(file_idx, file_path)
        
        # Create a block (with checkboxes) for each block of data
        for block_name, items in blocks.items():
            create_block(state.scrollable_frame, block_name, items)
        
        # Mark this file path as processed
        loaded_file_paths.add(file_path)

def create_block(parent, block_name, items):
    # Create a frame for the entire block
    block_frame = ttk.Frame(parent, style='TFrame')
    block_frame.pack(fill=tk.X, anchor=tk.W, pady=2)
    
    # Create a header frame for block title and toggle button
    header_frame = ttk.Frame(block_frame, style='TFrame')
    header_frame.pack(fill=tk.X)
    
    # Create an items frame to hold individual checkboxes (initially not packed)
    items_frame = ttk.Frame(block_frame, style='TFrame')
    
    # Create a toggle button to expand/collapse the block
    toggle_btn = tk.Button(
        header_frame,
        text="+",
        width=2,
        font=('Arial', 8, 'bold'),
        bg='white',
        relief='flat',
        command=lambda: _toggle_block(toggle_btn, items_frame)
    )
    toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    # Create a "select all" checkbox for the block
    select_all_var = tk.BooleanVar()
    select_all_cb = ttk.Checkbutton(
        header_frame,
        text=block_name,
        variable=select_all_var,
        style='Checkbox.TCheckbutton',
        command=lambda: _toggle_all_items(select_all_var, item_vars)
    )
    select_all_cb.pack(side=tk.LEFT, padx=5)
    
    # List to store individual item checkbox variables
    item_vars = []
    
    # Create individual checkboxes for each item in the block
    for key, label in items:
        # Create a boolean variable for each checkbox
        var = tk.BooleanVar()
        
        # Store the variable in the global state for tracking
        state.checkboxes[key] = var
        item_vars.append(var)
        
        # Create the checkbox
        checkbox = ttk.Checkbutton(
            items_frame,
            text=label,
            variable=var,
            command=lambda v=var, vars=item_vars, all_var=select_all_var: _item_toggled(v, vars, all_var),
            style='Checkbox.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W, padx=(20, 0))

def _toggle_block(btn, frame):
    """Toggle block expanded/collapsed state"""
    if frame.winfo_manager():
        # If frame is currently packed (expanded), collapse it
        btn.config(text="+")
        frame.pack_forget()
    else:
        # If frame is not packed (collapsed), expand it
        btn.config(text="-")
        frame.pack(fill=tk.X)

def _toggle_all_items(all_var, vars_list):
    """Toggle all checkboxes in a block based on "select all" state"""
    # Set all individual checkboxes to match the "select all" checkbox state
    for var in vars_list:
        var.set(all_var.get())
    
    # Update the plot to reflect the new selection
    plot_data()

def _item_toggled(changed_var, all_vars, all_cb_var):
    """Handle individual checkbox toggle"""
    # Check if all checkboxes in the block are selected
    all_selected = all(var.get() for var in all_vars)
    
    # Update the "select all" checkbox accordingly
    all_cb_var.set(all_selected)
    
    # Update the plot to reflect the new selection
    plot_data()