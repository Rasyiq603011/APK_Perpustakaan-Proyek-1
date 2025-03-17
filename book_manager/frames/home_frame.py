import tkinter as tk
from tkinter import ttk, messagebox
from book_manager.constants import COLORS, FONTS, BUTTON_SIZES, APP_COPYRIGHT

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=100)
        header_frame.pack(fill="x", pady=10)
        
        # Header dengan informasi login
        self.header_label = tk.Label(
            header_frame, 
            text="SISTEM MANAJEMEN BUKU", 
            font=FONTS["header"],
            bg=COLORS["primary"],
            fg="white"
        )
        self.header_label.pack(pady=15)
        
        # Label untuk menampilkan status login
        self.user_label = tk.Label(
            header_frame,
            text="",
            font=FONTS["normal"],
            bg=COLORS["primary"],
            fg="white"
        )
        self.user_label.pack(pady=5)
        
        # Main content
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Menu buttons with icons
        button_width = BUTTON_SIZES["large"]["width"]
        button_height = BUTTON_SIZES["large"]["height"]
        button_font = FONTS["button"]
        
        # Lihat Buku Button
        self.view_button = tk.Button(
            main_frame,
            text="📚 Lihat Data Buku",
            font=button_font,
            width=button_width,
            height=button_height,
            bg=COLORS["secondary"],
            fg="white",
            command=lambda: controller.show_frame("ViewBooksFrame")
        )
        
        self.view_button.pack(pady=10)
        
        # Tambah Buku Button - Admin Only
        self.add_button = tk.Button(
            main_frame,
            text="➕ Tambah Buku Baru",
            font=button_font,
            width=button_width,
            height=button_height,
            bg=COLORS["primary"],
            fg="white",
            command=lambda: controller.show_frame("AddBookFrame"),
            state=tk.DISABLED  # Disabled by default
        )
        self.add_button.pack(pady=10)
        
        # Update Buku Button - Admin Only
        self.update_button = tk.Button(
            main_frame,
            text="🔄 Update Data Buku",
            font=button_font,
            width=button_width,
            height=button_height,
            bg=COLORS["accent"],
            fg="white",
            command=lambda: controller.show_frame("UpdateBookFrame"),
            state=tk.DISABLED  # Disabled by default
        )
        self.update_button.pack(pady=10)
        
        # Logout Button
        self.logout_button = tk.Button(
            main_frame,
            text="🚪 Logout",
            font=button_font,
            width=button_width,
            height=2,
            bg=COLORS["dark"],
            fg="white",
            command=self.logout
        )
        self.logout_button.pack(pady=20)
        
        # Footer
        footer_frame = tk.Frame(self, bg=COLORS["dark"], height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        tk.Label(
            footer_frame,
            text=APP_COPYRIGHT,
            font=FONTS["normal"],
            bg=COLORS["dark"],
            fg="white"
        ).pack(pady=15)
    
    def on_show_frame(self):
        """Update tampilan saat frame ditampilkan"""
        self.update_ui_for_role()
    
    def update_ui_for_role(self):
        """Update tampilan UI berdasarkan peran pengguna"""
        if self.controller.auth_manager.is_authenticated():
            if self.controller.auth_manager.is_admin_user():
                # Admin mode
                self.user_label.config(text="Mode: Administrator")
                self.add_button.config(state=tk.NORMAL)
                self.update_button.config(state=tk.NORMAL)
            else:
                # User mode
                self.user_label.config(text="Mode: User (Hanya Lihat)")
                self.add_button.config(state=tk.DISABLED)
                self.update_button.config(state=tk.DISABLED)
        else:
            # Not logged in
            self.controller.show_frame("LoginFrame")
    
    def logout(self):
        """Fungsi untuk logout"""
        if messagebox.askyesno("Konfirmasi Logout", "Anda yakin ingin logout?"):
            self.controller.auth_manager.logout()
            self.controller.show_frame("LoginFrame")