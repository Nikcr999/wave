from tkinter import filedialog, messagebox

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if self.file_path:
        parse_file(self)
        self.update_checkboxes()

def parse_file(self):
    self.data.clear()
    current_wls, current_ssl = None, None
    current_data = []

    with open(self.file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if "START_SANPO" in line:
                if current_wls is not None and current_ssl is not None and current_data:
                    self.data[(current_wls, current_ssl)] = current_data
                current_wls, current_ssl = None, None
                current_data = []

            elif "WLS:" in line and "SSL:" in line:
                parts = line.split(',')
                for part in parts:
                    if "WLS:" in part:
                        current_wls = part.split("WLS:")[1].strip()
                    if "SSL:" in part:
                        current_ssl = part.split("SSL:")[1].strip()

            elif line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                current_data.append(float(line))

            elif "END_SANPO" in line:
                if current_wls is not None and current_ssl is not None and current_data:
                    self.data[(current_wls, current_ssl)] = current_data