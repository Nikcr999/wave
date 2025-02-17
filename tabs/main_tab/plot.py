import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox

def setup_plot(self):
    self.fig, self.ax = plt.subplots(figsize=(10, 6))
    self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.content_frame)
    self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    self.fig.canvas.mpl_connect("button_press_event", self.onclick)
    self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)

def configure_plot(self):
    self.ax.set_title("Cell Distribution")
    self.ax.set_xlabel("Voltage (mV)")
    self.ax.set_ylabel("Value")
    self.ax.legend()
    self.ax.grid(True)
    self.ax.set_xlim(-2.4, 0.8)
    self.ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1e'))

def plot_manual(self):
    wls = self.wls_var.get().strip()
    dummy = self.dummy_var.get().strip()
    cdummy = self.cdummy_var.get().strip()
    ssl = self.ssl_var.get().strip()

    if not ssl.isdigit():
        messagebox.showerror("Invalid Input", "SSL must be a number.")
        return

    ssl = int(ssl)
    key = None

    if wls and wls.isdigit():
        key = (int(wls), ssl)
    elif dummy:
        key = (f"DUMMY:{dummy}", ssl)
    elif cdummy:
        key = (f"CDUMMY:{cdummy}", ssl)
    else:
        messagebox.showerror("Invalid Input", "Enter either WLS, DUMMY, or CDUMMY with SSL.")
        return

    try:
        resolution = int(self.resolution_var.get()) / 1000
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    if key in self.data:
        self.ax.clear()
        self.plot_lines.clear()
        self.clear_marks()
        
        for checkbox_var in self.checkboxes.values():
            checkbox_var.set(False)
            
        if key in self.checkboxes:
            self.checkboxes[key].set(True)
        
        y_raw = self.data[key]
        if y_raw:
            x = np.arange(-2.4, -2.4 + len(y_raw) * resolution, resolution)
            
            if isinstance(key[0], int):
                label = f"WLS:{key[0]}, SSL:{key[1]}"
            else:
                label = f"{key[0]}, SSL:{key[1]}"
                
            line, = self.ax.plot(x, y_raw, '-', label=label)
            self.plot_lines[key] = line
            configure_plot(self)
            
        self.canvas_plot.draw()
    else:
        messagebox.showerror("Data Not Found", "No matching data for the given input.")

def plot_selected(self):
    try:
        resolution = int(self.resolution_var.get()) / 1000
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    self.ax.clear()
    self.plot_lines.clear()
    self.clear_marks()
    
    selected_keys = [(key, var.get()) for key, var in self.checkboxes.items()]
    selected_keys = [key for key, checked in selected_keys if checked]
    
    if not selected_keys:
        self.canvas_plot.draw()
        return
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(selected_keys)))
    
    for idx, key in enumerate(selected_keys):
        if key in self.data:
            y_raw = self.data[key]
            if y_raw:
                x = np.arange(-2.4, -2.4 + len(y_raw) * resolution, resolution)
                
                if isinstance(key[0], int):
                    label = f"WLS:{key[0]}, SSL:{key[1]}"
                else:
                    label = f"{key[0]}, SSL:{key[1]}"
                
                line, = self.ax.plot(x, y_raw, '-', label=label, color=colors[idx])
                self.plot_lines[key] = line
    
    configure_plot(self)
    self.canvas_plot.draw()

def clear_plots(self):
    self.ax.clear()
    self.plot_lines.clear()
    self.clear_marks()
    self.canvas_plot.draw()
    for var in self.checkboxes.values():
        var.set(False)