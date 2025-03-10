"""
Styles module for setting up the application's visual styles.
"""
from tkinter import ttk

def setup_styles():
    """
    Set up the application's visual styles
    """
    style = ttk.Style()
    
    # Frame styles
    style.configure('TFrame', background='white')
    style.configure('OuterBorder.TFrame', relief='solid', borderwidth=2)
    style.configure('Bordered.TFrame', relief='solid', borderwidth=1)
    
    # Label styles
    style.configure('TLabel', background='white')
    style.configure('Footer.TLabel', background='white', font=('Helvetica', 8))
    
    # Table styles
    style.configure('Header1.TLabel', 
                   background='#1e40af',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('Header2.TLabel',
                   background='white',
                   foreground='red',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('Cell.TLabel',
                   background='#dbeafe',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('CellWhite.TLabel',
                   background='white',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
    
    # Notebook styles
    style.configure('TNotebook', background='white')
    style.configure('TNotebook.Tab', background='white', padding=(10, 5), font=('', 10))
    
    # Treeview styles
    style.configure('Treeview', background='white', fieldbackground='white')
    
    # Other widget styles
    style.configure('TCanvas', background='white')
    
    # Analysis table styles
    style.configure('Analysis.TLabel',
                   background='#fef3c7',
                   foreground='black',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('AnalysisHeader.TLabel',
                   background='#d97706',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9, 'bold'),
                   borderwidth=1,
                   relief='solid')
                   
    style.configure('AnalysisKey.TLabel',
                   background='#155e75',
                   foreground='white',
                   padding=(2, 0),
                   font=('Helvetica', 9),
                   borderwidth=1,
                   relief='solid')
    
    # Checkbox style
    style.configure('Checkbox.TCheckbutton', 
                   background='white',
                   font=('Helvetica', 9))