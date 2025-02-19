import tkinter as tk
from tkinter import ttk

def setup_ui(self):
    input_frame = ttk.Frame(self.content_frame, padding="5")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Resolution (mV):").pack(side=tk.LEFT)
    self.resolution_var = tk.StringVar(value="40")
    ttk.Entry(input_frame, textvariable=self.resolution_var, width=10).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(input_frame, text="WLS:").pack(side=tk.LEFT)
    self.wls_var = tk.StringVar()
    ttk.Entry(input_frame, textvariable=self.wls_var, width=10).pack(side=tk.LEFT, padx=5)

    ttk.Label(input_frame, text="DUMMY:").pack(side=tk.LEFT)
    self.dummy_var = tk.StringVar()
    ttk.Entry(input_frame, textvariable=self.dummy_var, width=10).pack(side=tk.LEFT, padx=5)

    ttk.Label(input_frame, text="CDUMMY:").pack(side=tk.LEFT)
    self.cdummy_var = tk.StringVar()
    ttk.Entry(input_frame, textvariable=self.cdummy_var, width=10).pack(side=tk.LEFT, padx=5)

    ttk.Label(input_frame, text="SSL:").pack(side=tk.LEFT)
    self.ssl_var = tk.StringVar()
    ttk.Entry(input_frame, textvariable=self.ssl_var, width=10).pack(side=tk.LEFT, padx=5)

    button_frame = ttk.Frame(self.content_frame, padding="5")
    button_frame.pack(fill=tk.X)

    ttk.Button(button_frame, text="Browse", command=self.load_file).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Plot", command=self.plot_data).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Undo Mark", command=self.undo_mark).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear Marks", command=self.clear_marks).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear Plots", command=self.clear_plots).pack(side=tk.LEFT, padx=5)