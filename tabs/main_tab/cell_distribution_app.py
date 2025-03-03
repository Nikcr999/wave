import tkinter as tk
from tkinter import ttk
from tabs.developer_tab.developer_option import DeveloperOptionTab
from tabs.help_tab.help import HelpTab
from tabs.main_tab.sidebar_setup import setup_sidebar
from tabs.main_tab.plot import (
    setup_plot, plot_data, clear_plots, configure_plot, analyze_all_selected
)
from tabs.main_tab.table import (
    update_table_title, populate_table_data, update_pattern_analysis, 
    remove_pattern_analysis, clear_pattern_analysis, update_pattern_analysis_table,
    update_percentage_row, update_analyze_button
)
from tabs.main_tab.read import (
    load_file, update_checkboxes, _parse_key, check_key_exists, read_data_for_key
)
from tabs.main_tab.mark import onclick, undo_mark, clear_marks
from tabs.main_tab.hover import on_hover, find_nearest, _clear_hover_elements
from tabs.main_tab.excel import setup_excel_handler

class CellDistributionApp:
    VERSION = "1.0.0"
    DEVELOPER = "Nikhil"

    def __init__(self, root):
        self.root = root
        self.root.title("Cell Distribution Analysis")
        self.root.configure(bg='white')
        
        self.plot_lines = {}  
        self.marked_points = []
        self.hover_elements = {'text': None, 'line': None}
        self.checkboxes = {}
        self.input_dialog = None
        self.file_paths = []  # Initialize as empty list to store multiple file paths
        self.data_point_length = None  # Will store the length of data points for optimization
        
        self.resolution_var = tk.StringVar(value="40")
        self.wls_var = tk.StringVar()
        self.dummy_var = tk.StringVar()
        self.cdummy_var = tk.StringVar()
        self.ssl_var = tk.StringVar()
        
        # Bind methods
        self.load_file = lambda: load_file(self)
        self.update_checkboxes = lambda: update_checkboxes(self)
        self._parse_key = lambda line: _parse_key(self, line)
        self.check_key_exists = lambda key: check_key_exists(self, key)
        self.read_data_for_key = lambda key: read_data_for_key(self, key)
        self.plot_data = lambda: self._plot_data()
        self.clear_plots = lambda: self._clear_plots()
        self.onclick = lambda event: onclick(self, event)
        self.undo_mark = lambda: undo_mark(self)
        self.clear_marks = lambda: clear_marks(self)
        self.on_hover = lambda event: on_hover(self, event)
        self.find_nearest = lambda x_click, y_click=None: find_nearest(self, x_click, y_click)
        self._clear_hover_elements = lambda: _clear_hover_elements(self)
        
        # Table pattern analysis methods
        self.update_pattern_analysis = lambda key, patterns_data: update_pattern_analysis(self, key, patterns_data)
        self.remove_pattern_analysis = lambda key: remove_pattern_analysis(self, key)
        self.clear_pattern_analysis = lambda: clear_pattern_analysis(self)
        self.update_pattern_analysis_table = lambda: update_pattern_analysis_table(self)
        self.update_percentage_row = lambda percentage: update_percentage_row(self, percentage)
        
        self._setup_styles()
        self._setup_notebook()
        self._setup_buttons()
        self._setup_containers()
        self._initialize_data()
        self._setup_ui_internally()  # Changed to internal method instead of importing
        
        # Setup Excel handler
        setup_excel_handler(self)
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _plot_data(self):
        """Wrapper for the original plot_data function with Excel button update"""
        # Call the original plot_data function
        plot_data(self)
        
        # Update the analyze button
        update_analyze_button(self)
        
    def _clear_plots(self):
        """Wrapper for the original clear_plots function with Excel button update"""
        # Call the original clear_plots function
        clear_plots(self)
        
        # Update the analyze button
        update_analyze_button(self)
        
    def on_close(self):
        """Clean up resources when the application is closed"""
        # Close Excel if it's open
        if hasattr(self, 'excel_handler'):
            self.excel_handler.close()
        self.root.destroy()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.main_container.forget(self.sidebar)
            self.main_container.add(self.sidebar, width=30)
            self.toggle_btn.configure(text="►")
            self.canvas.pack_forget()
            self.sidebar_expanded = False
        else:
            self.main_container.forget(self.sidebar)
            self.main_container.add(self.sidebar, width=200)  # Increased from 150 to 200
            self.toggle_btn.configure(text="◄")
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.sidebar_expanded = True
    
    def _setup_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('TNotebook', background='white')
        style.configure('TNotebook.Tab', background='white', padding=(10, 5), font=('', 10))
        style.configure('Treeview', background='white', fieldbackground='white')
        style.configure('TCanvas', background='white')
        style.configure('Footer.TLabel', background='white', font=('Helvetica', 8))
    
    def _setup_notebook(self):
        style = ttk.Style()
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", padding=[10, 2], font=('Helvetica', 9), borderwidth=0)
        style.map("TNotebook.Tab",
                 background=[("selected", "white"), ("!selected", "white")],
                 foreground=[("selected", "#000000"), ("!selected", "#000000")])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.tab1 = ttk.Frame(self.notebook, style='TFrame')
        self.tab2 = DeveloperOptionTab(self.notebook, self)
        self.tab3 = HelpTab(self.notebook)
        
        self.notebook.add(self.tab1, text="Load")
        self.notebook.add(self.tab2, text="Developer Option")
        self.notebook.add(self.tab3, text="Help")
        
        self.indicator_frame = tk.Frame(self.root, height=3, bg="white")
        self.indicator_frame.pack(fill=tk.X, padx=0, pady=0)
        self.indicator = tk.Frame(self.indicator_frame, height=3, width=50, bg="#ff9900")
        self.indicator.place(x=25, y=0)
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def on_tab_changed(self, event):
        tab_id = self.notebook.select()
        tab_index = self.notebook.index(tab_id)
        tab_width = 50 if tab_index == 0 else 120 if tab_index == 1 else 45
        x_pos = 25 if tab_index == 0 else 85 if tab_index == 1 else 215
        
        self.indicator.place_forget()
        self.indicator = tk.Frame(self.indicator_frame, height=3, width=tab_width, bg="#ff9900")
        self.indicator.place(x=x_pos, y=0)
    
    def _setup_buttons(self):
        button_frame = ttk.Frame(self.tab1, style='TFrame')
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        buttons = [
            ("Load", self.load_file),
            ("Manual\nInput", self.show_manual_input),
            ("Undo\nMark", self.undo_mark),
            ("Clear\nMarks", self.clear_marks),
            ("Clear\nPlots", self.clear_plots)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg='#ff9900',
                fg='black',
                font=('Helvetica', 9),
                height=2,
                width=8,
                relief='raised',
                borderwidth=1
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _setup_containers(self):
        self.main_container = ttk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        setup_sidebar(self)
        self.content_frame = ttk.Frame(self.main_container, style='TFrame')
        self.main_container.add(self.content_frame)
    
    def _initialize_data(self):
        self.sidebar_expanded = True
    
    def _setup_ui_internally(self):
        # This replaces the imported setup_ui function
        self.resolution_var = tk.StringVar(value="40")
        self.wls_var = tk.StringVar()
        self.dummy_var = tk.StringVar()
        self.cdummy_var = tk.StringVar()
        self.ssl_var = tk.StringVar()
        
        # Now call setup_plot after setting up variables
        setup_plot(self)

    def show_manual_input(self):
        if self.input_dialog is None or not tk.Toplevel.winfo_exists(self.input_dialog):
            self.input_dialog = tk.Toplevel(self.root)
            self.input_dialog.title("Manual Input")
            self.input_dialog.geometry("400x200")
            self.input_dialog.configure(bg='white')
            
            input_frame = ttk.Frame(self.input_dialog, padding="20", style='TFrame')
            input_frame.pack(fill=tk.BOTH, expand=True)
            
            row1_frame = ttk.Frame(input_frame, style='TFrame')
            row1_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row1_frame, text="Resolution (mV):", width=12).pack(side=tk.LEFT)
            ttk.Entry(row1_frame, textvariable=self.resolution_var, width=10).pack(side=tk.LEFT, padx=(0,10))
            ttk.Label(row1_frame, text="WLS:", width=6).pack(side=tk.LEFT)
            ttk.Entry(row1_frame, textvariable=self.wls_var, width=10).pack(side=tk.LEFT, padx=(0,10))
            ttk.Label(row1_frame, text="DUMMY:", width=8).pack(side=tk.LEFT)
            ttk.Entry(row1_frame, textvariable=self.dummy_var, width=10).pack(side=tk.LEFT)
            
            row2_frame = ttk.Frame(input_frame, style='TFrame')
            row2_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row2_frame, text="CDUMMY:", width=12).pack(side=tk.LEFT)
            ttk.Entry(row2_frame, textvariable=self.cdummy_var, width=10).pack(side=tk.LEFT, padx=(0,10))
            ttk.Label(row2_frame, text="SSL:", width=6).pack(side=tk.LEFT)
            ttk.Entry(row2_frame, textvariable=self.ssl_var, width=10).pack(side=tk.LEFT)
            
            plot_btn = tk.Button(
                input_frame, 
                text="Plot",
                command=lambda: [self.plot_data(), self.input_dialog.destroy()],
                bg='#ff9900',
                fg='white',
                font=('Helvetica', 9),
                height=2,
                width=8,
                relief='raised',
                borderwidth=2
            )
            plot_btn.pack(pady=20)