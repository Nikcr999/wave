"""
Help tab module for setting up the help tab.
Contains functions to create and set up the help tab.
"""
import tkinter as tk
from tkinter import ttk

import state

def setup_help_tab():
    """
    Set up the help tab
    """
    notebook = state.tab3
    
    help_content = ttk.Label(
        notebook, 
        text="Help Section Coming Soon!",
        font=('Helvetica', 12)
    )
    help_content.pack(pady=20)
    
    # Could add more help content here in the future
    
    return help_content