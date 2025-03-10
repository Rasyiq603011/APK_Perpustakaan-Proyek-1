"""
Authentication Module for Book Manager
"""

import json
import os
import hashlib
from tkinter import messagebox

# File untuk menyimpan kredensial admin (dalam praktik nyata gunakan metode yang lebih aman)
AUTH_FILE = "admin_auth.json"

# Admin default jika file belum ada
DEFAULT_ADMIN = {
    "username": "admin",
    "password_hash": hashlib.sha256("admin123".encode()).hexdigest()
}

class AuthManager:
    """
    Class untuk mengelola autentikasi dan status login
    """
    def __init__(self):
        self.current_user = None
        self.is_admin = False
        self._ensure_auth_file()
    
    def _ensure_auth_file(self):
        """Membuat file autentikasi jika belum ada"""
        if not os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'w') as f:
                json.dump(DEFAULT_ADMIN, f)
    
    def login(self, username, password):
        """
        Mencoba login dengan username dan password
        
        Returns:
            tuple: (success, is_admin)
        """
        # Reset status login
        self.current_user = None
        self.is_admin = False
        
        # Jika login sebagai user biasa (tidak perlu autentikasi)
        if username.lower() == "user":
            self.current_user = "user"
            self.is_admin = False
            return True, False
            
        # Jika login sebagai admin
        try:
            with open(AUTH_FILE, 'r') as f:
                admin_data = json.load(f)
                
            # Hash password yang dimasukkan
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Periksa kredensial
            if (username == admin_data["username"] and 
                password_hash == admin_data["password_hash"]):
                self.current_user = username
                self.is_admin = True
                return True, True
            else:
                return False, False
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False, False
    
    def is_authenticated(self):
        """Mengembalikan True jika user sudah login"""
        return self.current_user is not None
    
    def is_admin_user(self):
        """Mengembalikan True jika user adalah admin"""
        return self.is_admin
    
    def logout(self):
        """Logout user saat ini"""
        self.current_user = None
        self.is_admin = False
    
    def change_admin_password(self, current_password, new_password):
        """Mengubah password admin"""
        if not self.is_admin:
            return False, "Hanya admin yang dapat mengubah password"
            
        try:
            with open(AUTH_FILE, 'r') as f:
                admin_data = json.load(f)
            
            # Verifikasi password lama
            current_hash = hashlib.sha256(current_password.encode()).hexdigest()
            if current_hash != admin_data["password_hash"]:
                return False, "Password lama tidak sesuai"
            
            # Update dengan password baru
            admin_data["password_hash"] = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Simpan perubahan
            with open(AUTH_FILE, 'w') as f:
                json.dump(admin_data, f)
                
            return True, "Password berhasil diubah"
            
        except Exception as e:
            return False, f"Error: {str(e)}"