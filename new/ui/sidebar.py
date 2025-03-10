"""
Sidebar module for creating and managing the sidebar with checkboxes.
"""
import tkinter as tk
from tkinter import ttk

import state
from data.file_reader import extract_blocks_from_file
from handlers.plot_handlers import plot_data

def create_sidebar():
    """
    Create the sidebar container and widgets
    
    Returns:
        ttk.Frame: Sidebar frame
    """
    # Create sidebar frame
    state.sidebar = ttk.Frame(state.main_container, padding="2", style='TFrame')
    state.main_container.add(state.sidebar)
    
    # Create header label
    ttk.Label(
        state.sidebar, 
        text="Block List", 
        style='TLabel'
    ).pack(anchor=tk.W, padx=2)
    
    # Create content frame
    content_frame = ttk.Frame(state.sidebar, style='TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create scroll frame
    scroll_frame = ttk.Frame(content_frame, style='TFrame')
    scroll_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create canvas for scrolling
    state.canvas = tk.Canvas(
        scroll_frame, 
        bg='white',
        highlightthickness=0,
        width=200  # Width for longer block names
    )
    
    # Create vertical scrollbar
    y_scrollbar = ttk.Scrollbar(
        scroll_frame,
        orient=tk.VERTICAL,
        command=state.canvas.yview
    )
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create bottom frame for horizontal controls
    bottom_frame = ttk.Frame(content_frame, style='TFrame')
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Create center frame for horizontal scrollbar and toggle button
    center_frame = ttk.Frame(bottom_frame, style='TFrame')
    center_frame.pack(fill=tk.X)
    
    # Create horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(
        center_frame,
        orient=tk.HORIZONTAL,
        command=state.canvas.xview
    )
    x_scrollbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Create toggle button
    state.toggle_btn = tk.Button(
        center_frame,
        text="◄",
        command=toggle_sidebar,
        bg='#d3d3d3',
        fg='black',
        font=('Arial', 8),
        width=2,
        height=1,
        relief='solid',
        bd=1
    )
    state.toggle_btn.pack(side=tk.LEFT)
    
    # Setup canvas and scrollable frame
    state.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    state.scrollable_frame = ttk.Frame(state.canvas, style='TFrame')
    
    # Create window in canvas for scrollable content
    state.canvas.create_window(
        (0, 0),
        window=state.scrollable_frame,
        anchor="nw"
    )
    
    # Configure scroll region when frame size changes
    state.scrollable_frame.bind(
        "<Configure>",
        lambda e: state.canvas.configure(scrollregion=state.canvas.bbox("all"))
    )
    
    # Connect scrollbars to canvas
    state.canvas.configure(
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set
    )
    
    return state.sidebar

def update_checkboxes():
    """
    Update checkbox list based on loaded files
    """
    # Clear existing checkboxes
    for widget in state.scrollable_frame.winfo_children():
        widget.destroy()
    state.checkboxes.clear()
    
    # Create container frame
    container_frame = ttk.Frame(state.scrollable_frame, style='TFrame')
    container_frame.pack(fill=tk.BOTH, expand=True)
    
    # Process each file and create blocks
    for file_idx, file_path in enumerate(state.file_paths):
        # Extract blocks from the file
        blocks = extract_blocks_from_file(file_idx, file_path)
        
        # Add each block to the container
        for block_name, items in blocks.items():
            create_block(container_frame, block_name, items)

def create_block(parent, block_name, items):
    """
    Create a collapsible block of checkboxes for a data block
    
    Args:
        parent: Parent frame to add the block to
        block_name: Name of the block
        items: List of (key, label) tuples for items in the block
    """
    # Create block frame
    block_frame = ttk.Frame(parent, style='TFrame')
    block_frame.pack(fill=tk.X, anchor=tk.W, pady=2)
    
    # Create header and items frames
    header_frame = ttk.Frame(block_frame, style='TFrame')
    header_frame.pack(fill=tk.X)
    
    items_frame = ttk.Frame(block_frame, style='TFrame')
    
    # Create toggle button for expanding/collapsing
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
    
    # Create "select all" checkbox
    select_all_var = tk.BooleanVar()
    select_all_cb = ttk.Checkbutton(
        header_frame,
        text=block_name,
        variable=select_all_var,
        style='Checkbox.TCheckbutton',
        command=lambda: _toggle_all_items(select_all_var, item_vars)
    )
    select_all_cb.pack(side=tk.LEFT, padx=5)
    
    # Create checkboxes for each item
    item_vars = []
    for key, label in items:
        var = tk.BooleanVar()
        state.checkboxes[key] = var
        item_vars.append(var)
        checkbox = ttk.Checkbutton(
            items_frame,
            text=label,
            variable=var,
            command=lambda v=var: _item_toggled(v, item_vars, select_all_var),
            style='Checkbox.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W, padx=(20, 0))

def toggle_sidebar():
    """
    Toggle sidebar expanded/collapsed state
    """
    if state.sidebar_expanded:
        # Collapse sidebar
        state.main_container.forget(state.sidebar)
        state.main_container.add(state.sidebar, width=30)
        state.toggle_btn.configure(text="►")
        state.canvas.pack_forget()
        state.sidebar_expanded = False
    else:
        # Expand sidebar
        state.main_container.forget(state.sidebar)
        state.main_container.add(state.sidebar, width=200)
        state.toggle_btn.configure(text="◄")
        state.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        state.sidebar_expanded = True

# Helper functions with underscore prefix (private)
def _toggle_block(btn, frame):
    """Toggle block expanded/collapsed state"""
    if frame.winfo_manager():
        # Collapse
        btn.config(text="+")
        frame.pack_forget()
    else:
        # Expand
        btn.config(text="-")
        frame.pack(fill=tk.X)

def _toggle_all_items(all_var, vars_list):
    """Toggle all checkboxes in a block based on "select all" state"""
    for var in vars_list:
        var.set(all_var.get())
    
    # Update plot
    plot_data()

def _item_toggled(changed_var, all_vars, all_cb_var):
    """Handle individual checkbox toggle"""
    # Update "select all" checkbox state
    all_selected = all(var.get() for var in all_vars)
    all_cb_var.set(all_selected)
    
    # Update plot
    plot_data()