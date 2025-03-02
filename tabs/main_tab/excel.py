import tkinter as tk
from tkinter import messagebox
import xlwings as xw
import re
import os

class ExcelProcessor:
    def __init__(self, main_app):
        self.main_app = main_app
        # Hardcoded file path - replace with your actual path
        self.excel_file_path = "path/to/your/excel_file.xlsx"
        self.app = None
        self.wb = None
        self.sheet = None
        self.data_dict = {}  # Store data in the format d['WLS:10']['MAT1'] = [1.57v, ..., 1.6v]
        # Hardcoded sheet name - replace with your actual sheet name
        self.sheet_name = "Sheet1"
        
    def load_excel_file(self):
        """Load the hardcoded Excel file and sheet using xlwings"""
        try:
            # Check if file exists
            if not os.path.exists(self.excel_file_path):
                messagebox.showerror("Error", f"Excel file not found at: {self.excel_file_path}")
                return False
            
            # Open Excel application and workbook
            self.app = xw.App(visible=False)  # Set visible=True for debugging
            self.wb = self.app.books.open(self.excel_file_path)
            
            # Verify that the specified sheet exists
            try:
                self.sheet = self.wb.sheets[self.sheet_name]
            except:
                messagebox.showerror("Error", f"Sheet '{self.sheet_name}' not found in workbook")
                self.wb.close()
                self.app.quit()
                return False
                
            # Process the data
            self.find_and_process_data()
            
            # Update the UI with loaded data
            self.update_ui_with_excel_data()
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file: {str(e)}")
            if self.wb:
                try:
                    self.wb.close()
                except:
                    pass
            if self.app:
                try:
                    self.app.quit()
                except:
                    pass
            return False
    
    def __del__(self):
        """Clean up Excel application resources when done"""
        self.close_excel()
    
    def close_excel(self):
        """Close Excel workbook and application"""
        try:
            if self.wb:
                self.wb.close()
            if self.app:
                self.app.quit()
        except:
            pass
            
    def find_and_process_data(self):
        """Find the 'z' text and process the table data"""
        # Clear previous data
        self.data_dict = {}
        
        # Find the 'z' text in the sheet
        z_cell = self.find_cell_with_text('z')
        if not z_cell:
            messagebox.showinfo("Information", "Could not find starting point 'z' in the sheet.")
            return False
            
        z_row = z_cell.row
        
        # Process from z_row to the end of the sheet
        self.process_table_data(z_row)
        return True
        
    def find_cell_with_text(self, search_text):
        """Find a cell containing the specified text"""
        # Get used range to avoid scanning the entire sheet
        used_range = self.sheet.used_range
        
        # Convert to numpy array for faster searching
        data = used_range.value
        
        # Search for the text
        for i in range(len(data)):
            for j in range(len(data[i]) if isinstance(data[i], list) else 1):
                cell_value = data[i][j] if isinstance(data[i], list) else data[i]
                if cell_value and str(cell_value).lower() == search_text.lower():
                    # Return the cell object
                    return self.sheet.cells(i + used_range.row, j + used_range.column)
        
        return None
        
    def process_table_data(self, start_row):
        """Process the table data starting from the given row"""
        # First, identify all the column headers (WL1~WL11(r9), etc.)
        column_ranges = self.identify_column_ranges(start_row)
        
        # If no column ranges were found, exit
        if not column_ranges:
            messagebox.showinfo("Information", "Could not identify column ranges.")
            return
            
        # Now process the data for each plane (MAT1, MAT2, etc.)
        self.process_plane_data(start_row + 1, column_ranges)
        
    def identify_column_ranges(self, header_row):
        """Identify the column ranges like WL1~WL11(r9)"""
        column_ranges = []
        
        # Get the row data
        row_data = self.sheet.range(f"{header_row}:{header_row}").value
        
        # If row_data is not a list, convert it to one
        if not isinstance(row_data, list):
            row_data = [row_data]
            
        # Process each cell to find WL ranges
        for col_idx, cell_value in enumerate(row_data):
            if cell_value and 'WL' in str(cell_value):
                # Extract the range using regex
                # Matches patterns like WL1~WL11(r9)
                match = re.search(r'WL(\d+)~WL(\d+)', str(cell_value))
                if match:
                    start_wl = int(match.group(1))
                    end_wl = int(match.group(2))
                    column_ranges.append({
                        'start_wl': start_wl,
                        'end_wl': end_wl,
                        'column': col_idx + 1,  # +1 because xlwings uses 1-based indexing
                        'header_text': cell_value
                    })
        
        return column_ranges
        
    def process_plane_data(self, start_row, column_ranges):
        """Process data for each plane (MAT1, MAT2, etc.)"""
        # Get the data range to process
        max_row = self.sheet.used_range.last_cell.row
        data_range = self.sheet.range(f"{start_row}:{max_row}").value
        
        current_plane = None
        plane_row_start = None
        
        # If data_range is not a list of lists, handle accordingly
        if not isinstance(data_range, list):
            data_range = [data_range]
        
        for row_idx, row_data in enumerate(data_range):
            # Convert to list if it's a single value
            if not isinstance(row_data, list):
                row_data = [row_data]
                
            # Check if this is a plane header (MAT1, MAT2, etc.)
            plane_header = None
            for col_idx in range(min(5, len(row_data))):  # Check first 5 columns
                cell_value = row_data[col_idx] if col_idx < len(row_data) else None
                if cell_value and isinstance(cell_value, str) and re.match(r'MAT\d+', cell_value):
                    plane_header = cell_value
                    current_plane = plane_header
                    plane_row_start = row_idx + 1  # Data starts in the next row
                    break
            
            # If we found a new plane, skip to next row
            if plane_header:
                continue
                
            # If we don't have a current plane, skip
            if not current_plane or not plane_row_start:
                continue
                
            # Process data for this row in each column range
            for col_range in column_ranges:
                col_idx = col_range['column'] - 1  # Convert to 0-based for list indexing
                read_col_idx = col_idx + 1  # +1 column for 'read' values
                
                # Check if read_col_idx is within row_data
                if read_col_idx < len(row_data):
                    read_value = row_data[read_col_idx]
                    
                    if read_value is not None:
                        # Extract voltage value (should be in format like 1.57v)
                        voltage_text = str(read_value)
                        
                        # Store data by WLS range and plane
                        range_key = f"WL{col_range['start_wl']}~WL{col_range['end_wl']}"
                        
                        # Create nested dictionaries if they don't exist
                        if range_key not in self.data_dict:
                            self.data_dict[range_key] = {}
                        if current_plane not in self.data_dict[range_key]:
                            self.data_dict[range_key][current_plane] = []
                            
                        # Add the voltage value to the list
                        self.data_dict[range_key][current_plane].append(voltage_text)
        
    def update_ui_with_excel_data(self):
        """Update the UI with the loaded Excel data"""
        # Initialize the checkboxes
        self.setup_excel_checkboxes()
        
        # Show a message about the loaded data
        num_ranges = len(self.data_dict)
        
        if num_ranges > 0:
            planes = set()
            total_values = 0
            
            for range_key, planes_dict in self.data_dict.items():
                for plane, values in planes_dict.items():
                    planes.add(plane)
                    total_values += len(values)
                    
            messagebox.showinfo(
                "Excel Data Loaded", 
                f"Successfully loaded {num_ranges} WL ranges across {len(planes)} planes with {total_values} total values."
            )
        else:
            messagebox.showinfo("Information", "No usable data found in the selected Excel sheet.")
            
    def setup_excel_checkboxes(self):
        """Setup checkboxes for Excel data selection"""
        from tkinter import ttk
        
        # Clear existing checkboxes if needed
        if hasattr(self.main_app, 'checkboxes'):
            self.main_app.checkboxes.clear()
            
            for widget in self.main_app.scrollable_frame.winfo_children():
                widget.destroy()
        
        # Create a container frame
        container_frame = ttk.Frame(self.main_app.scrollable_frame, style='TFrame')
        container_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create blocks for each WL range
        block_index = 0
        for range_key, planes_dict in self.data_dict.items():
            block_frame = ttk.Frame(container_frame, style='TFrame')
            block_frame.pack(fill=tk.X, anchor=tk.W, pady=2)
            
            header_frame = ttk.Frame(block_frame, style='TFrame')
            header_frame.pack(fill=tk.X)
            
            items_frame = ttk.Frame(block_frame, style='TFrame')
            
            toggle_btn = tk.Button(
                header_frame,
                text="+",
                width=2,
                font=('Arial', 8, 'bold'),
                bg='white',
                relief='flat',
                command=lambda f=items_frame, b=toggle_btn: self.toggle_excel_block(b, f)
            )
            toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            select_all_var = tk.BooleanVar()
            select_all_cb = ttk.Checkbutton(
                header_frame,
                text=range_key,
                variable=select_all_var,
                style='Checkbox.TCheckbutton',
                command=lambda v=select_all_var, items=[]: self.toggle_all_excel_items(v, items)
            )
            select_all_cb.pack(side=tk.LEFT, padx=5)
            
            item_vars = []
            
            # Add checkboxes for each plane in this range
            for plane, values in planes_dict.items():
                var = tk.BooleanVar()
                # Create a key that stores the excel data info
                excel_key = f"excel|{range_key}|{plane}"
                self.main_app.checkboxes[excel_key] = var
                item_vars.append(var)
                
                checkbox = ttk.Checkbutton(
                    items_frame,
                    text=f"{plane} ({len(values)} values)",
                    variable=var,
                    command=lambda v=var, items=item_vars, all_var=select_all_var, 
                           k=excel_key: self.excel_item_toggled(v, items, all_var, k),
                    style='Checkbox.TCheckbutton'
                )
                checkbox.pack(anchor=tk.W, padx=(20, 0))
            
            # Update the items list for the select all checkbox
            select_all_cb.config(
                command=lambda v=select_all_var, items=item_vars: self.toggle_all_excel_items(v, items)
            )
            
            block_index += 1
            
    def toggle_excel_block(self, btn, frame):
        """Toggle visibility of an Excel data block"""
        if frame.winfo_manager():
            btn.config(text="+")
            frame.pack_forget()
        else:
            btn.config(text="-")
            frame.pack(fill=tk.X)
            
    def toggle_all_excel_items(self, all_var, vars_list):
        """Toggle all items in an Excel data block"""
        for var in vars_list:
            var.set(all_var.get())
        # Trigger plot update
        if hasattr(self.main_app, 'plot_data'):
            self.main_app.plot_data()
            
    def excel_item_toggled(self, changed_var, all_vars, all_cb_var, key):
        """Handle toggling of an Excel data item"""
        all_selected = all(var.get() for var in all_vars)
        all_cb_var.set(all_selected)
        # Trigger plot update
        if hasattr(self.main_app, 'plot_data'):
            self.main_app.plot_data()
            
    def find_wls_column_range(self, wls_value):
        """Find the column range that contains the given WLS value"""
        for range_key in self.data_dict.keys():
            match = re.search(r'WL(\d+)~WL(\d+)', range_key)
            if match:
                start_wl = int(match.group(1))
                end_wl = int(match.group(2))
                if start_wl <= wls_value <= end_wl:
                    return range_key
        return None
        
    def get_plane_for_block(self, block_number):
        """Get the plane (MAT1, MAT2, etc.) for a given block number"""
        remainder = block_number % 4
        if remainder == 0:
            return "MAT1"
        elif remainder == 1:
            return "MAT2"
        elif remainder == 2:
            return "MAT3"
        else:  # remainder == 3
            return "MAT4"
            
    def get_data_for_key(self, excel_key):
        """Get data for a given Excel key (format: 'excel|range_key|plane')"""
        parts = excel_key.split('|')
        if len(parts) != 3 or parts[0] != 'excel':
            return []
            
        range_key = parts[1]
        plane = parts[2]
        
        if range_key in self.data_dict and plane in self.data_dict[range_key]:
            # Convert string values to float, removing 'v' suffix
            values = []
            for val in self.data_dict[range_key][plane]:
                try:
                    # Remove 'v' suffix and convert to float
                    if isinstance(val, str) and val.lower().endswith('v'):
                        val = val[:-1]  # Remove the 'v'
                    values.append(float(val))
                except (ValueError, TypeError):
                    # Skip values that can't be converted
                    continue
            return values
            
        return []
        
    def get_data_for_wls_block_plane(self, wls, block, ssl=None):
        """
        Get data based on WLS, block number, and optionally SSL
        Returns data in the format needed for plotting
        """
        # Find the column range that contains the WLS value
        range_key = self.find_wls_column_range(wls)
        if not range_key:
            return []
            
        # Find the plane based on block number
        plane = self.get_plane_for_block(block)
        
        # Create the key and get the data
        excel_key = f"excel|{range_key}|{plane}"
        return self.get_data_for_key(excel_key)

# Integration with cell_distribution_app.py

def integrate_excel_processor(app):
    """Integrate the Excel processor with the main application"""
    # Create Excel processor instance
    app.excel_processor = ExcelProcessor(app)
    
    # Load Excel file automatically at startup
    app.excel_processor.load_excel_file()
    
    # Override read_data_for_key to check Excel data
    original_read_data_for_key = app.read_data_for_key
    
    def extended_read_data_for_key(key):
        """Extended version that checks Excel data first"""
        if key.startswith('excel|'):
            return app.excel_processor.get_data_for_key(key)
        else:
            return original_read_data_for_key(key)
            
    app.read_data_for_key = extended_read_data_for_key
    
    # Make sure to clean up Excel resources when the app is closed
    original_destroy = app.root.destroy
    def extended_destroy():
        if hasattr(app, 'excel_processor'):
            app.excel_processor.close_excel()
        original_destroy()
    app.root.destroy = extended_destroy
    
    return app.excel_processor

# Add this to CellDistributionApp.__init__
# self.excel_processor = integrate_excel_processor(self)

# Usage example:
# data = processor.get_data_for_wls_block_plane(10, 244)  # Gets data for WLS=10, block=244 (maps to MAT1)