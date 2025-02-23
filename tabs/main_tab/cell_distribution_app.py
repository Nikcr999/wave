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
        
        self.resolution_var = tk.StringVar(value="40")
        self.wls_var = tk.StringVar()
        self.dummy_var = tk.StringVar()
        self.cdummy_var = tk.StringVar()
        self.ssl_var = tk.StringVar()
        
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
        
        self._setup_styles()
        self._setup_notebook()
        self._setup_buttons()
        self._setup_containers()
        self._initialize_data()
        self._setup_ui()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.main_container.forget(self.sidebar)
            self.main_container.add(self.sidebar, width=30)
            self.toggle_btn.configure(text="►")
            self.canvas.pack_forget()
            self.sidebar_expanded = False
        else:
            self.main_container.forget(self.sidebar)
            self.main_container.add(self.sidebar, width=150)
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
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        self.tab1 = ttk.Frame(self.notebook, style='TFrame')
        self.tab2 = DeveloperOptionTab(self.notebook, self)
        self.tab3 = HelpTab(self.notebook)
        self.notebook.add(self.tab1, text="Main")
        self.notebook.add(self.tab2, text="Developer Option")
        self.notebook.add(self.tab3, text="Help")
    
    def _setup_buttons(self):
        button_frame = ttk.Frame(self.tab1, style='TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
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
                bg='orange',
                fg='black',
                font=('Helvetica', 10, 'bold'),
                height=2,
                width=8,
                wraplength=80,
                relief='solid',
                bd=1
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
    
    def _setup_ui(self):
        setup_ui(self)  
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
                bg='orange',
                fg='black',
                font=('Helvetica', 10, 'bold'),
                height=2,
                width=8,
                relief='solid',
                bd=1
            )
            plot_btn.pack(pady=20)