import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
import json
from datetime import datetime
from PIL import Image, ImageTk
from logic.Login import AuthManager

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.auth_manager = AuthManager()
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        # Make the frame fill the entire container
        self.pack_propagate(False)
        
        # Load assets
        self.logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
        self.bg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "library_bg.jpg")
        
        # Create directory for user data if it doesn't exist
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.logs_file = os.path.join(self.data_dir, "logs.json")
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize users file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({
                    "admin@bookku.com": {
                        "name": "Administrator",
                        "password": "admin123",
                        "role": "admin"
                    }
                }, f, indent=4)
        
        # Initialize logs file if it doesn't exist
        if not os.path.exists(self.logs_file):
            with open(self.logs_file, 'w') as f:
                json.dump([], f, indent=4)
        
        # Create left panel for logo and background
        self.left_panel = ctk.CTkFrame(self, fg_color="#121212", corner_radius=0)
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # Create right panel for login form
        self.right_panel = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Configure panels to be equal width
        self.left_panel.configure(width=512)
        self.right_panel.configure(width=512)
        
        # Setup left panel with background image and logo
        self.setup_left_panel()
        
        # Setup right panel with login form
        self.setup_login_panel()
    
    def setup_left_panel(self):
        try:
            # Background image
            if os.path.exists(self.bg_path):
                bg_image = Image.open(self.bg_path)
                bg_image = bg_image.resize((512, 768))
                self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(512, 768))
                
                bg_label = ctk.CTkLabel(self.left_panel, image=self.bg_photo, text="")
                bg_label.place(relwidth=1, relheight=1)
            
            # Semi-transparent overlay
            overlay = ctk.CTkFrame(self.left_panel, fg_color="#000000", corner_radius=0)
            overlay.place(relwidth=1, relheight=1)
            
            # App name and tagline
            app_name = ctk.CTkLabel(
                overlay,
                text="BOOK-KU",
                font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
                text_color="#FFFFFF"
            )
            app_name.place(relx=0.5, rely=0.4, anchor="center")
            
            tagline = ctk.CTkLabel(
                overlay,
                text="Your Digital Library Experience",
                font=ctk.CTkFont(family="Arial", size=18),
                text_color="#FFFFFF"
            )
            tagline.place(relx=0.5, rely=0.46, anchor="center")
        
        except Exception as e:
            print(f"Error setting up left panel: {e}")
            # Fallback if image loading fails
            ctk.CTkLabel(
                self.left_panel,
                text="BOOK-KU\nYour Digital Library",
                font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.5, anchor="center")
    
    def setup_login_panel(self):
        # Login container
        login_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        login_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            login_container,
            text="Welcome Back!",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#FFFFFF"
        )
        welcome_label.pack(pady=(0, 20))
        
        # Login instruction
        instruction_label = ctk.CTkLabel(
            login_container,
            text="Please login to your account",
            font=ctk.CTkFont(family="Arial", size=16),
            text_color="#AAAAAA"
        )
        instruction_label.pack(pady=(0, 40))
        
        # Email entry
        email_frame = ctk.CTkFrame(login_container, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 15))
        
        email_label = ctk.CTkLabel(
            email_frame, 
            text="Email",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#FFFFFF",
            anchor="w"
        )
        email_label.pack(anchor="w", padx=5, pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Enter your email",
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#2B2B2B",
            border_color="#666666",
            text_color="#FFFFFF",
            corner_radius=8,
            height=40
        )
        self.email_entry.pack(fill="x")
        
        # Password entry
        password_frame = ctk.CTkFrame(login_container, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 20))
        
        password_label = ctk.CTkLabel(
            password_frame, 
            text="Password",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#FFFFFF",
            anchor="w"
        )
        password_label.pack(anchor="w", padx=5, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter your password",
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#2B2B2B",
            border_color="#666666",
            text_color="#FFFFFF",
            corner_radius=8,
            height=40,
            show="●"
        )
        self.password_entry.pack(fill="x")
        
        # Login button
        self.login_btn = ctk.CTkButton(
            login_container,
            text="LOGIN",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            fg_color="#4d6980",
            hover_color="#3c5b74",
            text_color="#FFFFFF",
            corner_radius=8,
            height=45,
            command=self.login
        )
        self.login_btn.pack(fill="x", pady=(20, 10))
        
        # Register link
        register_frame = ctk.CTkFrame(login_container, fg_color="transparent")
        register_frame.pack(pady=(10, 0))
        
        register_label = ctk.CTkLabel(
            register_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#AAAAAA"
        )
        register_label.pack(side="left", padx=(0, 5))
        
        register_btn = ctk.CTkButton(
            register_frame,
            text="Register now",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            fg_color="transparent",
            hover_color="#333333",
            text_color="#3c5b74",
            corner_radius=0,
            command=self.show_register_form
        )
        register_btn.pack(side="left")
        
        # Initialize login panel as active
        self.current_panel = "login"
    
    def show_register_form(self):
        if self.current_panel != "register":
            # Clear the right panel
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            
            # Register container
            register_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
            register_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
            
            # Register header
            register_label = ctk.CTkLabel(
                register_container,
                text="Create Account",
                font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
                text_color="#FFFFFF"
            )
            register_label.pack(pady=(0, 20))
            
            # Register instruction
            instruction_label = ctk.CTkLabel(
                register_container,
                text="Please fill in the form to create your account",
                font=ctk.CTkFont(family="Arial", size=16),
                text_color="#AAAAAA"
            )
            instruction_label.pack(pady=(0, 30))
            
            # Name entry
            name_frame = ctk.CTkFrame(register_container, fg_color="transparent")
            name_frame.pack(fill="x", pady=(0, 15))
            
            name_label = ctk.CTkLabel(
                name_frame, 
                text="Name",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#FFFFFF",
                anchor="w"
            )
            name_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            self.reg_name_entry = ctk.CTkEntry(
                name_frame,
                placeholder_text="Enter your full name",
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#2B2B2B",
                border_color="#666666",
                text_color="#FFFFFF",
                corner_radius=8,
                height=40
            )
            self.reg_name_entry.pack(fill="x")
            
            # Email entry
            email_frame = ctk.CTkFrame(register_container, fg_color="transparent")
            email_frame.pack(fill="x", pady=(0, 15))
            
            email_label = ctk.CTkLabel(
                email_frame, 
                text="Email",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#FFFFFF",
                anchor="w"
            )
            email_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            self.reg_email_entry = ctk.CTkEntry(
                email_frame,
                placeholder_text="Enter your email",
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#2B2B2B",
                border_color="#666666",
                text_color="#FFFFFF",
                corner_radius=8,
                height=40
            )
            self.reg_email_entry.pack(fill="x")
            
            # Password entry
            password_frame = ctk.CTkFrame(register_container, fg_color="transparent")
            password_frame.pack(fill="x", pady=(0, 15))
            
            password_label = ctk.CTkLabel(
                password_frame, 
                text="Password",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#FFFFFF",
                anchor="w"
            )
            password_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            self.reg_password_entry = ctk.CTkEntry(
                password_frame,
                placeholder_text="Create a password",
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#2B2B2B",
                border_color="#666666",
                text_color="#FFFFFF",
                corner_radius=8,
                height=40,
                show="●"
            )
            self.reg_password_entry.pack(fill="x")
            
            # Confirm Password entry
            confirm_password_frame = ctk.CTkFrame(register_container, fg_color="transparent")
            confirm_password_frame.pack(fill="x", pady=(0, 20))
            
            confirm_password_label = ctk.CTkLabel(
                confirm_password_frame, 
                text="Confirm Password",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#FFFFFF",
                anchor="w"
            )
            confirm_password_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            self.reg_confirm_password_entry = ctk.CTkEntry(
                confirm_password_frame,
                placeholder_text="Confirm your password",
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#2B2B2B",
                border_color="#666666",
                text_color="#FFFFFF",
                corner_radius=8,
                height=40,
                show="●"
            )
            self.reg_confirm_password_entry.pack(fill="x")
            
            # Button container for register and back buttons
            button_container = ctk.CTkFrame(register_container, fg_color="transparent")
            button_container.pack(fill="x", pady=(10, 0))
            
            # Back to login button
            back_btn = ctk.CTkButton(
                button_container,
                text="Back to Login",
                font=ctk.CTkFont(family="Arial", size=16),
                fg_color="#333333",
                hover_color="#444444",
                text_color="#FFFFFF",
                corner_radius=8,
                height=45,
                command=self.setup_login_panel
            )
            back_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Register button
            register_btn = ctk.CTkButton(
                button_container,
                text="REGISTER",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                fg_color="#4d6980",
                hover_color="#3c5b74",
                text_color="#FFFFFF",
                corner_radius=8,
                height=45,
                command=self.register
            )
            register_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
            
            self.current_panel = "register"
    
    def register(self):
        """Handle user registration"""
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        
        # Basic validation
        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Registration Error", "Please fill all fields")
            return
        
        # Password validation
        if len(password) < 8:
            messagebox.showerror("Registration Error", "Password must be at least 8 characters long")
            return
        
        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match")
            return
        
        # Register user using AuthManager
        success, message = self.auth_manager.register(name, email, password)
        
        if success:
            messagebox.showinfo("Registration Successful", message)
            self.setup_login_panel()
        else:
            messagebox.showerror("Registration Error", message)
    
    def login(self):
        """Handle user login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Login using AuthManager
        success, message, user_info = self.auth_manager.login(email, password)
        
        if success:
            # Store user info in controller
            self.controller.current_user = user_info
            
            # Show home page based on role
            messagebox.showinfo("Login Successful", f"Welcome back, {user_info['name']}!")
            self.controller.showFrame("HomeFrame")
        else:
            messagebox.showerror("Login Error", message)


# For testing purposes
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("Login Test")
    
    class MockController:
        def showFrame(self, frame_name):
            print(f"Showing frame: {frame_name}")
        
        def current_user(self):
            return None
    
    frame = LoginFrame(root, MockController())
    frame.pack(fill="both", expand=True)
    
    root.mainloop()