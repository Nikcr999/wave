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

def plot_manual(self):
    key = None  

    wls = self.wls_var.get().strip()
    dummy = self.dummy_var.get().strip()
    cdummy = self.cdummy_var.get().strip()
    ssl = self.ssl_var.get().strip()

    if not ssl.isdigit():
        messagebox.showerror("Invalid Input", "SSL must be a number.")
        return
    ssl = int(ssl)
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
        y_raw = self.data[key]
        y = [np.log10(y_val) if y_val > 0 else 0 for y_val in y_raw]
        start_voltage = -2.4
        x = np.arange(start_voltage, start_voltage + len(y) * resolution, resolution)

        line, = self.ax.plot(x, y, '-', label=f"{key[0]}, SSL:{key[1]}")
        self.plot_lines[key] = line

        self.ax.set_title("Cell Distribution")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Log10(Value)")
        self.ax.legend()
        self.ax.grid(True)
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
    plotted_any = False  

    for (key, var) in self.checkboxes.items():
        if var.get():  
            if key in self.data:
                y_raw = self.data[key]
                y = [np.log10(y_val) if y_val > 0 else 0 for y_val in y_raw]
                start_voltage = -2.4
                x = np.arange(start_voltage, start_voltage + len(y) * resolution, resolution)

                line, = self.ax.plot(x, y, '-', label=f"{key[0]}, SSL:{key[1]}")
                self.plot_lines[key] = line 
                plotted_any = True

    if plotted_any:
        self.ax.set_title("Cell Distribution")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Log10(Value)")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas_plot.draw()
    else:
        messagebox.showwarning("No Selection", "Please select at least one checkbox to plot.")

def clear_plots(self):
    self.ax.clear()  
    self.plot_lines.clear()
    self.canvas_plot.draw()
    for var in self.checkboxes.values():
        var.set(False)
