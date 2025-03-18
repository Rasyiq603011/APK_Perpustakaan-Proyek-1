import tkinter as tk
from tkinter import messagebox
from views.components import UIComponents, PURPLE_COLOR

class LoginView:
    """View for login and registration screens"""
    
    def __init__(self, parent, auth_controller, on_login_success=None):
        """Initialize login view"""
        self.parent = parent
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        
        # Main frame
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(expand=True, fill="both")
        
        # Frames for login and signup
        self.login_frame = tk.Frame(self.main_frame)
        self.signup_frame = tk.Frame(self.main_frame)
        
        # Set up the views
        self._setup_login_view()
        self._setup_signup_view()
        
        # Show login by default
        self.show_login()
    
    def _setup_login_view(self):
        """Set up the login view"""
        # Title frame
        title_frame = tk.Frame(self.login_frame, bg=PURPLE_COLOR)
        title_frame.pack(pady=20)
        
        # Title
        title_label = tk.Label(
            title_frame, 
            text="📖 BOOK-KU!", 
            font=("Arial Black", 48, "bold"), 
            fg="black", 
            bg=PURPLE_COLOR
        )
        title_label.pack()
        
        # Login form frame
        login_form_frame = tk.Frame(self.login_frame, bg=PURPLE_COLOR, padx=20, pady=20)
        login_form_frame.pack(expand=True)
        
        # Entry fields
        self.username_entry = UIComponents.create_entry_field(login_form_frame, "your @gmail.com")
        self.username_entry.pack(fill="x", padx=10, pady=10, ipady=10)
        
        self.password_entry = UIComponents.create_entry_field(login_form_frame, "password", show="*")
        self.password_entry.pack(fill="x", padx=10, pady=10, ipady=10)
        
        # Login button
        login_button = UIComponents.create_button(
            self.login_frame,
            "LOGIN",
            command=self._on_login,
            width=10,
            height=1,
            font=("Arial", 16, "bold")
        )
        login_button.pack(pady=20)
        
        # Register link
        signup_link = UIComponents.create_button(
            self.login_frame,
            "Belum punya akun? Daftar",
            command=self.show_signup,
            width=20,
            height=1
        )
        signup_link.pack()
        
        # Exit button
        exit_button = UIComponents.create_button(
            self.login_frame,
            "Keluar",
            command=self.parent.destroy,
            width=10,
            height=1
        )
        exit_button.pack(pady=10)
    
    def _setup_signup_view(self):
        """Set up the signup view"""
        # Title frame
        title_frame = tk.Frame(self.signup_frame, bg=PURPLE_COLOR)
        title_frame.pack(pady=20)
        
        # Title
        title_label = tk.Label(
            title_frame, 
            text="📖 BOOK-KU!", 
            font=("Arial Black", 48, "bold"), 
            fg="black", 
            bg=PURPLE_COLOR
        )
        title_label.pack()
        
        # Signup form frame
        signup_form_frame = tk.Frame(self.signup_frame, bg=PURPLE_COLOR, padx=20, pady=20)
        signup_form_frame.pack(expand=True)
        
        # Entry fields
        self.name_entry = UIComponents.create_entry_field(signup_form_frame, "your name")
        self.name_entry.pack(fill="x", padx=20, pady=10, ipady=10)
        
        self.reg_username_entry = UIComponents.create_entry_field(signup_form_frame, "your @gmail.com")
        self.reg_username_entry.pack(fill="x", padx=20, pady=10, ipady=10)
        
        self.reg_password_entry = UIComponents.create_entry_field(signup_form_frame, "password", show="*")
        self.reg_password_entry.pack(fill="x", padx=20, pady=10, ipady=10)
        
        self.confirm_password_entry = UIComponents.create_entry_field(signup_form_frame, "confirm password", show="*")
        self.confirm_password_entry.pack(fill="x", padx=20, pady=10, ipady=10)
        
        # Signup button
        signup_button = UIComponents.create_button(
            self.signup_frame,
            "SIGN UP",
            command=self._on_signup,
            width=10,
            height=1,
            font=("Arial", 16, "bold")
        )
        signup_button.pack(pady=20)
        
        # Login link
        login_link = UIComponents.create_button(
            self.signup_frame,
            "Sudah punya akun? Login",
            command=self.show_login,
            width=20,
            height=1
        )
        login_link.pack()
        
        # Exit button
        exit_button = UIComponents.create_button(
            self.signup_frame,
            "Keluar",
            command=self.parent.destroy,
            width=10,
            height=1
        )
        exit_button.pack(pady=10)
    
    def show_login(self):
        """Show login frame"""
        self.signup_frame.pack_forget()
        self.login_frame.pack(expand=True, fill="both")
    
    def show_signup(self):
        """Show signup frame"""
        self.login_frame.pack_forget()
        self.signup_frame.pack(expand=True, fill="both")
    
    def _on_login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check if using placeholder
        if self.username_entry.placeholder_active or self.password_entry.placeholder_active:
            messagebox.showerror("Error", "Please enter your username and password")
            return
        
        # Authenticate
        success, message, user_data = self.auth_controller.login(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            if self.on_login_success:
                self.on_login_success(user_data)
        else:
            messagebox.showerror("Error", message)
    
    def _on_signup(self):
        """Handle signup button click"""
        name = self.name_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Check if using placeholder
        if (self.name_entry.placeholder_active or 
            self.reg_username_entry.placeholder_active or 
            self.reg_password_entry.placeholder_active or
            self.confirm_password_entry.placeholder_active):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        # Register
        success, message = self.auth_controller.register(name, username, password, confirm_password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_login()
        else:
            messagebox.showerror("Error", message)
    
    def destroy(self):
        """Destroy the view"""
        self.main_frame.destroy()