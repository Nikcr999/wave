import tkinter as tk
from tkinter import ttk

def setup_sidebar(self):
    self.sidebar = ttk.Frame(self.main_container, padding="2", style='TFrame')
    self.main_container.add(self.sidebar)
    
    # Add header
    ttk.Label(
        self.sidebar, 
        text="Block List", 
        style='TLabel'
    ).pack(anchor=tk.W, padx=2)
    
    # Create content frame to hold everything
    content_frame = ttk.Frame(self.sidebar, style='TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Frame for scroll components
    scroll_frame = ttk.Frame(content_frame, style='TFrame')
    scroll_frame.pack(fill=tk.BOTH, expand=True)
    
    # Canvas for scrollable content
    self.canvas = tk.Canvas(
        scroll_frame, 
        bg='white',
        highlightthickness=0,
        width=200
    )
    
    # Vertical scrollbar
    y_scrollbar = ttk.Scrollbar(
        scroll_frame,
        orient=tk.VERTICAL,
        command=self.canvas.yview
    )
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Bottom frame for horizontal scrollbar and toggle button
    bottom_frame = ttk.Frame(content_frame, style='TFrame')
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(
        bottom_frame,
        orient=tk.HORIZONTAL,
        command=self.canvas.xview
    )
    x_scrollbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Toggle button
    self.sidebar_expanded = True
    self.toggle_btn = tk.Button(
        bottom_frame,
        text="◄",
        command=lambda: self.toggle_sidebar(),
        bg='#d3d3d3',
        fg='black',
        font=('Arial', 8),
        width=2,
        height=1,
        relief='solid',
        bd=1
    )
    self.toggle_btn.pack(side=tk.RIGHT)
    
    # Position and configure canvas
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Create frame that will contain all the checkboxes
    self.scrollable_frame = ttk.Frame(self.canvas, style='TFrame')

    # Create window in canvas that will display the scrollable frame
    self.canvas_window = self.canvas.create_window(
        (0, 0),
        window=self.scrollable_frame,
        anchor="nw",
        width=self.canvas.winfo_width()
    )
    
    # Update scrollable frame width when canvas is resized
    def update_scrolled_frame_width(event):
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
    
    self.canvas.bind('<Configure>', update_scrolled_frame_width)
    
    # Update scrollregion when the size of scrollable_frame changes
    def update_scrollregion(event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    self.scrollable_frame.bind("<Configure>", update_scrollregion)
    
    # Configure scrollbar commands
    self.canvas.configure(
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set
    )
    
    # Dictionary to store checkbox variables
    self.checkboxes = {}
