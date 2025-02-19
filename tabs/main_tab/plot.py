import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox

def setup_plot(self):
    self.fig, self.ax = plt.subplots(figsize=(15, 6))
    self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.content_frame)
    self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    self.fig.canvas.mpl_connect("button_press_event", self.onclick)
    self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
    self.fig.subplots_adjust(left=0.05, right=0.95)

def configure_plot(self):
    self.ax.set_title("Cell Distribution")
    self.ax.set_xlabel("Voltage (mV)")
    self.ax.set_ylabel("Value")
    self.ax.legend()
    self.ax.grid(True)
    self.ax.set_xlim(-2.4, 0.8)
    self.ax.set_xticks(np.arange(-2.4, 0.9, 0.4))
    self.ax.set_yscale('log')
    self.ax.set_ylim(1, 10000)

def plot_data(self):
    try:
        resolution = int(self.resolution_var.get()) / 1000
        if resolution <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Resolution", "Please enter a valid positive integer for resolution.")
        return

    wls = self.wls_var.get().strip()
    dummy = self.dummy_var.get().strip()
    cdummy = self.cdummy_var.get().strip()
    ssl = self.ssl_var.get().strip()

    manual_key = None
    if ssl.isdigit():
        ssl = int(ssl)
        if wls and wls.isdigit():
            manual_key = (int(wls), ssl)
        elif dummy:
            manual_key = (f"DUMMY:{dummy}", ssl)
        elif cdummy:
            manual_key = (f"CDUMMY:{cdummy}", ssl)

    if manual_key and manual_key in self.checkboxes:
        self.checkboxes[manual_key].set(True)

    selected_keys = [(key, var.get()) for key, var in self.checkboxes.items()]
    selected_keys = [key for key, checked in selected_keys if checked]
    
    if not selected_keys:
        self.ax.clear()
        self.plot_lines.clear()
        self.marked_points.clear()
        configure_plot(self)
        self.canvas_plot.draw()
        return
    
    # Store current marks and their x-coordinates with associated lines
    current_marks = []
    for mark in self.marked_points:
        x, y = mark[0].get_data()
        x_val = x[0]
        # Find which line this mark belongs to
        for key, line in self.plot_lines.items():
            if x_val in line.get_xdata():
                current_marks.append((x_val, y[0], key))
                break
    
    self.ax.clear()
    self.plot_lines.clear()
    self.marked_points.clear()
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(selected_keys)))
    
    for idx, key in enumerate(selected_keys):
        data = self.read_data_for_key(key)
        if data:
            x = np.arange(-2.4, -2.4 + len(data) * resolution, resolution)
            
            if isinstance(key[0], int):
                label = f"WLS:{key[0]}, SSL:{key[1]}"
            else:
                label = f"{key[0]}, SSL:{key[1]}"
            
            line, = self.ax.plot(x, data, '-', label=label, color=colors[idx])
            self.plot_lines[key] = line
    
    configure_plot(self)
    
    # Restore only marks for currently plotted lines
    for x_val, y_val, orig_key in current_marks:
        if orig_key in self.plot_lines:  # Only restore if the line is still plotted
            marker = self.ax.plot(x_val, y_val, 'ro', markersize=8, alpha=0.8)[0]
            vline = self.ax.axvline(x=x_val, color='black', linestyle=':', alpha=0.5)
            text = self.ax.text(
                x_val, self.ax.get_ylim()[0],
                f'V: {x_val:.3f}',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7, ec='gray'),
                ha='center', va='bottom'
            )
            self.marked_points.append((marker, vline, text))
    
    self.canvas_plot.draw()

def clear_plots(self):
    self.ax.clear()
    self.plot_lines.clear()
    self.marked_points.clear()
    self.canvas_plot.draw()
    for var in self.checkboxes.values():
        var.set(False)