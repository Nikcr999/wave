import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox

# def setup_plot(self):
#     self.paned_window = ttk.PanedWindow(self.content_frame, orient=tk.VERTICAL)
#     self.paned_window.pack(fill=tk.BOTH, expand=True)
    
#     self.upper_frame = ttk.Frame(self.paned_window)
#     self.lower_frame = ttk.Frame(self.paned_window)
    
#     self.paned_window.add(self.upper_frame, weight=2)
#     self.paned_window.add(self.lower_frame, weight=8)
    
#     self.fig, self.ax = plt.subplots(figsize=(15, 1.8))
#     self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.upper_frame)
#     self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
#     self.fig.canvas.mpl_connect("button_press_event", self.onclick)
#     self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
#     self.fig.subplots_adjust(left=0.08, right=0.95, bottom=0.25, top=0.9)
    
#     self.lower_box = ttk.Frame(self.lower_frame, style='Bordered.TFrame')
#     self.lower_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
#     style = ttk.Style()
#     style.configure('Bordered.TFrame', borderwidth=2, relief='solid')

# def configure_plot(self):
#     self.ax.set_title("Cell Distribution")
#     self.ax.set_xlabel("Voltage (mV)")
#     self.ax.set_ylabel("Value")
#     self.ax.grid(True)
#     self.ax.set_xlim(-2.4, 0.8)
#     self.ax.set_xticks(np.arange(-2.4, 0.9, 0.4))
#     self.ax.set_yscale('log')
#     self.ax.set_ylim(1, 10000)
#     self.ax.legend(bbox_to_anchor=(0.5, -0.35), loc='center', ncol=len(self.plot_lines), 
#                   borderaxespad=0.)

def setup_plot(self):
    self.paned_window = ttk.PanedWindow(self.content_frame, orient=tk.VERTICAL)
    self.paned_window.pack(fill=tk.BOTH, expand=True)
    self.upper_frame = ttk.Frame(self.paned_window)
    self.lower_frame = ttk.Frame(self.paned_window)
    self.paned_window.add(self.upper_frame, weight=2)
    self.paned_window.add(self.lower_frame, weight=8)
    self.fig, self.ax = plt.subplots(figsize=(12, 1.8))
    self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.upper_frame)
    self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    self.fig.canvas.mpl_connect("button_press_event", self.onclick)
    self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
    self.fig.subplots_adjust(left=0.12, right=0.98, bottom=0.4, top=0.85)
    
    self.lower_box = ttk.Frame(self.lower_frame, style='Bordered.TFrame')
    self.lower_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    style = ttk.Style()
    style.configure('Bordered.TFrame', borderwidth=2, relief='solid')

def configure_plot(self):
    self.ax.set_title("Cell Distribution")
    self.ax.set_xlabel("Voltage (mV)")
    self.ax.set_ylabel("Value")
    self.ax.grid(True)
    self.ax.set_xlim(-2.4, 0.8)
    self.ax.set_xticks(np.arange(-2.4, 0.9, 0.4))
    self.ax.set_yscale('log')
    self.ax.set_ylim(1, 10000)
    self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1E}'))
    
    self.ax.legend(bbox_to_anchor=(0.5, -0.5), 
                  loc='center', 
                  ncol=len(self.plot_lines),
                  borderaxespad=0,
                  frameon=False)
    
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
            manual_key = f"w_{wls}_{ssl}"
        elif dummy:
            manual_key = f"d_{dummy}_{ssl}"
        elif cdummy:
            manual_key = f"c_{cdummy}_{ssl}"

    if manual_key and manual_key in self.checkboxes:
        self.checkboxes[manual_key].set(True)

    selected_keys = [(key, var.get()) for key, var in self.checkboxes.items()]
    selected_keys = [key for key, checked in selected_keys if checked]
    
    if not selected_keys:
        if manual_key:
            messagebox.showerror("Invalid Input", "The specified combination is not in the available list.")
        self.clear_plots()
        return
    
    current_marks = self.marked_points.copy()
    
    self.ax.clear()
    self.plot_lines.clear()
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(selected_keys)))
    
    for idx, key in enumerate(selected_keys):
        data = self.read_data_for_key(key)
        if data:
            x = np.arange(-2.4, -2.4 + len(data) * resolution, resolution)
            
            key_parts = key.split('_')
            key_type = key_parts[0]
            if key_type == 'w':
                label = f"WLS:{key_parts[1]}, SSL:{key_parts[2]}"
            elif key_type == 'd':
                label = f"DUMMY:{key_parts[1]}, SSL:{key_parts[2]}"
            else:
                label = f"CDUMMY:{key_parts[1]}, SSL:{key_parts[2]}"
            
            line, = self.ax.plot(x, data, '-', label=label, color=colors[idx])
            self.plot_lines[key] = line
    
    configure_plot(self)
    
    self.marked_points = []
    for mark in current_marks:
        marker_data = mark[0].get_data()
        x_val = marker_data[0][0]
        y_val = marker_data[1][0]
        
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