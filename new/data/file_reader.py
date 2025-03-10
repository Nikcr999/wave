"""
File reader module for handling data files.
Contains functions for loading, parsing, and reading data files.
"""
import os
from tkinter import filedialog, messagebox
import tkinter as tk

import state
from ui.sidebar import update_checkboxes

def load_file():
    """
    Open file dialog and load selected files.
    Updates global state with file paths.
    """
    file_paths = filedialog.askopenfilenames(filetypes=[("Text file", "*.txt")])
    if file_paths:
        try:
            # Check for duplicate files and only add new ones
            new_files_added = False
            for file_path in file_paths:
                # Check if this exact file path exists
                if file_path not in state.file_paths:
                    # Also check if file with same name already exists (different path)
                    file_name = os.path.basename(file_path)
                    duplicate = False
                    for existing_path in state.file_paths:
                        if os.path.basename(existing_path) == file_name:
                            duplicate = True
                            break
                    
                    # If not a duplicate, add it
                    if not duplicate:
                        state.file_paths.append(file_path)
                        new_files_added = True
            
            # Only update UI if we actually added new files
            if new_files_added:
                update_checkboxes()
                
                # Set title to just "Cell Distribution" without the filename
                if state.plot_title:
                    state.plot_title.config(text="Cell Distribution")
            else:
                messagebox.showinfo("Information", "No new files added. Same files are already loaded.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def read_data_for_key(target_key):
    """
    Read data for a specific key from a file
    
    Args:
        target_key: Key to read data for (format: "file_idx|data_key")
        
    Returns:
        List of data values or empty list if key not found
    """
    # Split target key to extract file index and data key
    parts = target_key.split('|')
    if len(parts) < 2:
        return []
    
    file_idx = int(parts[0])
    data_key = parts[1]
    
    if file_idx >= len(state.file_paths):
        return []
    
    file_path = state.file_paths[file_idx]
    
    # Get data point length if we already know it
    data_length = state.data_point_length
    
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
            current_key = parse_key(line)
            
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
                    state.data_point_length = count
            except ValueError:
                continue
                
    return found_data

def parse_key(line):
    """
    Parse a key from a line in the data file
    
    Args:
        line: Line containing data key information
        
    Returns:
        Parsed key string or None if no key found
    """
    parts = [part.strip() for part in line.split(',')]
    wls = dummy = cdummy = ssl = None
    
    for part in parts:
        if "WLS:" in part:
            try:
                wls = int(part.split("WLS:")[1].strip())
            except ValueError:
                wls = part.split("WLS:")[1].strip()
        elif "DUMMY:" in part:
            dummy = part.split("DUMMY:")[1].strip()
        elif "CDUMMY:" in part:
            cdummy = part.split("CDUMMY:")[1].strip()
        elif "SSL:" in part:
            try:
                ssl = int(part.split("SSL:")[1].strip())
            except ValueError:
                ssl = part.split("SSL:")[1].strip()
    
    if wls is not None and ssl is not None:
        return f"w_{wls}_{ssl}"
    elif dummy is not None and ssl is not None:
        return f"d_{dummy}_{ssl}"
    elif cdummy is not None and ssl is not None:
        return f"c_{cdummy}_{ssl}"
    
    return None

def extract_block_info(line):
    """
    Extract abbreviated block identifier from the line (using initials)
    
    Args:
        line: Line containing block information
        
    Returns:
        Abbreviated block identifier string
    """
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
    """
    Create a display label for a data point - just the combination part
    
    Args:
        line: Line containing data specification
        
    Returns:
        Display label string
    """
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

def extract_blocks_from_file(file_idx, file_path):
    """
    Extract all data blocks from a file
    
    Args:
        file_idx: Index of the file in the global file paths list
        file_path: Path to the file to extract blocks from
        
    Returns:
        Dictionary of block names mapped to lists of (key, label) tuples
    """
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
                block_info = None  # Reset block info for each new block
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
                data_key = parse_key(line)
                if data_key is None:
                    continue  # Skip if no valid key found
                
                # Create a composite key that includes file index and data key
                composite_key = f"{file_idx}|{data_key}"
                
                # Get label for display (just the combination part)
                display_label = create_display_label(line)
                
                # Check if this key already exists in the block
                exists = False
                for existing_key, _ in blocks[block_info]:
                    if existing_key == composite_key:
                        exists = True
                        break
                
                # Add to block items if not a duplicate
                if not exists:
                    blocks[block_info].append((composite_key, display_label))
                
    except Exception as e:
        if state.debug_mode:
            print(f"Error extracting blocks from {file_path}: {str(e)}")
        messagebox.showerror("Error", f"Failed to process file {os.path.basename(file_path)}: {str(e)}")
    
    return blocks

def check_key_exists(key):
    """
    Check if a data key exists in any of the loaded files
    
    Args:
        key: Key to check (format: "file_idx|data_key")
        
    Returns:
        Boolean indicating if the key exists
    """
    data = read_data_for_key(key)
    return len(data) > 0