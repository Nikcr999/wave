"""
Main window setup module.
Contains functions to create and set up the main application window.
"""
import tkinter as tk

def create_main_window():
    """
    Create and return the main application window
    
    Returns:
        tk.Tk: Main window object
    """
    root = tk.Tk()
    root.title("Cell Distribution Analysis")
    root.configure(bg='white')
    return root