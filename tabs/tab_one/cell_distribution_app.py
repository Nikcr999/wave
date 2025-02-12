import tkinter as tk
from tkinter import ttk
from tabs.tab_one.ui_setup import setup_ui
from tabs.tab_one.sidebar_setup import setup_sidebar
from tabs.tab_one.plot import setup_plot, plot_manual, plot_selected, clear_plots
from tabs.tab_one.read import load_file, parse_file
from tabs.tab_one.mark import onclick, undo_mark, clear_marks
from tabs.tab_one.hover import on_hover, find_nearest
from tabs.tab_two.developer_option import DeveloperOptionTab
from tabs.tab_three.help_tab import HelpTab

class CellDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cell Distribution Analysis")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Main")
        self.tab2 = DeveloperOptionTab(self.notebook, self)
        self.notebook.add(self.tab2, text="Developer Option")
        self.tab3 = HelpTab(self.notebook)
        self.notebook.add(self.tab3, text="Help")
        self.main_container = ttk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        setup_sidebar(self)
        self.content_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.content_frame)
        self.load_file = lambda: load_file(self)
        self.parse_file = lambda: parse_file(self)
        self.plot_manual = lambda: plot_manual(self)
        self.plot_selected = lambda: plot_selected(self)
        self.clear_plots = lambda: clear_plots(self)
        self.onclick = lambda event: onclick(self, event)
        self.undo_mark = lambda: undo_mark(self)
        self.clear_marks = lambda: clear_marks(self)
        self.on_hover = lambda event: on_hover(self, event)
        self.find_nearest = lambda x_click: find_nearest(self, x_click)
        self.plot_lines = {}  
        self.data = {} 
        self.marked_points = []
        setup_ui(self)  
        setup_plot(self)
        self.checkboxes = {}

    def update_checkboxes(self, wls_range):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkboxes.clear()
        for wls in range(wls_range, -1, -1):  
            for ssl in range(8):
                var = tk.BooleanVar()
                self.checkboxes[(wls, ssl)] = var
                ttk.Checkbutton(
                    self.scrollable_frame,
                    text=f"WLS: {wls}, SSL: {ssl}",
                    variable=var,
                    command=self.plot_selected
                ).pack(anchor="w", padx=5, pady=2)
        fixed_combinations = [
            ("DUMMY:1", range(8)), ("DUMMY:2", range(8)), 
            ("CDUMMY:3", range(8)), ("CDUMMY:0", range(7))
        ]
        for dummy, ssl_range in fixed_combinations:
            for ssl in ssl_range:
                var = tk.BooleanVar()
                self.checkboxes[(dummy, ssl)] = var
                ttk.Checkbutton(
                    self.scrollable_frame,
                    text=f"{dummy}, SSL:{ssl}",
                    variable=var,
                    command=self.plot_selected
                ).pack(anchor="w", padx=5, pady=2)
