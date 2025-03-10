import tkinter as tk
from tkinter import ttk

class HomeFrame(tk.Frame):
    """Frame utama dengan menu navigasi"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header_frame = tk.Frame(self, bg="#3498db", height=100)
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame, 
            text="SISTEM MANAJEMEN BUKU", 
            font=("Arial", 24, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=25)
        
        # Main content
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Menu buttons with icons (using text as placeholders for icons)
        button_width = 25
        button_height = 3
        button_font = ("Arial", 12)
        
        # Lihat Buku Button
        view_button = tk.Button(
            main_frame,
            text="📚 Lihat Data Buku",
            font=button_font,
            width=button_width,
            height=button_height,
            bg="#2ecc71",
            fg="white",
            command=lambda: controller.show_frame("ViewBooksFrame")
        )
        view_button.pack(pady=10)
        
        # Tambah Buku Button
        add_button = tk.Button(
            main_frame,
            text="➕ Tambah Buku Baru",
            font=button_font,
            width=button_width,
            height=button_height,
            bg="#3498db",
            fg="white",
            command=lambda: controller.show_frame("AddBookFrame")
        )
        add_button.pack(pady=10)
        
        # Update Buku Button
        update_button = tk.Button(
            main_frame,
            text="🔄 Update Data Buku",
            font=button_font,
            width=button_width,
            height=button_height,
            bg="#f39c12",
            fg="white",
            command=lambda: controller.show_frame("UpdateBookFrame")
        )
        update_button.pack(pady=10)
        
        # Footer
        footer_frame = tk.Frame(self, bg="#34495e", height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        tk.Label(
            footer_frame,
            text="© 2025 Sistem Manajemen Perpustakaan",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        ).pack(pady=15)

if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Sistem Manajemen Buku")
    root.geometry("1000x800")

    app = HomeFrame(root, None)
    app.pack(fill="both", expand=True)

    root.mainloop()