import tkinter as tk
from tabs.tab_one.cell_distribution_app import CellDistributionApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CellDistributionApp(root)
    root.geometry("1200x700")
    root.mainloop()
