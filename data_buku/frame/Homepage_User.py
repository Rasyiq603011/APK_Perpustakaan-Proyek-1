import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class Homepage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.title("Homepage")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.create_widgets()
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def create_widgets(self):
            self.book_frame = tk.Frame(self.mainFrame)
            self.book_frame.pack(fill=tk.BOTH, expand=True)
            
            self.photo_references = {}
            self.total_books = 20
            self.display_books()

        def display_books(self):
            cek = True
            i = 0
            count = 0
            # Implementasi algoritma sesuai permintaan
            while cek:
                for j in range(4):  # 4 kolom
                    if count < self.total_books:
                        book_id = count + 1
                        self.create_book_button({
                            "id": book_id,
                            "title": f"Buku #{book_id}"
                        }, i, j)
                        count += 1
                    else:
                        cek = False
                        break
                i += 1
        
        def create_book_button(self, book, row, col):
        
            # Frame untuk setiap buku
            book_frame = tk.Frame(self.book_frame, padx=5, pady=5, bg="#42f5bf")
            book_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            
            # Memuat gambar cover (gunakan gambar yang sama untuk semua buku)
            photo = self.load_image()
            self.photo_references[book.get_id()] = photo
            
            # Button dengan gambar cover
            btn = tk.Button(
                book_frame, 
                image=photo, 
                text=book.get_id(),
                compound=tk.TOP,
                width=110,
                height=180,
                wraplength=100
            )
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Menambahkan handler
            btn.configure(command=lambda b=book: self.on_book_click(b))
            
            # Binding scroll pada button juga
            btn.bind("<MouseWheel>", self.on_mousewheel)
            btn.bind("<Button-4>", self.on_mousewheel)
            btn.bind("<Button-5>", self.on_mousewheel)
