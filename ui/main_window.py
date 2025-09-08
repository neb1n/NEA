import tkinter as tk
from tkinter import ttk
from ui.user_interface import UserInterface
from ui.admin_interface import AdminInterface
from ui.login_window import LoginWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Theater Reservation System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        self.current_interface = None
        self.auth_service = None
        
        self.setup_ui()
        self.show_user_interface()
    
    def setup_ui(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Interface menu
        interface_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Interface", menu=interface_menu)
        interface_menu.add_command(label="User Interface", command=self.show_user_interface)
        interface_menu.add_command(label="Admin Login", command=self.show_admin_login)
        interface_menu.add_separator()
        interface_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_user_interface(self):
        self.clear_container()
        self.current_interface = UserInterface(self.main_container)
        self.root.title("Movie Theater Reservation System - User Interface")
    
    def show_admin_login(self):
        LoginWindow(self.root, self.on_admin_login_success)
    
    def on_admin_login_success(self, auth_service):
        self.auth_service = auth_service
        self.show_admin_interface()
    
    def show_admin_interface(self):
        if not self.auth_service or not self.auth_service.is_authenticated():
            self.show_admin_login()
            return
        
        self.clear_container()
        self.current_interface = AdminInterface(self.main_container, self.auth_service)
        self.root.title("Movie Theater Reservation System - Admin Panel")
    
    def show_about(self):
        about_text = ""
        