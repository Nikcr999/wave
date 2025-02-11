import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from ui_setup import setup_ui
from sidebar_setup import setup_sidebar
from plot import setup_plot, plot_manual, plot_selected, clear_plots
from read import load_file, parse_file
from mark import onclick, undo_mark, clear_marks
from hover import on_hover, find_nearest

class CellDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cell Distribution Analysis")
        self.file_path = None
        self.data = {}
        self.marked_points = []
        self.hover_text = None
        self.plot_lines = {}  
        self.checkboxes = {}
        
        # Bind all external functions to the instance
        self.load_file = lambda: load_file(self)
        self.parse_file = lambda: parse_file(self)
        self.plot_manual = lambda: plot_manual(self)
        self.plot_selected = lambda: plot_selected(self)
        self.clear_plots = lambda: clear_plots(self)
        self.onclick = lambda event: onclick(self, event)
        self.undo_mark = lambda: undo_mark(self)
        self.clear_marks = lambda: clear_marks(self)
        self.on_hover = lambda event: on_hover(self, event)
        self.find_nearest = lambda x_click: find_nearest(self, x_click)
        
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        setup_sidebar(self)
        self.content_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.content_frame)
        
        setup_ui(self)
        setup_plot(self)

    def update_checkboxes(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkboxes.clear()
        for wls, ssl in sorted(self.data.keys()):
            var = tk.BooleanVar()
            self.checkboxes[(wls, ssl)] = var
            ttk.Checkbutton(
                self.scrollable_frame,
                text=f"WLS: {wls}, SSL: {ssl}",
                variable=var,
                command=self.plot_selected
            ).pack(anchor="w", padx=5, pady=2)