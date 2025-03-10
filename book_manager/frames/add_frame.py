import tkinter as tk
from tkinter import ttk, messagebox
from book_manager.constants import FONTS
from book_manager.utils import add_book

class AddBookFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        tk.Label(
            self, 
            text="Tambah Buku Baru", 
            font=FONTS["subheader"]
        ).pack(pady=10)
        
        # Back button (top left)
        back_button = tk.Button(
            self,
            text="← Kembali",
            command=lambda: controller.show_frame("HomeFrame")
        )
        back_button.place(x=10, y=10)
        
        # Main form
        form_frame = ttk.LabelFrame(self, text="Data Buku Baru")
        form_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Form fields
        # Using grid for better alignment
        padx = 10
        pady = 10
        
        # Judul
        ttk.Label(form_frame, text="Judul Buku:").grid(row=0, column=0, sticky="w", padx=padx, pady=pady)
        self.judul_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.judul_var, width=50).grid(row=0, column=1, padx=padx, pady=pady)
        
        # Penulis
        ttk.Label(form_frame, text="Penulis:").grid(row=1, column=0, sticky="w", padx=padx, pady=pady)
        self.penulis_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.penulis_var, width=50).grid(row=1, column=1, padx=padx, pady=pady)
        
        # Tahun
        ttk.Label(form_frame, text="Tahun Terbit:").grid(row=2, column=0, sticky="w", padx=padx, pady=pady)
        self.tahun_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.tahun_var, width=50).grid(row=2, column=1, padx=padx, pady=pady)

        # Penerbit
        ttk.Label(form_frame, text="Penerbit:").grid(row=3, column=0, sticky="w", padx=padx, pady=pady)
        self.penerbit_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.penerbit_var, width=50).grid(row=3, column=1, padx=padx, pady=pady)

        # Genre
        ttk.Label(form_frame, text="Genre:").grid(row=4, column=0, sticky="w", padx=padx, pady=pady)
        self.genre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.genre_var, width=50).grid(row=4, column=1, padx=padx, pady=pady)

        # ISBN
        ttk.Label(form_frame, text="ISBN:").grid(row=5, column=0, sticky="w", padx=padx, pady=pady)
        self.isbn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.isbn_var, width=50).grid(row=5, column=1, padx=padx, pady=pady)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Save button
        save_button = ttk.Button(
            button_frame,
            text="Simpan Data",
            command=self.tambah_buku
        )
        save_button.pack(side="left", padx=5)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="Bersihkan Form",
            command=self.clear_form
        )
        clear_button.pack(side="left", padx=5)
    
    def on_show_frame(self):
        """Dipanggil saat frame ini ditampilkan"""
        # Bersihkan form saat frame ditampilkan
        self.clear_form()
    
    def clear_form(self):
        """Bersihkan semua field"""
        self.judul_var.set("")
        self.penulis_var.set("")
        self.tahun_var.set("")
        self.tahun_var.set("")
        self.penerbit_var.set("")
        self.genre_var.set("")
        self.isbn_var.set("")
    
    def tambah_buku(self):
        """Fungsi untuk menambah buku baru"""
        judul = self.judul_var.get().strip()
        penulis = self.penulis_var.get().strip()
        tahun = self.tahun_var.get().strip()
        penerbit = self.penerbit_var.get().strip()
        genre = self.genre_var.get().strip()
        isbn = self.isbn_var.get().strip()

        
        # Validation
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
            
        # Add book
        success = add_book(judul, penulis, tahun, penerbit, genre, isbn)    
        
        if success:
            # Clear form
            self.clear_form()
            
            # Refresh all frames
            self.controller.refresh_all_frames()
            
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
            
            # Option to add another or go back to home
            if messagebox.askyesno("Tambah Lagi?", "Ingin menambahkan buku lain?"):
                # Stay on this form
                pass
            else:
                # Go back to home
                self.controller.show_frame("HomeFrame")
        else:
            messagebox.showerror("Error", "Gagal menambah data buku!")