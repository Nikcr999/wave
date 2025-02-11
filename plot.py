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
    wls = self.wls_var.get().strip()
    ssl = self.ssl_var.get().strip()

    try:
        resolution = int(self.resolution_var.get())
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    if (wls, ssl) in self.data:
        y_raw = self.data[(wls, ssl)]
        y = [np.log10(y_val) if y_val > 0 else 0 for y_val in y_raw]
        start_voltage = -2400
        x = np.arange(start_voltage, start_voltage + len(y) * resolution, resolution)
        self.x_data = x
        self.y_data = y

        line, = self.ax.plot(x, y, '-', label=f"WLS:{wls}, SSL:{ssl}")
        self.plot_lines[(wls, ssl)] = line

        self.ax.set_title("Cell Distribution")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Log10(Value)")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas_plot.draw()
    else:
        messagebox.showerror("Data Not Found", "No matching data for the given WLS and SSL.")

def plot_selected(self):
    try:
        resolution = int(self.resolution_var.get())
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    self.ax.clear()
    self.plot_lines.clear()

    for (wls, ssl), var in self.checkboxes.items():
        if var.get():  
            y_raw = self.data[(wls, ssl)]
            y = [np.log10(y_val) if y_val > 0 else 0 for y_val in y_raw]
            start_voltage = -2400
            x = np.arange(start_voltage, start_voltage + len(y) * resolution, resolution)
            
            line, = self.ax.plot(x, y, '-', label=f"WLS:{wls}, SSL:{ssl}")
            self.plot_lines[(wls, ssl)] = line
            self.x_data = x
            self.y_data = y

    if self.plot_lines:
        self.ax.set_title("Cell Distribution")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Log10(Value)")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas_plot.draw()

def clear_plots(self):
    self.ax.clear()
    self.plot_lines.clear()
    self.canvas_plot.draw()
    for var in self.checkboxes.values():
        var.set(False)
