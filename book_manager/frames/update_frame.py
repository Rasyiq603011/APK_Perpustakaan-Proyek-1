"""
Update Book Frame for Book Manager Application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from book_manager.constants import FONTS
from book_manager.utils import update_book

class UpdateBookFrame(tk.Frame):
    """Frame untuk mengupdate buku"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        tk.Label(
            self, 
            text="Update Data Buku", 
            font=FONTS["subheader"]
        ).pack(pady=10)
        
        # Back button (top left)
        back_button = tk.Button(
            self,
            text="← Kembali",
            command=lambda: controller.show_frame("ViewBooksFrame")
        )
        back_button.place(x=10, y=10)
        
        # Main form
        form_frame = ttk.LabelFrame(self, text="Edit Data Buku")
        form_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Form fields
        # Using grid for better alignment
        padx = 10
        pady = 10
        
        # ID (hidden/readonly)
        ttk.Label(form_frame, text="ID Buku:").grid(row=0, column=0, sticky="w", padx=padx, pady=pady)
        self.id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.id_var, width=50, state="readonly").grid(row=0, column=1, padx=padx, pady=pady)
        
        # Judul
        ttk.Label(form_frame, text="Judul Buku:").grid(row=1, column=0, sticky="w", padx=padx, pady=pady)
        self.judul_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.judul_var, width=50).grid(row=1, column=1, padx=padx, pady=pady)
        
        # Penulis
        ttk.Label(form_frame, text="Penulis:").grid(row=2, column=0, sticky="w", padx=padx, pady=pady)
        self.penulis_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.penulis_var, width=50).grid(row=2, column=1, padx=padx, pady=pady)
        
        # Tahun
        ttk.Label(form_frame, text="Tahun Terbit:").grid(row=3, column=0, sticky="w", padx=padx, pady=pady)
        self.tahun_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.tahun_var, width=50).grid(row=3, column=1, padx=padx, pady=pady)

        # Penerbit
        ttk.Label(form_frame, text="Penerbit:").grid(row=4, column=0, sticky="w", padx=padx, pady=pady)
        self.penerbit_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.penerbit_var, width=50).grid(row=4, column=1, padx=padx, pady=pady)

        # Genre
        ttk.Label(form_frame, text="Genre:").grid(row=5, column=0, sticky="w", padx=padx, pady=pady)
        self.genre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.genre_var, width=50).grid(row=5, column=1, padx=padx, pady=pady)

        # ISBN
        ttk.Label(form_frame, text="ISBN:").grid(row=6, column=0, sticky="w", padx=padx, pady=pady)
        self.isbn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.isbn_var, width=50).grid(row=6, column=1, padx=padx, pady=pady)
        
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        # Update button
        update_button = ttk.Button(
            button_frame,
            text="Update Data",
            command=self.update_buku
        )
        update_button.pack(side="left", padx=5)
        
        # View All button
        view_button = ttk.Button(
            button_frame,
            text="Lihat Semua Buku",
            command=lambda: controller.show_frame("ViewBooksFrame")
        )
        view_button.pack(side="left", padx=5)
    
    def populate_fields(self, values):
        """Isi form dengan data buku yang dipilih"""
        self.id_var.set(values[0])
        self.judul_var.set(values[1])
        self.penulis_var.set(values[2])
        self.tahun_var.set(values[3])
        self.penerbit_var.set(values[3])
        self.genre_var.set(values[3])
        self.isbn_var.set(values[3])
    
    def on_show_frame(self):
        """Dipanggil saat frame ditampilkan"""
        # Jika tidak ada data yang diisi (misal dari home langsung ke update)
        # Maka tampilkan dialog untuk memilih buku dari daftar
        if not self.id_var.get():
            messagebox.showinfo("Pilih Buku", "Silakan pilih buku dari daftar untuk diupdate.")
            self.controller.show_frame("ViewBooksFrame")
    
    def update_buku(self):
        """Fungsi untuk mengupdate data buku"""
        id_buku = self.id_var.get()
        judul = self.judul_var.get().strip()
        penulis = self.penulis_var.get().strip()
        tahun = self.tahun_var.get().strip()
        penerbit = self.penerbit_var.get().strip()
        genre = self.genre_var.get().strip()
        isbn = self.isbn_var.get().strip()
        
        # Validation
        if not id_buku or not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
            
        try:
            # Update book
            success = update_book(int(id_buku), judul, penulis, tahun, penerbit, genre, isbn)
            
            if success:
                # Refresh all frames
                self.controller.refresh_all_frames()
                
                messagebox.showinfo("Sukses", "Buku berhasil diupdate!")
                
                # Go back to view books
                self.controller.show_frame("ViewBooksFrame")
            else:
                messagebox.showwarning("Peringatan", "ID buku tidak ditemukan.")
        except ValueError:
            messagebox.showerror("Error", "ID buku harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate data: {str(e)}")