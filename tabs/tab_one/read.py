from tkinter import filedialog, messagebox

def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if self.file_path:
        parse_file(self)
        self.update_checkboxes(175)  

def parse_file(self):
    self.data.clear()  
    current_key = None 
    current_data = []
    parsing = False  

    with open(self.file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if "START" in line:
                parsing = True
                continue 

            if "END" in line:
                if current_key and current_data:
                    self.data[current_key] = current_data
                break  

            if parsing and ("WLS:" in line or "DUMMY:" in line or "CDUMMY:" in line) and "SSL:" in line:
                parts = line.split(',')
                wls = dummy = cdummy = ssl = None

                for part in parts:
                    part = part.strip()
                    if "WLS:" in part:
                        wls = int(part.split("WLS:")[1].strip())
                    elif "DUMMY:" in part:
                        dummy = f"DUMMY:{part.split('DUMMY:')[1].strip()}"
                    elif "CDUMMY:" in part:
                        cdummy = f"CDUMMY:{part.split('CDUMMY:')[1].strip()}"
                    elif "SSL:" in part:
                        ssl = int(part.split("SSL:")[1].strip())

                if wls is not None and ssl is not None:
                    current_key = (wls, ssl)
                elif dummy is not None and ssl is not None:
                    current_key = (dummy, ssl)
                elif cdummy is not None and ssl is not None:
                    current_key = (cdummy, ssl)
                else:
                    continue  

                if current_key not in self.data:
                    self.data[current_key] = []

            elif parsing and (line.replace('.', '', 1).isdigit() or (line.startswith('-') and line[1:].replace('.', '', 1).isdigit())):
                if current_key:
                    self.data[current_key].append(float(line))
