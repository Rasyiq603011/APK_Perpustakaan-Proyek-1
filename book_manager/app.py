import tkinter as tk
from book_manager.constants import APP_TITLE, APP_SIZE
from book_manager.utils import buat_file
from book_manager.auth import AuthManager

# Import semua frame
from book_manager.frames import HomeFrame, ViewBooksFrame, AddBookFrame, UpdateBookFrame, HomeFramePage
# Import LoginFrame secara terpisah karena belum ditambahkan ke frames/__init__.py
from book_manager.frames.login_frame import LoginFrame

class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(True, True)
        
        # Ensure the file exists
        buat_file()
        
        # Create auth manager
        self.auth_manager = AuthManager()
        
        # Container untuk semua frame
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary untuk menyimpan semua frame
        self.frames = {}
        
        # Buat dan inisialisasi frame-frame
        self.create_frames()
        
        # Tampilkan login frame pertama kali
        self.show_frame("LoginFrame")
    
    def create_frames(self):

        # Daftar semua kelas frame yang akan digunakan
        frame_classes = (LoginFrame, HomeFrame, ViewBooksFrame, AddBookFrame, UpdateBookFrame, HomeFramePage)
        
        # Inisialisasi setiap frame
        for F in frame_classes:
            frame_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """Menampilkan frame tertentu ke depan"""
        # Jika mencoba akses frame yang butuh autentikasi
        if frame_name != "LoginFrame" and not self.auth_manager.is_authenticated():
            frame_name = "LoginFrame"
            
        # Jika mencoba akses frame yang butuh admin tetapi bukan admin
        admin_only_frames = ["AddBookFrame", "UpdateBookFrame"]
        if frame_name in admin_only_frames and not self.auth_manager.is_admin_user():
            frame_name = "HomeFrame"
            
        frame = self.frames[frame_name]
        frame.tkraise()
        
        # Perbarui data jika perlu
        if hasattr(frame, "on_show_frame"):
            frame.on_show_frame()
    
    def refresh_all_frames(self):
        """Memperbarui data di semua frame"""
        for frame_name, frame in self.frames.items():
            if hasattr(frame, "refresh_data"):
                frame.refresh_data()
    
    def update_ui_for_role(self):
        """Update UI components based on current role"""
        for frame_name, frame in self.frames.items():
            if hasattr(frame, "update_ui_for_role"):
                frame.update_ui_for_role()