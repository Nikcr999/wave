"""
Buttons module for creating the application's control buttons.
"""
import tkinter as tk
from tkinter import ttk

from data.file_reader import load_file
from handlers.mark_handlers import undo_mark, clear_marks
from handlers.plot_handlers import clear_plots
from handlers.ui_handlers import show_manual_input

def create_button_panel(parent):
    """
    Create the button panel with control buttons
    
    Args:
        parent: Parent frame to add buttons to
        
    Returns:
        ttk.Frame: Button frame
    """
    button_frame = ttk.Frame(parent, style='TFrame')
    button_frame.pack(fill=tk.X, padx=5, pady=5)
    
    buttons = [
        ("Load", load_file),
        ("Manual\nInput", show_manual_input),
        ("Undo\nMark", undo_mark),
        ("Clear\nMarks", clear_marks),
        ("Clear\nPlots", clear_plots)
    ]
    
    for text, command in buttons:
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            bg='#ff9900',
            fg='black',
            font=('Helvetica', 9),
            height=2,
            width=8,
            relief='raised',
            borderwidth=1
        )
        btn.pack(side=tk.LEFT, padx=2)
    
    return button_frame