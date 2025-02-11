import tkinter as tk
from tkinter import ttk

def setup_sidebar(self):
    self.sidebar = ttk.Frame(self.main_container, padding="5")
    self.main_container.add(self.sidebar)
    self.canvas = tk.Canvas(self.sidebar, width=200)
    self.scrollbar = ttk.Scrollbar(self.sidebar, orient="vertical", command=self.canvas.yview)
    self.scrollable_frame = ttk.Frame(self.canvas)

    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    )

    self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    ttk.Label(self.sidebar, text="Available Combinations").pack()
    self.canvas.pack(side="left", fill="both", expand=True)
    self.scrollbar.pack(side="right", fill="y")
