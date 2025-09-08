import tkinter as tk
from ui.main_window import MainWindow
from db.init_db import init_database

def main():
    # Initialize database
    init_database()
    
    # Create main window
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()