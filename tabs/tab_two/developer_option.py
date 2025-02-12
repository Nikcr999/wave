import tkinter as tk
from tkinter import ttk, messagebox

class DeveloperOptionTab(ttk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.max_wls_var = tk.StringVar(value="175")

        ttk.Label(self, text="Set Maximum WLS Value:").pack(pady=5)
        self.entry = ttk.Entry(self, textvariable=self.max_wls_var, width=10)
        self.entry.pack(pady=5)

        ttk.Button(self, text="Submit", command=self.confirm_wls_update).pack(pady=10)

    def confirm_wls_update(self):
        try:
            new_wls = int(self.max_wls_var.get())
            if new_wls < 0:
                raise ValueError

            confirm = messagebox.askyesno("Confirm Update", f"Set WLS max to {new_wls}?")
            if confirm:
                self.main_app.update_checkboxes(new_wls)
                self.main_app.notebook.select(self.main_app.tab1)

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid positive integer for WLS.")