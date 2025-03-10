"""
Login Frame for Book Manager Application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from book_manager.constants import COLORS, FONTS

class LoginFrame(tk.Frame):
    """Frame untuk login ke aplikasi"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=100)
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame, 
            text="SISTEM MANAJEMEN BUKU", 
            font=FONTS["header"],
            bg=COLORS["primary"],
            fg="white"
        ).pack(pady=25)
        
        # Main content
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # User selection frame
        user_frame = ttk.LabelFrame(main_frame, text="Pilih Mode Akses")
        user_frame.pack(fill="x", pady=20, padx=50)
        
        # User button
        user_button = tk.Button(
            user_frame,
            text="Masuk sebagai User",
            font=FONTS["button"],
            width=20,
            height=2,
            bg=COLORS["secondary"],
            fg="white",
            command=self.login_as_user
        )
        user_button.pack(pady=10, padx=20, fill="x")
        
        # Administrator frame
        admin_frame = ttk.LabelFrame(main_frame, text="Login Administrator")
        admin_frame.pack(fill="x", pady=20, padx=50)
        
        # Login form
        form_frame = ttk.Frame(admin_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.password_var, width=30, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        # Login button
        login_button = tk.Button(
            admin_frame,
            text="Login sebagai Admin",
            font=FONTS["button"],
            bg=COLORS["accent"],
            fg="white",
            command=self.login_as_admin
        )
        login_button.pack(pady=10, padx=20, fill="x")
        
        # Footer
        footer_frame = tk.Frame(self, bg=COLORS["dark"], height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        tk.Label(
            footer_frame,
            text="© 2025 Sistem Manajemen Perpustakaan",
            font=FONTS["normal"],
            bg=COLORS["dark"],
            fg="white"
        ).pack(pady=15)
    
    def login_as_user(self):
        """Login sebagai pengguna biasa (tanpa hak edit)"""
        success, is_admin = self.controller.auth_manager.login("user", "")
        if success:
            self.controller.show_frame("HomeFrame")
            self.controller.update_ui_for_role()
            messagebox.showinfo("Login Berhasil", "Anda masuk sebagai User")
    
    def login_as_admin(self):
        """Login sebagai administrator"""
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password harus diisi!")
            return
            
        success, is_admin = self.controller.auth_manager.login(username, password)
        
        if success:
            self.controller.show_frame("HomeFrame")
            self.controller.update_ui_for_role()
            messagebox.showinfo("Login Berhasil", "Anda masuk sebagai Administrator")
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")
    
    def on_show_frame(self):
        """Reset form saat frame ditampilkan"""
        self.username_var.set("")
        self.password_var.set("")