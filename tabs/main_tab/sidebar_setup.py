import tkinter as tk
from tkinter import ttk

def setup_sidebar(self):
    self.sidebar = ttk.Frame(self.main_container, padding="2", style='TFrame')
    self.main_container.add(self.sidebar)
    
    ttk.Label(
        self.sidebar, 
        text="Block List", 
        style='TLabel'
    ).pack(anchor=tk.W, padx=2)
    
    content_frame = ttk.Frame(self.sidebar, style='TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    scroll_frame = ttk.Frame(content_frame, style='TFrame')
    scroll_frame.pack(fill=tk.BOTH, expand=True)
    
    self.canvas = tk.Canvas(
        scroll_frame, 
        bg='white',
        highlightthickness=0,
        width=150
    )
    
    # Vertical scrollbar on the right
    y_scrollbar = ttk.Scrollbar(
        scroll_frame,
        orient=tk.VERTICAL,
        command=self.canvas.yview
    )
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Bottom frame for horizontal scrollbar and toggle button
    bottom_frame = ttk.Frame(content_frame, style='TFrame')
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Frame to center the toggle button
    center_frame = ttk.Frame(bottom_frame, style='TFrame')
    center_frame.pack(fill=tk.X)
    
    x_scrollbar = ttk.Scrollbar(
        center_frame,
        orient=tk.HORIZONTAL,
        command=self.canvas.xview
    )
    x_scrollbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    self.sidebar_expanded = True
    self.toggle_btn = tk.Button(
        center_frame,
        text="◄",
        command=self.toggle_sidebar,
        bg='#d3d3d3',
        fg='black',
        font=('Arial', 8),
        width=2,
        height=1,
        relief='solid',
        bd=1
    )
    self.toggle_btn.pack(side=tk.LEFT)
    
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.scrollable_frame = ttk.Frame(self.canvas, style='TFrame')
    
    self.canvas.create_window(
        (0, 0),
        window=self.scrollable_frame,
        anchor="nw"
    )
    
    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    )
    
    self.canvas.configure(
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set
    )