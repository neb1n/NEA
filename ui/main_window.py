import tkinter as tk
from tkinter import ttk, messagebox
from ui.user_interface import UserInterface
from ui.admin_interface import AdminInterface
from ui.login_window import LoginWindow
from ui.theme import Colors

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Theater Reservation System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        #!Background from theme
        self.root.configure(bg=Colors.BACKGROUND)

        self.current_interface = None
        self.auth_service = None

        self.setup_ui()
        self.show_user_interface()

    def setup_ui(self):
        #!Main container
        style = ttk.Style()
        style.configure("Main.TFrame", background=Colors.BACKGROUND)
        self.main_container = ttk.Frame(self.root, style="Main.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        #!Sets empty menu
        self.root.config(menu=tk.Menu(self.root))
        #!Clears the menu
    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        #!Pulls user interface
    def show_user_interface(self):
        self.clear_container()
        self.current_interface = UserInterface(self.main_container, self.show_admin_login)
        self.root.title("Movie Theater Reservation System - User Interface")

    def show_admin_login(self):
        LoginWindow(self.root, self.on_admin_login_success)

    def on_admin_login_success(self, auth_service):
        self._finalize_admin_login(auth_service)

    def _finalize_admin_login(self, auth_service):
        self.auth_service = auth_service
        try:
            self.show_admin_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open admin interface: {e}")
            #!Exception handling
            self.show_user_interface()

    def show_admin_interface(self):
        if not self.auth_service or not self.auth_service.is_authenticated():
            self.show_admin_login()
            return
        #!Runs the admin interface together
        self.clear_container()
        self.current_interface = AdminInterface(self.main_container, self.auth_service, logout_callback=self.logout_admin)
        self.root.title("Movie Theater Reservation System - Admin Panel")
    #!Logging out
    def logout_admin(self):
        if self.auth_service:
            self.auth_service.logout()
        self.show_user_interface()
