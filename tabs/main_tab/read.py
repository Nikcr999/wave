from tkinter import filedialog, messagebox, ttk
import tkinter as tk

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if self.file_path:
        try:
            self.update_checkboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def read_data_for_key(self, target_key):
    with open(self.file_path, 'r') as file:
        lines = file.readlines()
    
    current_data = []
    current_key = None
    inside_data_block = False
    found_data = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('START_SANPO'):
            inside_data_block = True
            continue
            
        if line.startswith('END_SANPO'):
            if current_key == target_key and current_data:
                found_data = current_data
            inside_data_block = False
            current_data = []
            current_key = None
            continue
        
        if not inside_data_block:
            continue
            
        if any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
            if current_key == target_key and current_data:
                found_data = current_data.copy()
            current_data = []
            current_key = _parse_key(self, line)
        else:
            try:
                value = float(line)
                current_data.append(value)
            except ValueError:
                continue
                
    return found_data

def check_key_exists(self, key):
    return True

def update_checkboxes(self):
    for widget in self.scrollable_frame.winfo_children():
        widget.destroy()
    self.checkboxes.clear()
    
    style = ttk.Style()
    style.configure('Checkbox.TCheckbutton', 
                   background='white',
                   font=('Helvetica', 9))
    
    all_combinations = []
    
    for wls in range(175, -1, -1):
        for ssl in range(8):
            key = f"w_{wls}_{ssl}"
            all_combinations.append((key, f"WLS:{wls}, SSL:{ssl}"))
            
    for dummy in range(2, 0, -1):
        for ssl in range(8):
            key = f"d_{dummy}_{ssl}"
            all_combinations.append((key, f"DUMMY:{dummy}, SSL:{ssl}"))
            
    cdummy_ssl_ranges = {3: range(8), 0: range(7)}
    for cdummy, ssl_range in cdummy_ssl_ranges.items():
        for ssl in ssl_range:
            key = f"c_{cdummy}_{ssl}"
            all_combinations.append((key, f"CDUMMY:{cdummy}, SSL:{ssl}"))

    container_frame = ttk.Frame(self.scrollable_frame, style='TFrame')
    container_frame.pack(fill=tk.BOTH, expand=True)

    for key, label in all_combinations:
        var = tk.BooleanVar()
        self.checkboxes[key] = var
        checkbox = ttk.Checkbutton(
            container_frame,
            text=label,
            variable=var,
            command=self.plot_data,
            style='Checkbox.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W, padx=5)

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