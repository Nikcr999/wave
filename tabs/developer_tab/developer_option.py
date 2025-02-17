import tkinter as tk
from tkinter import ttk

class DeveloperOptionTab(ttk.Frame):
    def __init__(self, notebook, main_app):
        super().__init__(notebook)
        self.main_app = main_app
        
        # Create a frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add title
        title_label = ttk.Label(
            main_frame, 
            text="Developer Options",
            font=('Helvetica', 12, 'bold')
        )
        title_label.pack(pady=10)
        
        # Add development settings and tools here
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(
            main_frame,
            text="Enable Debug Mode",
            variable=self.debug_var,
            command=self.toggle_debug
        )
        debug_check.pack(anchor=tk.W, pady=5)
        
        # Resolution adjustment
        resolution_frame = ttk.LabelFrame(main_frame, text="Resolution Settings", padding="5")
        resolution_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(resolution_frame, text="Custom Resolution (mV):").pack(side=tk.LEFT, padx=5)
        self.custom_resolution = ttk.Entry(resolution_frame, width=10)
        self.custom_resolution.pack(side=tk.LEFT, padx=5)
        self.custom_resolution.insert(0, "40")
        
        ttk.Button(
            resolution_frame,
            text="Apply",
            command=self.apply_custom_resolution
        ).pack(side=tk.LEFT, padx=5)

    def toggle_debug(self):
        if self.debug_var.get():
            print("Debug mode enabled")
        else:
            print("Debug mode disabled")

    def apply_custom_resolution(self):
        try:
            resolution = float(self.custom_resolution.get())
            self.main_app.resolution_var.set(str(int(resolution)))
            print(f"Resolution updated to {resolution}mV")
        except ValueError:
            print("Invalid resolution value")