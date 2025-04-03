from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import os

def load_file(self):
    file_paths = filedialog.askopenfilenames(filetypes=[("Text file", "*.txt")])
    if file_paths:
        try:
            # Initialize file paths list if not already done
            if not hasattr(self, 'file_paths'):
                self.file_paths = []
            
            # Check for duplicate files and only add new ones
            new_files_added = False
            for file_path in file_paths:
                # Check if this exact file path exists
                if file_path not in self.file_paths:
                    # Also check if file with same name already exists (different path)
                    file_name = os.path.basename(file_path)
                    duplicate = False
                    for existing_path in self.file_paths:
                        if os.path.basename(existing_path) == file_name:
                            duplicate = True
                            break
                    
                    # If not a duplicate, add it
                    if not duplicate:
                        self.file_paths.append(file_path)
                        new_files_added = True
            
            # Only update UI if we actually added new files
            if new_files_added:
                self.update_checkboxes()
                # Set title to just "Cell Distribution" without the filename
                self.plot_title.config(text="Cell Distribution")
            else:
                messagebox.showinfo("Information", "No new files added. Same files are already loaded.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def read_data_for_key(self, target_key):
    # Split target key to extract file index and data key
    parts = target_key.split('|')
    if len(parts) < 2:
        return []
    
    file_idx = int(parts[0])
    data_key = parts[1]
    
    if not hasattr(self, 'file_paths') or file_idx >= len(self.file_paths):
        return []
    
    file_path = self.file_paths[file_idx]
    
    # Get data point length if we already know it
    data_length = self.data_point_length if hasattr(self, 'data_point_length') else None
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_data = []
    current_key = None
    inside_data_block = False
    found_data = []
    skip_count = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip lines if we're counting through data points and know how many to skip
        if skip_count > 0:
            skip_count -= 1
            continue
            
        if line.startswith('START_SANPO'):
            inside_data_block = True
            continue
            
        if line.startswith('END_SANPO'):
            if current_key == data_key and current_data:
                found_data = current_data
            inside_data_block = False
            current_data = []
            current_key = None
            continue
        
        if not inside_data_block:
            continue
            
        if any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
            if current_key == data_key and current_data:
                found_data = current_data.copy()
                
            # If we found data previously and now hit a new combination, we can return
            if found_data:
                return found_data
                
            current_data = []
            current_key = _parse_key(self, line)
            
            # If we know data length and this isn't our target, skip ahead
            if data_length is not None and current_key != data_key:
                skip_count = data_length
        else:
            try:
                value = float(line)
                current_data.append(value)
                
                # If this is the first dataset, save its length for future optimizations
                if len(current_data) == 1 and data_length is None:
                    # Count how many numerical lines follow
                    count = 1
                    for next_line in lines[i+1:]:
                        next_line = next_line.strip()
                        try:
                            float(next_line)
                            count += 1
                        except ValueError:
                            break
                    self.data_point_length = count
            except ValueError:
                continue
                
    return found_data

def check_key_exists(self, key):
    return True

def update_checkboxes(self):
    # Clear existing checkboxes
    for widget in self.scrollable_frame.winfo_children():
        widget.destroy()

    # Clear checkbox variables
    if hasattr(self, 'checkboxes'):
        self.checkboxes.clear()
    else:
        self.checkboxes = {}

    # Create a new frame inside the canvas to hold the checkboxes
    self.inner_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

    # Configure style for checkboxes
    style = ttk.Style()
    style.configure('Checkbox.TCheckbutton', 
                   background='white',
                   font=('Helvetica', 9))

    # Sample data structure (replace with real data extraction)
    sample_blocks = {
        "F:0,C:0,W:0": [(f"0|sample_{i}", f"WLS: {i}, SSL: 1") for i in range(1, 6000)],
        "F:1,C:1,W:1": [(f"1|sample_{i}", f"DUMMY: A{i}, SSL: 2") for i in range(1, 8000)],
        "F:2,C:2,W:2": [(f"2|sample_{i}", f"CDUMMY: B{i}, SSL: 3") for i in range(1, 10000)]
    }

    # Create blocks from sample data
    for block_name, items in sample_blocks.items():
        create_block(self, self.inner_frame, block_name, items)

    # Update the canvas to fit the new content
    self.inner_frame.update_idletasks()
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def create_block(self, parent, block_name, items):
    block_frame = ttk.Frame(parent)
    block_frame.pack(fill=tk.X, anchor=tk.W, pady=2)

    # Create header frame for the block title and toggle button
    header_frame = ttk.Frame(block_frame)
    header_frame.pack(fill=tk.X)

    # Create a separate frame for the items that can be toggled
    items_frame = ttk.Frame(block_frame)

    # Toggle button for expanding/collapsing the block
    toggle_btn = tk.Button(
        header_frame,
        text="+",
        width=2,
        font=('Arial', 8, 'bold'),
        bg='white',
        relief='flat'
    )
    toggle_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Select all checkbox for the block
    select_all_var = tk.BooleanVar()
    select_all_cb = ttk.Checkbutton(
        header_frame,
        text=block_name,
        variable=select_all_var,
        style='Checkbox.TCheckbutton'
    )
    select_all_cb.pack(side=tk.LEFT, padx=5, fill=tk.X)

    # List to store all checkbox variables for this block
    item_vars = []

    # Create checkboxes for each item
    for key, label in items:
        var = tk.BooleanVar()
        self.checkboxes[key] = var
        item_vars.append(var)

        checkbox = ttk.Checkbutton(
            items_frame,
            text=label,
            variable=var,
            style='Checkbox.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W, padx=(20, 0), fill=tk.X)

    # Force update geometry after adding checkboxes
    items_frame.update_idletasks()

    # Define toggle block function
    def toggle_block():
        if items_frame.winfo_manager():
            toggle_btn.config(text="+")
            items_frame.pack_forget()
        else:
            toggle_btn.config(text="-")
            items_frame.pack(fill=tk.X)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Attach command to toggle button
    toggle_btn.config(command=toggle_block)

    # Define function to toggle all items in the block
    def toggle_all_items():
        for var in item_vars:
            var.set(select_all_var.get())
        if hasattr(self, 'plot_data'):
            self.plot_data()

    # Attach command to select all checkbox
    select_all_cb.config(command=toggle_all_items)

    # Define function for individual item toggle
    def item_toggled(event=None):
        all_selected = all(var.get() for var in item_vars)
        select_all_var.set(all_selected)
        if hasattr(self, 'plot_data'):
            self.plot_data()

    # Attach toggle callback to each checkbox
    for var in item_vars:
        var.trace_add("write", lambda *args, v=var: item_toggled())

    return block_frame


def extract_blocks_from_file(self, file_idx, file_path):
    blocks = {}
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
        block_info = None
        inside_data_block = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('START_SANPO'):
                inside_data_block = True
                continue
                
            if line.startswith('END_SANPO'):
                inside_data_block = False
                continue
            
            if inside_data_block and any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
                # Extract the block info part (everything up to WLS, DUMMY, or CDUMMY)
                if block_info is None:
                    block_info = extract_block_info(line)
                
                if block_info not in blocks:
                    blocks[block_info] = []
                
                # Parse the key for this line
                data_key = _parse_key(self, line)
                
                # Create a composite key that includes file index and data key
                composite_key = f"{file_idx}|{data_key}"
                
                # Get label for display (just the combination part)
                display_label = create_display_label(line)
                
                # Add to block items
                blocks[block_info].append((composite_key, display_label))
                
    except Exception as e:
        print(f"Error extracting blocks from {file_path}: {str(e)}")
    
    return blocks

def extract_block_info(line):
    """Extract abbreviated block identifier from the line (using initials)"""
    # Find where the WLS, DUMMY, or CDUMMY part starts
    split_indices = []
    if "WLS:" in line:
        split_indices.append(line.find("WLS:"))
    if "DUMMY:" in line:
        split_indices.append(line.find("DUMMY:"))
    if "CDUMMY:" in line:
        split_indices.append(line.find("CDUMMY:"))
    
    # If we found any split points, use the earliest one
    if split_indices:
        split_point = min(split_indices)
        block_part = line[:split_point].strip()
        if block_part.endswith(','):
            block_part = block_part[:-1]  # Remove trailing comma
        
        # Convert to abbreviated format (F:0,C:0,W:0,D:0,B:244)
        parts = [part.strip() for part in block_part.split(',')]
        abbreviated_parts = []
        
        for part in parts:
            if ':' in part:
                prefix, value = part.split(':', 1)
                abbreviated_parts.append(f"{prefix[0]}:{value}")
        
        return ",".join(abbreviated_parts)
    
    # Fallback if we couldn't split properly
    return "Unknown"

def create_display_label(line):
    """Create a display label for a data point - just the combination part"""
    # Find where the WLS, DUMMY, or CDUMMY part starts
    split_indices = []
    if "WLS:" in line:
        split_indices.append(line.find("WLS:"))
    if "DUMMY:" in line:
        split_indices.append(line.find("DUMMY:"))
    if "CDUMMY:" in line:
        split_indices.append(line.find("CDUMMY:"))
    
    # If we found any split points, use the earliest one
    if split_indices:
        split_point = min(split_indices)
        # Get the combination part (everything after the split point)
        combination_part = line[split_point:].strip()
        return combination_part
    
    # Fallback
    return line



def _parse_key(self, line):
    parts = [part.strip() for part in line.split(',')]
    wls = dummy = cdummy = ssl = None
    
    for part in parts:
        if "WLS:" in part:
            wls = int(part.split("WLS:")[1].strip())
        elif "DUMMY:" in part:
            dummy = part.split("DUMMY:")[1].strip()
        elif "CDUMMY:" in part:
            cdummy = part.split("CDUMMY:")[1].strip()
        elif "SSL:" in part:
            ssl = int(part.split("SSL:")[1].strip())
    
    if wls is not None and ssl is not None:
        return f"w_{wls}_{ssl}"
    elif dummy is not None and ssl is not None:
        return f"d_{dummy}_{ssl}"
    elif cdummy is not None and ssl is not None:
        return f"c_{cdummy}_{ssl}"
    
    return None