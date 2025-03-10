"""
Notebook setup module.
Contains functions to create and set up the application's tabbed interface.
"""
import tkinter as tk
from tkinter import ttk

import state

def setup_notebook(root):
    """
    Create and return the notebook with tabs
    
    Args:
        root: Root window object
        
    Returns:
        tuple: (notebook, tab1, tab2, tab3)
    """
    style = ttk.Style()
    style.configure("TNotebook", background="white", borderwidth=0)
    style.configure("TNotebook.Tab", padding=[10, 2], font=('Helvetica', 9), borderwidth=0)
    style.map("TNotebook.Tab",
             background=[("selected", "white"), ("!selected", "white")],
             foreground=[("selected", "#000000"), ("!selected", "#000000")])
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    tab1 = ttk.Frame(notebook, style='TFrame')
    tab2 = ttk.Frame(notebook, style='TFrame')
    tab3 = ttk.Frame(notebook, style='TFrame')
    
    notebook.add(tab1, text="Load")
    notebook.add(tab2, text="Developer Option")
    notebook.add(tab3, text="Help")
    
    # Create indicator for selected tab
    indicator_frame = tk.Frame(root, height=3, bg="white")
    indicator_frame.pack(fill=tk.X, padx=0, pady=0)
    indicator = tk.Frame(indicator_frame, height=3, width=50, bg="#ff9900")
    indicator.place(x=25, y=0)
    
    # Set up tab change event
    notebook.bind("<<NotebookTabChanged>>", lambda event: on_tab_changed(event, indicator_frame, indicator))
    
    return notebook, tab1, tab2, tab3

def on_tab_changed(event, indicator_frame, indicator):
    """
    Handle tab changed event
    
    Args:
        event: Event object
        indicator_frame: Frame containing the indicator
        indicator: Indicator widget
    """
    notebook = event.widget
    tab_id = notebook.select()
    tab_index = notebook.index(tab_id)
    
    tab_width = 50 if tab_index == 0 else 120 if tab_index == 1 else 45
    x_pos = 25 if tab_index == 0 else 85 if tab_index == 1 else 215
    
    indicator.place_forget()
    indicator = tk.Frame(indicator_frame, height=3, width=tab_width, bg="#ff9900")
    indicator.place(x=x_pos, y=0)