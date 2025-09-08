import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService

class LoginWindow:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        self.auth_service = AuthService()
        
        #!Creating the window
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Login")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #!Title
        title_label = ttk.Label(main_frame, text="Admin Login", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        #!Username
        ttk.Label(main_frame, text="Username:").pack(anchor="w")
        self.username_entry = ttk.Entry(main_frame, width=25)
        self.username_entry.pack(pady=(0, 10))
        
        #!Password
        ttk.Label(main_frame, text="Password:").pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, width=25, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        #!Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.window.destroy)
        cancel_btn.pack(side=tk.LEFT)
        
        #!Bind Enter key to login function (WHAT IS LAMBDA I SWEAR)
        self.window.bind('<Return>', lambda e: self.login())
        
        #!Focus on username entry
        self.username_entry.focus()
    
    def center_window(self):
        self.window.update_idletasks() #!Update the window to get its size active
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2) #!Centering the window
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2) #!Centering the window
        self.window.geometry(f"+{x}+{y}") #!Setting the position of the window
    
    def login(self):
        #!Getting username and password
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if self.auth_service.login(username, password):
            self.on_login_success(self.auth_service)
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)