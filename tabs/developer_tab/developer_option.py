import tkinter as tk
from tkinter import ttk, messagebox

class DeveloperOptionTab(ttk.Frame):
    def __init__(self, notebook, main_app):
        super().__init__(notebook)
        self.main_app = main_app
        
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame, 
            text="Developer Options",
            font=('Helvetica', 12, 'bold')
        )
        title_label.pack(pady=10)
        
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

        # WLS Range adjustment
        wls_frame = ttk.LabelFrame(main_frame, text="WLS Range Settings", padding="5")
        wls_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(wls_frame, text="Max WLS Value:").pack(side=tk.LEFT, padx=5)
        self.max_wls = ttk.Entry(wls_frame, width=10)
        self.max_wls.pack(side=tk.LEFT, padx=5)
        self.max_wls.insert(0, "175")
        
        ttk.Button(
            wls_frame,
            text="Apply",
            command=self.apply_wls_range
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
            messagebox.showerror("Error", "Invalid resolution value")

    def apply_wls_range(self):
        try:
            max_wls = int(self.max_wls.get())
            if max_wls <= 0:
                raise ValueError("WLS value must be positive")
                
            # Update WLS range in read.py
            self.main_app.wls_max_value = max_wls
            # Update checkboxes with new range
            self.main_app.update_checkboxes()
            messagebox.showinfo("Success", f"WLS range updated to 0-{max_wls}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid WLS value: {str(e)}")