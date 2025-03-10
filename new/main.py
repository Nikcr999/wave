"""
Main entry point for the Cell Distribution Analysis application.
Uses a functional approach with global state.
"""
import tkinter as tk
from tkinter import ttk
import atexit

# Import global state
import state

# Import UI modules
from ui.styles import setup_styles
from ui.main_window import create_main_window
from ui.notebook import setup_notebook
from ui.buttons import create_button_panel
from ui.sidebar import create_sidebar
from ui.plot import setup_plot_area
from ui.table import setup_table
from ui.developer_tab import setup_developer_tab
from ui.help_tab import setup_help_tab

def setup_application():
    """Set up the complete application UI"""
    # Create main window
    state.root = create_main_window()
    
    # Set up styles
    setup_styles()
    
    # Create notebook with tabs
    state.notebook, state.tab1, state.tab2, state.tab3 = setup_notebook(state.root)
    
    # Create components for main tab
    create_button_panel(state.tab1)
    state.main_container = ttk.PanedWindow(state.tab1, orient=tk.HORIZONTAL)
    state.main_container.pack(fill=tk.BOTH, expand=True)
    
    # Create sidebar
    create_sidebar()
    
    # Create content frame
    content_frame = ttk.Frame(state.main_container, style='TFrame')
    state.main_container.add(content_frame)
    
    # Setup plot area
    setup_plot_area(content_frame)
    
    # Setup table
    setup_table()
    
    # Setup other tabs
    setup_developer_tab()
    setup_help_tab()
    
    # Create footer
    setup_footer()
    
    return state.root

def setup_footer():
    """Create footer with version information"""
    VERSION = "1.0.0"
    DEVELOPER = "Nikhil"
    
    footer = ttk.Label(
        state.root,
        text=f"Version {VERSION} | Developed by {DEVELOPER}",
        style='Footer.TLabel',
        anchor='e'
    )
    footer.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

def main():
    """Main application entry point"""
    # Initialize global state
    state.init()
    
    # Set up the application
    root = setup_application()
    
    # Initialize Tkinter variables after root is created
    state.resolution_var = tk.StringVar(value="40")
    state.wls_var = tk.StringVar()
    state.dummy_var = tk.StringVar()
    state.cdummy_var = tk.StringVar()
    state.ssl_var = tk.StringVar()
    
    # Register cleanup function
    atexit.register(state.cleanup)
    
    # Start main loop
    root.geometry("1024x768")
    root.mainloop()

if __name__ == "__main__":
    main()