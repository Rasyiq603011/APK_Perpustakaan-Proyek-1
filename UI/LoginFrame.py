import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import json
from datetime import datetime
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Moduls.Login import AuthManager

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.auth_manager = AuthManager()
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        # Make the frame fill the entire container
        self.pack_propagate(False)
        
        # Inisialisasi paths dan setup UI
        self._initialize_paths()
        self._setup_ui()
    
    def _initialize_paths(self):
        """Inisialisasi semua path yang dibutuhkan"""
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        self.logo_path = os.path.join(assets_dir, "logo.png")
        self.bg_path = os.path.join(assets_dir, "library_bg.jpg")
        
        # Get paths from AuthManager
        self.data_dir = self.auth_manager.data_dir
        self.users_file = self.auth_manager.users_file
        self.logs_file = self.auth_manager.logs_file
    
    def _setup_ui(self):
        """Setup utama UI"""
        # Buat dan konfigurasi panels
        self.left_panel = self._create_panel("left", "#121212")
        self.right_panel = self._create_panel("right", "#1E1E1E")
        
        # Setup panels
        self._setup_left_panel()
        self.setup_login_panel()
    
    def _create_panel(self, side, color):
        """Helper untuk membuat panel dengan konfigurasi standar"""
        panel = ctk.CTkFrame(self, fg_color=color, corner_radius=0)
        panel.pack(side=side, fill="both", expand=True)
        panel.configure(width=512)
        return panel
    
    def _create_entry_field(self, container, label_text, placeholder, show=None):
        """Helper untuk membuat field input yang konsisten"""
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            frame, 
            text=label_text,
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#FFFFFF",
            anchor="w"
        ).pack(anchor="w", padx=5, pady=(0, 5))
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#2B2B2B",
            border_color="#666666",
            text_color="#FFFFFF",
            corner_radius=8,
            height=40,
            show=show
        )
        entry.pack(fill="x")
        return entry
    
    def _create_button(self, parent, text, command, is_primary=True, **kwargs):
        """Helper untuk membuat tombol dengan style yang konsisten"""
        styles = {
            "primary": {
                "fg_color": "#4d6980",
                "hover_color": "#3c5b74",
                "weight": "bold"
            },
            "secondary": {
                "fg_color": "#333333",
                "hover_color": "#444444",
                "weight": "normal"
            }
        }
        
        style = styles["primary"] if is_primary else styles["secondary"]
        
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ctk.CTkFont(family="Arial", size=16, weight=style["weight"]),
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            text_color="#FFFFFF",
            corner_radius=8,
            height=45,
            **kwargs
        )
    
    def _setup_left_panel(self):
        """Setup panel kiri dengan background dan branding"""
        try:
            if os.path.exists(self.bg_path):
                # Setup background image
                bg_image = Image.open(self.bg_path)
                bg_image = bg_image.resize((512, 768))
                self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(512, 768))
                ctk.CTkLabel(self.left_panel, image=self.bg_photo, text="").place(relwidth=1, relheight=1)
            
            # Overlay dan branding
            overlay = ctk.CTkFrame(self.left_panel, fg_color="#000000", corner_radius=0)
            overlay.place(relwidth=1, relheight=1)
            self._create_branding(overlay)
            
        except Exception as e:
            print(f"Error setting up left panel: {e}")
            self._create_fallback_branding()
    
    def _create_branding(self, parent):
        """Membuat elemen branding"""
        ctk.CTkLabel(
            parent,
            text="BOOK-KU",
            font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.4, anchor="center")
        
        ctk.CTkLabel(
            parent,
            text="Your Digital Library Experience",
            font=ctk.CTkFont(family="Arial", size=18),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.46, anchor="center")
    
    def _create_fallback_branding(self):
        """Membuat branding fallback jika gambar gagal dimuat"""
        ctk.CTkLabel(
            self.left_panel,
            text="BOOK-KU\nYour Digital Library",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")
    
    def _create_form_header(self, container, title, subtitle):
        """Membuat header form yang konsisten"""
        ctk.CTkLabel(
            container,
            text=title,
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            container,
            text=subtitle,
            font=ctk.CTkFont(family="Arial", size=16),
            text_color="#AAAAAA"
        ).pack(pady=(0, 40))
    
    def setup_login_panel(self):
        """Setup panel login"""
        # Clear existing content
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create container
        container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
        
        # Header
        self._create_form_header(container, "Welcome Back!", "Please login to your account")
        
        # Form fields
        self.email_entry = self._create_entry_field(container, "Email", "Enter your email")
        self.password_entry = self._create_entry_field(container, "Password", "Enter your password", show="●")
        
        # Login button
        self._create_button(container, "LOGIN", self.login).pack(fill="x", pady=(20, 10))
        
        # Register link
        self._create_register_link(container)
        
        self.current_panel = "login"
    
    def _create_register_link(self, container):
        """Membuat link registrasi"""
        register_frame = ctk.CTkFrame(container, fg_color="transparent")
        register_frame.pack(pady=(10, 0))
        
        ctk.CTkLabel(
            register_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#AAAAAA"
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            register_frame,
            text="Register now",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            fg_color="transparent",
            hover_color="#333333",
            text_color="#3c5b74",
            corner_radius=0,
            command=self.show_register_form
        ).pack(side="left")
    
    def show_register_form(self):
        """Menampilkan form registrasi"""
        if self.current_panel == "register":
            return
        
        # Clear existing content
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create container
        container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        # Header
        self._create_form_header(container, "Create Account", "Please fill in the form to create your account")
        
        # Form fields
        self.reg_name_entry = self._create_entry_field(container, "Name", "Enter your full name")
        self.reg_email_entry = self._create_entry_field(container, "Email", "Enter your email")
        self.reg_password_entry = self._create_entry_field(container, "Password", "Create a password", show="●")
        self.reg_confirm_password_entry = self._create_entry_field(container, "Confirm Password", "Confirm your password", show="●")
        
        # Button container
        button_container = ctk.CTkFrame(container, fg_color="transparent")
        button_container.pack(fill="x", pady=(10, 0))
        
        # Back and Register buttons
        self._create_button(
            button_container,
            "Back to Login",
            self.setup_login_panel,
            is_primary=False
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self._create_button(
            button_container,
            "REGISTER",
            self.register
        ).pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        self.current_panel = "register"
    
    def register(self):
        """Handle registrasi pengguna"""
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        
        # Validasi konfirmasi password di UI
        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match")
            return
        
        # Delegasikan ke AuthManager untuk validasi lainnya dan proses registrasi
        success, message = self.auth_manager.register(name, email, password)
        
        if success:
            messagebox.showinfo("Registration Successful", message)
            self.setup_login_panel()
        else:
            messagebox.showerror("Registration Error", message)
    
    def login(self):
        """Handle login pengguna"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        success, message, user_info = self.auth_manager.login(email, password)
        
        if success:
            self.controller.current_user = user_info
            # Show home page based on role
            messagebox.showinfo("Login Successful", f"Welcome back, {user_info['name']}!")
            self.setup_login_panel()
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
