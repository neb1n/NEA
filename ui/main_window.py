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
        self.root.configure(bg="#f5f6fa")  # Light background

        self.current_interface = None
        self.auth_service = None

        self.setup_ui()
        self.show_user_interface()

    def setup_ui(self):
        # Main container
        self.main_container = ttk.Frame(self.root, style="Main.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Remove menu bar for a cleaner look
        self.root.config(menu=tk.Menu(self.root))  # Empty menu

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_user_interface(self):
        self.clear_container()
        self.current_interface = UserInterface(self.main_container, self.show_admin_login)
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
        self.current_interface = AdminInterface(self.main_container, self.auth_service, logout_callback=self.logout_admin)
        self.root.title("Movie Theater Reservation System - Admin Panel")

    def logout_admin(self):
        if self.auth_service:
            self.auth_service.logout()
        self.show_user_interface()
