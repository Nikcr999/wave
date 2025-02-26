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
    
    # Main data table
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
    
    # Analysis table title
    self.analysis_title_label = ttk.Label(
        table_container, 
        text="Pattern Analysis", 
        font=('Helvetica', 12, 'bold')
    )
    self.analysis_title_label.pack(pady=(20,5))
    
    # Create analysis frame
    self.analysis_container = ttk.Frame(table_container, style='TFrame')
    self.analysis_container.pack(fill=tk.X, expand=False)
    
    # Create initial empty table with header
    self.analysis_frame = ttk.Frame(self.analysis_container, style='OuterBorder.TFrame')
    self.analysis_frame.pack(fill=tk.X, expand=False)
    
    # Store pattern data for each key
    self.pattern_data = {}
    
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
                   
    style.configure('Analysis.TLabel',
                   background='#fef3c7',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('AnalysisHeader.TLabel',
                   background='#d97706',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9, 'bold'),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('AnalysisKey.TLabel',
                   background='#155e75',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')

def update_table_title(self, title):
    if hasattr(self, 'table_title_label'):
        self.table_title_label.config(text=title)

def populate_table_data(self, headers, data):
    table_container = self.lower_box.winfo_children()[0]
    
    # Find and remove the current table frame (but keep the title and analysis table)
    for widget in table_container.winfo_children():
        if isinstance(widget, ttk.Frame) and widget != getattr(self, 'analysis_container', None):
            if widget.winfo_class() == 'TFrame' and not widget.winfo_children():
                continue  # Skip empty frames
            widget.destroy()
            break
            
    # Create new table frame
    table_frame = ttk.Frame(table_container, style='OuterBorder.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
    
    # Position it after the title but before the analysis table
    children = table_container.winfo_children()
    title_index = children.index(self.table_title_label)
    table_frame.tkraise()
    
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

def update_pattern_analysis_table(self):
    """
    Update the pattern analysis table based on currently stored pattern data
    """
    if not hasattr(self, 'analysis_frame') or not hasattr(self, 'pattern_data'):
        return
        
    # Remove the old analysis frame
    if hasattr(self, 'analysis_frame'):
        self.analysis_frame.destroy()
    
    # Create a new frame
    self.analysis_frame = ttk.Frame(self.analysis_container, style='OuterBorder.TFrame')
    self.analysis_frame.pack(fill=tk.X, expand=False)
    
    # Check if we have any pattern data
    if not self.pattern_data:
        # Display empty table with message
        empty_label = ttk.Label(
            self.analysis_frame,
            text="No data selected. Select plots to analyze patterns.",
            style='Cell.TLabel',
            anchor='center'
        )
        empty_label.pack(fill=tk.X, expand=True, pady=5)
        return
        
    # Determine the maximum number of patterns across all keys
    max_patterns = 0
    for key, data in self.pattern_data.items():
        percentages = data.get('percentages', [])
        max_patterns = max(max_patterns, len(percentages))
    
    if max_patterns == 0:
        # No patterns found in any data
        empty_label = ttk.Label(
            self.analysis_frame,
            text="No low-high-low patterns detected in selected data.",
            style='Cell.TLabel',
            anchor='center'
        )
        empty_label.pack(fill=tk.X, expand=True, pady=5)
        return
        
    # Configure columns - first column for key name, rest for patterns
    self.analysis_frame.columnconfigure(0, weight=2, uniform="analysis_col")  # Key column wider
    for i in range(max_patterns):
        self.analysis_frame.columnconfigure(i+1, weight=1, uniform="analysis_col")
    
    # Create headers
    key_header = ttk.Label(
        self.analysis_frame,
        text="Data Key",
        style='AnalysisHeader.TLabel',
        anchor='center'
    )
    key_header.grid(row=0, column=0, sticky='ew', ipady=2)
    
    for i in range(max_patterns):
        pattern_header = ttk.Label(
            self.analysis_frame,
            text=f"Pattern {i+1}",
            style='AnalysisHeader.TLabel',
            anchor='center'
        )
        pattern_header.grid(row=0, column=i+1, sticky='ew', ipady=2)
    
    # Add data rows
    row_idx = 1
    for key, data in self.pattern_data.items():
        # Format key for display
        key_parts = key.split('_')
        key_type = key_parts[0]
        if key_type == 'w':
            display_key = f"WLS:{key_parts[1]}, SSL:{key_parts[2]}"
        elif key_type == 'd':
            display_key = f"DUMMY:{key_parts[1]}, SSL:{key_parts[2]}"
        else:
            display_key = f"CDUMMY:{key_parts[1]}, SSL:{key_parts[2]}"
            
        # Add key label
        key_label = ttk.Label(
            self.analysis_frame,
            text=display_key,
            style='AnalysisKey.TLabel',
            anchor='center'
        )
        key_label.grid(row=row_idx, column=0, sticky='ew', ipady=2)
        
        # Add pattern percentages
        percentages = data.get('percentages', [])
        for i in range(max_patterns):
            if i < len(percentages):
                cell_text = f"{percentages[i]:.2f}%"
            else:
                cell_text = "-"
                
            cell = ttk.Label(
                self.analysis_frame,
                text=cell_text,
                style='Analysis.TLabel',
                anchor='center'
            )
            cell.grid(row=row_idx, column=i+1, sticky='ew', ipady=2)
            
        row_idx += 1

def update_pattern_analysis(self, key, patterns_data):
    """
    Update the pattern analysis for a specific key and refresh the table
    
    Args:
        key: The data key
        patterns_data: Dictionary with percentages and patterns
    """
    # Store the pattern data
    if not hasattr(self, 'pattern_data'):
        self.pattern_data = {}
        
    self.pattern_data[key] = patterns_data
    
    # Update the table
    update_pattern_analysis_table(self)
    
def remove_pattern_analysis(self, key):
    """
    Remove pattern analysis for a specific key
    
    Args:
        key: The data key to remove
    """
    if hasattr(self, 'pattern_data') and key in self.pattern_data:
        del self.pattern_data[key]
        update_pattern_analysis_table(self)
        
def clear_pattern_analysis(self):
    """
    Clear all pattern analysis data
    """
    if hasattr(self, 'pattern_data'):
        self.pattern_data = {}
        update_pattern_analysis_table(self)