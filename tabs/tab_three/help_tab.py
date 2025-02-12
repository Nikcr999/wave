import tkinter as tk
from tkinter import ttk

class HelpTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Help Section Coming Soon!").pack(pady=20)
