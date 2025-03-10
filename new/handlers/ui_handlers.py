"""
UI handlers module for functions related to UI interactions.
Contains functions for handling various UI events and interactions.
"""
import tkinter as tk
from tkinter import ttk

import state
from handlers.plot_handlers import plot_data

def show_manual_input():
    """
    Show manual input dialog for entering data manually
    """
    if state.input_dialog is None or not tk.Toplevel.winfo_exists(state.input_dialog):
        state.input_dialog = tk.Toplevel(state.root)
        state.input_dialog.title("Manual Input")
        state.input_dialog.geometry("400x200")
        state.input_dialog.configure(bg='white')
        
        input_frame = ttk.Frame(state.input_dialog, padding="20", style='TFrame')
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        row1_frame = ttk.Frame(input_frame, style='TFrame')
        row1_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row1_frame, text="Resolution (mV):", width=12).pack(side=tk.LEFT)
        ttk.Entry(row1_frame, textvariable=state.resolution_var, width=10).pack(side=tk.LEFT, padx=(0,10))
        ttk.Label(row1_frame, text="WLS:", width=6).pack(side=tk.LEFT)
        ttk.Entry(row1_frame, textvariable=state.wls_var, width=10).pack(side=tk.LEFT, padx=(0,10))
        ttk.Label(row1_frame, text="DUMMY:", width=8).pack(side=tk.LEFT)
        ttk.Entry(row1_frame, textvariable=state.dummy_var, width=10).pack(side=tk.LEFT)
        
        row2_frame = ttk.Frame(input_frame, style='TFrame')
        row2_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row2_frame, text="CDUMMY:", width=12).pack(side=tk.LEFT)
        ttk.Entry(row2_frame, textvariable=state.cdummy_var, width=10).pack(side=tk.LEFT, padx=(0,10))
        ttk.Label(row2_frame, text="SSL:", width=6).pack(side=tk.LEFT)
        ttk.Entry(row2_frame, textvariable=state.ssl_var, width=10).pack(side=tk.LEFT)
        
        plot_btn = tk.Button(
            input_frame, 
            text="Plot",
            command=lambda: [plot_data(), state.input_dialog.destroy()],
            bg='#ff9900',
            fg='white',
            font=('Helvetica', 9),
            height=2,
            width=8,
            relief='raised',
            borderwidth=2
        )
        plot_btn.pack(pady=20)