from tkinter import filedialog, messagebox, ttk
import tkinter as tk

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if self.file_path:
        try:
            self.parse_file()
            self.update_checkboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def parse_file(self):
    with open(self.file_path, 'r') as file:
        lines = file.readlines()
    
    self.data.clear()
    current_data = []
    current_key = None
    inside_data_block = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('START_SANPO'):
            inside_data_block = True
            continue
            
        if line.startswith('END_SANPO'):
            if current_key and current_data:
                self.data[current_key] = current_data
            inside_data_block = False
            current_data = []
            current_key = None
            continue
        
        if not inside_data_block:
            continue
            
        if any(x in line for x in ['WLS:', 'DUMMY:', 'CDUMMY:']):
            if current_key and current_data:
                self.data[current_key] = current_data.copy()
                current_data = []
            current_key = _parse_key(self, line)
        else:
            try:
                value = float(line)
                current_data.append(value)
            except ValueError:
                continue

def update_checkboxes(self):
    for widget in self.scrollable_frame.winfo_children():
        widget.destroy()
    self.checkboxes.clear()
    
    all_combinations = []
    for wls in range(175, -1, -1):
        for ssl in range(8):
            all_combinations.append((wls, ssl))
            
    for dummy in range(2, -1, -1):
        for ssl in range(8):
            all_combinations.append((dummy, ssl))
        
    for cdummy in range(2, -1, -1):
        for ssl in range(8):
            all_combinations.append((cdummy, ssl))

    for key in all_combinations:
        var = tk.BooleanVar()
        self.checkboxes[key] = var
        if isinstance(key[0], int):
            label = f"WLS:{key[0]}, SSL:{key[1]}"
        else:
            label = f"{key[0]}, SSL:{key[1]}"
            
        has_data = key in self.data and self.data[key]
        checkbox = ttk.Checkbutton(
            self.scrollable_frame, 
            text=label, 
            variable=var,
            command=self.plot_selected,
            state='normal' if has_data else 'disabled'
        )
        checkbox.pack(anchor=tk.W)

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
        return (wls, ssl)
    elif dummy is not None and ssl is not None:
        return (f"DUMMY:{dummy}", ssl)
    elif cdummy is not None and ssl is not None:
        return (f"CDUMMY:{cdummy}", ssl)
    
    return None