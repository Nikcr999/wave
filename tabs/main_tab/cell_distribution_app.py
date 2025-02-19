import tkinter as tk
from tkinter import ttk
from tabs.developer_tab.developer_option import DeveloperOptionTab
from tabs.help_tab.help import HelpTab
from tabs.main_tab.ui_setup import setup_ui
from tabs.main_tab.sidebar_setup import setup_sidebar
from tabs.main_tab.plot import (
    setup_plot, plot_data, clear_plots, configure_plot
)
from tabs.main_tab.read import (
    load_file, update_checkboxes, _parse_key, check_key_exists, read_data_for_key
)
from tabs.main_tab.mark import onclick, undo_mark, clear_marks
from tabs.main_tab.hover import on_hover, find_nearest, _clear_hover_elements

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
        
        # Initialize class methods
        self.load_file = lambda: load_file(self)
        self.update_checkboxes = lambda: update_checkboxes(self)
        self._parse_key = lambda line: _parse_key(self, line)
        self.check_key_exists = lambda key: check_key_exists(self, key)
        self.read_data_for_key = lambda key: read_data_for_key(self, key)
        self.plot_data = lambda: plot_data(self)
        self.clear_plots = lambda: clear_plots(self)
        self.onclick = lambda event: onclick(self, event)
        self.undo_mark = lambda: undo_mark(self)
        self.clear_marks = lambda: clear_marks(self)
        self.on_hover = lambda event: on_hover(self, event)
        self.find_nearest = lambda x_click, y_click=None: find_nearest(self, x_click, y_click)
        self._clear_hover_elements = lambda: _clear_hover_elements(self)
        
        # Initialize data structures
        self.plot_lines = {}  
        self.marked_points = []
        self.hover_elements = {'text': None, 'line': None}
        self.checkboxes = {}
        
        # Setup UI components
        setup_ui(self)  
        setup_plot(self)