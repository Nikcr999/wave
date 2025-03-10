"""
Table module for setting up and managing data tables.
Contains functions to create and update tables for data display and analysis.
"""
import tkinter as tk
from tkinter import ttk
import os

import state

def setup_table():
    """
    Set up the data tables in the lower box
    """
    table_container = ttk.Frame(state.lower_box)
    table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create main data table title
    state.table_title_label = ttk.Label(
        table_container, 
        text="Table Title", 
        font=('Helvetica', 12, 'bold')
    )
    state.table_title_label.pack(pady=(0,5))
    
    # Main data table
    table_frame = ttk.Frame(table_container, style='OuterBorder.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=False)
    
    table_frame.columnconfigure(0, weight=1, uniform="column")
    table_frame.columnconfigure(1, weight=1, uniform="column")
    
    header1 = ttk.Label(
        table_frame,
        text="Cell 1,1",
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
    state.analysis_title_label = ttk.Label(
        table_container, 
        text="Pattern Analysis", 
        font=('Helvetica', 12, 'bold')
    )
    state.analysis_title_label.pack(pady=(20,5))
    
    # Create analysis container frame
    state.analysis_container = ttk.Frame(table_container, style='TFrame')
    state.analysis_container.pack(fill=tk.X, expand=False)
    
    # Create initial empty analysis table with header
    state.analysis_frame = ttk.Frame(state.analysis_container, style='OuterBorder.TFrame')
    state.analysis_frame.pack(fill=tk.X, expand=False)
    
    # Initialize with empty message
    empty_label = ttk.Label(
        state.analysis_frame,
        text="No data selected. Select plots to analyze patterns.",
        style='Cell.TLabel',
        anchor='center'
    )
    empty_label.pack(fill=tk.X, expand=True, pady=5)

def update_table_title(title):
    """
    Update the title of the main data table
    
    Args:
        title: New title text
    """
    if state.table_title_label:
        state.table_title_label.config(text=title)

def update_percentage_row(percentage):
    """
    Update the percentage row in the table based on the currently selected item
    
    Args:
        percentage: Percentage value to display, or None if no data selected
    """
    table_container = state.lower_box.winfo_children()[0]
    
    # Find the main table frame
    table_frame = None
    for widget in table_container.winfo_children():
        if isinstance(widget, ttk.Frame) and widget != getattr(state, 'analysis_container', None):
            if widget.winfo_class() == 'TFrame' and not widget.winfo_children():
                continue  # Skip empty frames
            
            # This is the main table frame
            table_frame = widget
            break
    
    if table_frame:
        # Find the percentage row if it exists
        percentage_row = getattr(table_frame, 'percentage_row', None)
        
        if percentage_row:
            # Update the existing percentage row
            if percentage is None:
                percentage_row['text'] = "No data selected. Select plots to analyze patterns."
            else:
                percentage_row['text'] = f"Percentage: {percentage:.2f}%"
        else:
            # Create a new percentage row
            row_count = 0
            for child in table_frame.winfo_children():
                info = child.grid_info()
                if 'row' in info:
                    row_count = max(row_count, int(info['row']))
            
            percentage_row = ttk.Label(
                table_frame,
                text="No data selected. Select plots to analyze patterns." if percentage is None else f"Percentage: {percentage:.2f}%",
                style='Cell.TLabel',
                anchor='center'
            )
            percentage_row.grid(row=row_count+1, column=0, columnspan=2, sticky='ew', ipady=2)
            
            # Store reference to the percentage row
            table_frame.percentage_row = percentage_row

def populate_table_data(headers, data):
    """
    Populate the main data table with headers and data
    
    Args:
        headers: List of header texts
        data: 2D list of data values
    """
    table_container = state.lower_box.winfo_children()[0]
    
    # Find and remove the current table frame (but keep the title and analysis table)
    for widget in table_container.winfo_children():
        if isinstance(widget, ttk.Frame) and widget != getattr(state, 'analysis_container', None):
            if widget.winfo_class() == 'TFrame' and not widget.winfo_children():
                continue  # Skip empty frames
            widget.destroy()
            break
            
    # Create new table frame
    table_frame = ttk.Frame(table_container, style='OuterBorder.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
    
    # Position it after the title but before the analysis table
    children = table_container.winfo_children()
    title_index = children.index(state.table_title_label)
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
    
    # Add the percentage row
    percentage_row = ttk.Label(
        table_frame,
        text="No data selected. Select plots to analyze patterns.",
        style='Cell.TLabel',
        anchor='center'
    )
    percentage_row.grid(row=len(data)+1, column=0, columnspan=num_cols, sticky='ew', ipady=2)
    table_frame.percentage_row = percentage_row

def update_pattern_analysis_table():
    """
    Update the pattern analysis table to show data for the last selected key
    """
    if not state.analysis_frame:
        return
        
    # Remove the old analysis frame
    state.analysis_frame.destroy()
    
    # Create a new frame
    state.analysis_frame = ttk.Frame(state.analysis_container, style='OuterBorder.TFrame')
    state.analysis_frame.pack(fill=tk.X, expand=False)
    
    # Check if we have any pattern data and last selected key
    if not state.pattern_data or not state.last_selected_key:
        # Display empty table with message
        empty_label = ttk.Label(
            state.analysis_frame,
            text="No data selected. Select plots to analyze patterns.",
            style='Cell.TLabel',
            anchor='center'
        )
        empty_label.pack(fill=tk.X, expand=True, pady=5)
        return
    
    # Get only the data for the last selected key
    last_key = state.last_selected_key
    if last_key not in state.pattern_data:
        # No pattern data for the last key
        empty_label = ttk.Label(
            state.analysis_frame,
            text="No low-high-low patterns detected in selected data.",
            style='Cell.TLabel',
            anchor='center'
        )
        empty_label.pack(fill=tk.X, expand=True, pady=5)
        return
    
    data = state.pattern_data[last_key]
    percentages = data.get('percentages', [])
    
    if not percentages:
        # No patterns found
        empty_label = ttk.Label(
            state.analysis_frame,
            text="No low-high-low patterns detected in selected data.",
            style='Cell.TLabel',
            anchor='center'
        )
        empty_label.pack(fill=tk.X, expand=True, pady=5)
        return
    
    # Configure columns - first column for key name, rest for patterns
    max_patterns = len(percentages)
    state.analysis_frame.columnconfigure(0, weight=2, uniform="analysis_col")  # Key column wider
    for i in range(max_patterns):
        state.analysis_frame.columnconfigure(i+1, weight=1, uniform="analysis_col")
    
    # Create headers
    key_header = ttk.Label(
        state.analysis_frame,
        text="Data Key",
        style='AnalysisHeader.TLabel',
        anchor='center'
    )
    key_header.grid(row=0, column=0, sticky='ew', ipady=2)
    
    for i in range(max_patterns):
        pattern_header = ttk.Label(
            state.analysis_frame,
            text=f"Pattern {i+1}",
            style='AnalysisHeader.TLabel',
            anchor='center'
        )
        pattern_header.grid(row=0, column=i+1, sticky='ew', ipady=2)
    
    # Format key for display based on whether it's a composite key
    key_parts = last_key.split('|')
    if len(key_parts) >= 2:
        # It's a composite key with file index and data key
        file_idx = key_parts[0]
        data_key = key_parts[1]
        
        key_type_parts = data_key.split('_')
        if len(key_type_parts) >= 3:
            key_type = key_type_parts[0]
            if key_type == 'w':
                display_key = f"WLS:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
            elif key_type == 'd':
                display_key = f"DUMMY:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
            else:
                display_key = f"CDUMMY:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
        else:
            display_key = data_key
    else:
        # Legacy key format
        key_type_parts = last_key.split('_')
        if len(key_type_parts) >= 3:
            key_type = key_type_parts[0]
            if key_type == 'w':
                display_key = f"WLS:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
            elif key_type == 'd':
                display_key = f"DUMMY:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
            else:
                display_key = f"CDUMMY:{key_type_parts[1]}, SSL:{key_type_parts[2]}"
        else:
            display_key = last_key
        
    # Add key label
    key_label = ttk.Label(
        state.analysis_frame,
        text=display_key,
        style='AnalysisKey.TLabel',
        anchor='center'
    )
    key_label.grid(row=1, column=0, sticky='ew', ipady=2)
    
    # Add pattern percentages for this key
    for i in range(max_patterns):
        if i < len(percentages):
            cell_text = f"{percentages[i]:.2f}%"
        else:
            cell_text = "-"
            
        cell = ttk.Label(
            state.analysis_frame,
            text=cell_text,
            style='Analysis.TLabel',
            anchor='center'
        )
        cell.grid(row=1, column=i+1, sticky='ew', ipady=2)

def clear_pattern_analysis():
    """
    Clear all pattern analysis data and reset the table
    """
    state.pattern_data = {}
    update_pattern_analysis_table()