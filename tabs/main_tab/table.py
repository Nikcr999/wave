import tkinter as tk
from tkinter import ttk
import os

def setup_table(self):
    table_container = ttk.Frame(self.lower_box)
    table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    self.table_title_label = ttk.Label(
        table_container, 
        text="Table Title", 
        font=('Helvetica', 12, 'bold')
    )
    self.table_title_label.pack(pady=(0,5))
    
    if hasattr(self, 'file_path') and self.file_path:
        file_name = os.path.basename(self.file_path)
        title = os.path.splitext(file_name)[0]
        self.table_title_label.config(text=title)
    
    table_frame = ttk.Frame(table_container, style='OuterBorder.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=False)
    
    table_frame.columnconfigure(0, weight=1, uniform="column")
    table_frame.columnconfigure(1, weight=1, uniform="column")
    
    header1 = ttk.Label(
        table_frame,
        text="test test test test test test test test test test",
        style='Header1.TLabel',
        anchor='center'
    )
    header1.grid(row=0, column=0, sticky='ew', ipady=2)
    
    header2 = ttk.Label(
        table_frame,
        text="Cell 1,2",
        style='Header2.TLabel',
        anchor='center'
    )
    header2.grid(row=0, column=1, sticky='ew', ipady=2)
    
    cell21 = ttk.Label(
        table_frame,
        text="Cell 2,1",
        style='Cell.TLabel',
        anchor='center'
    )
    cell21.grid(row=1, column=0, sticky='ew', ipady=2)
    
    cell22 = ttk.Label(
        table_frame,
        text="Cell 2,2",
        style='CellWhite.TLabel',
        anchor='center'
    )
    cell22.grid(row=1, column=1, sticky='ew', ipady=2)
    
    cell31 = ttk.Label(
        table_frame,
        text="Cell 3,1",
        style='Cell.TLabel',
        anchor='center'
    )
    cell31.grid(row=2, column=0, sticky='ew', ipady=2)
    
    cell32 = ttk.Label(
        table_frame,
        text="Cell 3,2",
        style='CellWhite.TLabel',
        anchor='center'
    )
    cell32.grid(row=2, column=1, sticky='ew', ipady=2)
    
    setup_table_styles()

def setup_table_styles():
    style = ttk.Style()
    style.configure('OuterBorder.TFrame', 
                   relief='solid', 
                   borderwidth=2)
    
    style.configure('Header1.TLabel', 
                   background='#1e40af',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('Header2.TLabel',
                   background='white',
                   foreground='red',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('Cell.TLabel',
                   background='#dbeafe',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('CellWhite.TLabel',
                   background='white',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')

def update_table_title(self, title):
    if hasattr(self, 'table_title_label'):
        self.table_title_label.config(text=title)

def populate_table_data(self, headers, data):
    table_container = self.lower_box.winfo_children()[0]
    
    for widget in table_container.winfo_children():
        if isinstance(widget, ttk.Frame) and not isinstance(widget, ttk.Label):
            widget.destroy()
    table_frame = ttk.Frame(table_container, style='OuterBorder.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
    
    num_cols = len(headers)
    for i in range(num_cols):
        table_frame.columnconfigure(i, weight=1, uniform="column")
    
    for col, header_text in enumerate(headers):
        header = ttk.Label(
            table_frame,
            text=header_text,
            style='Header1.TLabel',
            anchor='center'
        )
        header.grid(row=0, column=col, sticky='ew', ipady=2)
    
    for row_idx, row_data in enumerate(data):
        for col_idx, cell_value in enumerate(row_data):
            style = 'Cell.TLabel' if row_idx % 2 == 0 else 'CellWhite.TLabel'
            
            cell = ttk.Label(
                table_frame,
                text=str(cell_value),
                style=style,
                anchor='center'
            )
            cell.grid(row=row_idx+1, column=col_idx, sticky='ew', ipady=2)