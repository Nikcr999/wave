import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import numpy as np
import xlwings as xw

class ExcelHandler:
    def __init__(self, main_app):
        self.main_app = main_app
        self.excel_file_path = None
        self.z_text_row = None
        self.z_text_col = None
        self.app = None
        self.wb = None
        self.ws = None
        self.data_dict = {}
        
    def load_excel_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
        )
            
        if not file_path:
            return False
            
        try:
            self.excel_file_path = file_path
            # Initialize xlwings app
            self.app = xw.App(visible=False)
            self.wb = self.app.books.open(file_path)
            
            # Use the first sheet
            self.ws = self.wb.sheets[0]
            
            self.find_z_text()
            return True
        except Exception as e:
            messagebox.showerror("Excel Error", f"Error loading Excel file: {str(e)}")
            if self.app:
                self.app.quit()
                self.app = None
            return False
            
    def find_z_text(self):
        """Find the 'z' text in the Excel sheet"""
        if not self.ws:
            return False
            
        # Search the entire worksheet for 'z' text
        data = self.ws.used_range.value
        if not data:
            return False
            
        # Convert to list if it's not already
        if not isinstance(data, list):
            data = [[data]]
            
        for row_idx, row in enumerate(data, 1):
            if not row:
                continue
                
            for col_idx, cell_value in enumerate(row, 1):
                if cell_value and isinstance(cell_value, str) and 'z' in cell_value.lower():
                    self.z_text_row = row_idx
                    self.z_text_col = col_idx
                    print(f"Found 'z' text at row {row_idx}, column {col_idx}")
                    return True
                    
        messagebox.showwarning("Warning", "Could not find 'z' text in the Excel file.")
        return False
        
    def get_range(self, range_text):
        """Parse a range text like 'WL1~WL11(r9)' to extract start and end values"""
        # Try to match the pattern WLx~WLy
        match = re.search(r'WL(\d+)~WL(\d+)', range_text)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            return (start, end)
        
        # If no match found, return default
        return (None, None)
        
    def determine_mat_from_block(self, block_number):
        """Determine which MAT plane a block belongs to based on block number"""
        remainder = block_number % 4
        
        if remainder == 0:
            return 'MAT1'
        elif remainder == 1:
            return 'MAT2'
        elif remainder == 2:
            return 'MAT3'
        elif remainder == 3:
            return 'MAT4'
        
    def extract_wls_data(self, wls_value, block_number):
        """Extract data for a specific WLS value and block number"""
        if not self.z_text_row or not self.ws:
            return []
            
        try:
            # Get the entire data range as a 2D array
            data = self.ws.used_range.value
            if not data:
                return []
                
            # Find which column range contains the WLS value
            wls_col = None
            
            # Scan the header row (same row as z_text_row) for column headers
            header_row = data[self.z_text_row - 1]  # Adjust for 0-indexing
            for col_idx, cell_value in enumerate(header_row):
                if cell_value and isinstance(cell_value, str) and 'WL' in cell_value:
                    start, end = self.get_range(cell_value)
                    if start is not None and end is not None:
                        # Check if the WLS value is within this range
                        if start <= wls_value <= end:
                            # Calculate column offset within the range
                            wls_col = col_idx + (wls_value - start)
                            break
            
            if wls_col is None:
                return []
                
            # Determine MAT plane based on block number
            mat_plane = self.determine_mat_from_block(block_number)
            
            # Find MAT plane row
            mat_row = None
            for row_idx, row in enumerate(data):
                if row_idx <= self.z_text_row:
                    continue
                    
                if row and row[0] and isinstance(row[0], str) and mat_plane in row[0]:
                    mat_row = row_idx
                    break
                    
            if mat_row is None:
                return []
                
            # Extract data - assuming 15 rows for each MAT plane
            voltage_values = []
            for row_idx in range(mat_row, min(mat_row + 15, len(data))):
                if row_idx < len(data) and wls_col < len(data[row_idx]):
                    cell_value = data[row_idx][wls_col]
                    if cell_value is not None:
                        try:
                            # Try to extract the voltage value
                            if isinstance(cell_value, (int, float)):
                                voltage_values.append(cell_value)
                            else:
                                # Try to extract a number from text
                                value_match = re.search(r'([-+]?\d*\.\d+|\d+)', str(cell_value))
                                if value_match:
                                    voltage_values.append(float(value_match.group(1)))
                        except (ValueError, TypeError):
                            pass
                            
            return voltage_values
        except Exception as e:
            print(f"Error extracting WLS data: {str(e)}")
            return []
            
    def process_selected_checkbox(self):
        """Process the last selected checkbox to extract data"""
        if not hasattr(self.main_app, 'last_selected_key') or not self.main_app.last_selected_key:
            return False, {}
            
        key = self.main_app.last_selected_key
        key_parts = key.split('|')
        
        if len(key_parts) < 2:
            return False, {}
            
        data_key = key_parts[1]
        key_type_parts = data_key.split('_')
        
        if len(key_type_parts) < 3:
            return False, {}
            
        key_type = key_type_parts[0]
        
        if key_type != 'w':  # Only process WLS type keys
            return False, {}
            
        try:
            wls = int(key_type_parts[1])
            ssl = int(key_type_parts[2])
            
            # Get block number
            block = None
            from tabs.main_tab.read import extract_block_info
            
            file_idx = int(key_parts[0])
            if hasattr(self.main_app, 'file_paths') and file_idx < len(self.main_app.file_paths):
                with open(self.main_app.file_paths[file_idx], 'r') as file:
                    for line in file:
                        if any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
                            block_info = extract_block_info(line)
                            # Extract block number (B:244)
                            block_match = re.search(r'B:(\d+)', block_info)
                            if block_match:
                                block = int(block_match.group(1))
                                break
            
            if block is None:
                return False, {}
                
            # Extract data
            voltage_values = self.extract_wls_data(wls, block)
            
            if not voltage_values:
                return False, {}
                
            # Format results
            mat_plane = self.determine_mat_from_block(block)
            result_dict = {
                str(wls): {
                    mat_plane: voltage_values
                }
            }
            
            return True, result_dict
            
        except (ValueError, IndexError) as e:
            print(f"Error processing checkbox: {str(e)}")
            return False, {}

    def close(self):
        """Close Excel application to free resources"""
        if self.app:
            try:
                self.app.quit()
            except:
                pass
            self.app = None
            
def setup_excel_handler(app):
    """Setup the Excel handler for the main application"""
    app.excel_handler = ExcelHandler(app)
    
    # Override the load_file function to also load Excel
    original_load_file = app.load_file
    
    def extended_load_file():
        result = original_load_file()
        # After loading text files, try to load Excel
        app.excel_handler.load_excel_file()
        return result
        
    app.load_file = extended_load_file