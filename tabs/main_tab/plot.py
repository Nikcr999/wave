import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
import matplotlib.cm as cm
import os
from tkinter import filedialog

def setup_plot(self):
    self.paned_window = ttk.PanedWindow(self.content_frame, orient=tk.VERTICAL)
    self.paned_window.pack(fill=tk.BOTH, expand=True)
    self.upper_frame = ttk.Frame(self.paned_window)
    self.lower_frame = ttk.Frame(self.paned_window)
    self.paned_window.add(self.upper_frame, weight=2)
    self.paned_window.add(self.lower_frame, weight=8)
    
    self.plot_title = ttk.Label(
        self.upper_frame,
        text="Cell Distribution",
        font=('Helvetica', 12, 'bold')
    )
    self.plot_title.pack(pady=(5,0))
    
    self.fig, self.ax = plt.subplots(figsize=(16, 1.8))
    self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.upper_frame)
    self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    self.fig.canvas.mpl_connect("button_press_event", self.onclick)
    self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
    self.fig.subplots_adjust(left=0.08, right=0.98, bottom=0.4, top=0.85)
    configure_initial_plot(self)
    self.lower_box = ttk.Frame(self.lower_frame, style='Bordered.TFrame')
    self.lower_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Import table setup from table.py
    from tabs.main_tab.table import setup_table
    setup_table(self)

def configure_initial_plot(self):
    self.ax.grid(True, which='major', linestyle='-', alpha=0.8)
    self.ax.grid(True, which='minor', linestyle=':', alpha=0.5)
    self.ax.minorticks_on()
    self.ax.set_xlim(-2.4, 4.6)
    x_ticks_major = np.arange(-2.4, 4.8, 1.0)
    x_ticks_minor = np.arange(-2.4, 4.8, 0.5)
    self.ax.set_xticks(x_ticks_major)
    self.ax.set_xticks(x_ticks_minor, minor=True)
    x_labels = [f'+{x:.2f}' if x > 0 else f'{x:.2f}' for x in x_ticks_major]
    self.ax.set_xticklabels(x_labels, fontsize=8)
    self.ax.set_yscale('log')
    self.ax.set_ylim(1, 1e7)
    y_ticks = [10**i for i in range(8)]
    self.ax.set_yticks(y_ticks)
    self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1E}'))
    self.ax.yaxis.set_minor_formatter(plt.NullFormatter())
    self.ax.set_xlabel('')
    self.ax.set_ylabel('')
    self.ax.tick_params(axis='y', labelsize=6)
    self.ax.grid(True, which='minor', linestyle='-', alpha=0.4)
    self.canvas_plot.draw()

def configure_plot(self):
    configure_initial_plot(self)
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
    
    colors = cm.rainbow(np.linspace(0, 1, len(selected_keys)))
    
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
    configure_initial_plot(self)
    for var in self.checkboxes.values():
        var.set(False)