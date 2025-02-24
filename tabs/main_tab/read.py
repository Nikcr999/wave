from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import os

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if self.file_path:
        try:
            self.update_checkboxes()
            self.plot_title.config(text="Cell Distribution")
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
    
    container_frame = ttk.Frame(self.scrollable_frame, style='TFrame')
    container_frame.pack(fill=tk.BOTH, expand=True)
    
    all_items = []
    
    for wls in range(175, -1, -1):
        for ssl in range(8):
            key = f"w_{wls}_{ssl}"
            all_items.append((key, f"WLS:{wls}, SSL:{ssl}"))
            
    for dummy in range(2, 0, -1):
        for ssl in range(8):
            key = f"d_{dummy}_{ssl}"
            all_items.append((key, f"DUMMY:{dummy}, SSL:{ssl}"))
            
    cdummy_ssl_ranges = {3: range(8), 0: range(7)}
    for cdummy, ssl_range in cdummy_ssl_ranges.items():
        for ssl in ssl_range:
            key = f"c_{cdummy}_{ssl}"
            all_items.append((key, f"CDUMMY:{cdummy}, SSL:{ssl}"))
    
    block_name = "Block_Name"
    if hasattr(self, 'file_path') and self.file_path:
        file_name = os.path.basename(self.file_path)
        block_name = os.path.splitext(file_name)[0]
        
        if hasattr(self, 'table_title_label'):
            self.table_title_label.config(text=block_name)
    
    create_block(self, container_frame, block_name, all_items)

def create_block(self, parent, block_name, items):
    block_frame = ttk.Frame(parent, style='TFrame')
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
        command=lambda: toggle_block(toggle_btn, items_frame)
    )
    toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    select_all_var = tk.BooleanVar()
    select_all_cb = ttk.Checkbutton(
        header_frame,
        text=block_name,
        variable=select_all_var,
        style='Checkbox.TCheckbutton',
        command=lambda: toggle_all_items(select_all_var, item_vars)
    )
    select_all_cb.pack(side=tk.LEFT, padx=5)
    
    item_vars = []
    for key, label in items:
        var = tk.BooleanVar()
        self.checkboxes[key] = var
        item_vars.append(var)
        checkbox = ttk.Checkbutton(
            items_frame,
            text=label,
            variable=var,
            command=lambda v=var, k=key: item_toggled(v, item_vars, select_all_var),
            style='Checkbox.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W, padx=(20, 0))
    
    def toggle_block(btn, frame):
        if frame.winfo_manager():
            btn.config(text="+")
            frame.pack_forget()
        else:
            btn.config(text="-")
            frame.pack(fill=tk.X)
    
    def toggle_all_items(all_var, vars_list):
        for var in vars_list:
            var.set(all_var.get())
        self.plot_data()
    
    def item_toggled(changed_var, all_vars, all_cb_var):
        all_selected = all(var.get() for var in all_vars)
        all_cb_var.set(all_selected)
        self.plot_data()

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