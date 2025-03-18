import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Moduls.Book_Manager import BookManager as L


class DetailsBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, book=None):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        self.pack(expand=True, fill="both")
        self.controller = controller
        self.selectedBook = book
        self.defaultCover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.dataDir = os.path.join(os.path.dirname(__file__), "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover")
        
        # Frame utama untuk layout (tanpa grid)
        self.main_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Back button di bagian atas
        self.back_btn = ctk.CTkButton(
            self.main_frame, 
            text="← Kembali", 
            command= lambda: self.controller.show_frame("home") if hasattr(self.controller, 'show_frame') else None,
            fg_color="#4C0086",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            corner_radius=15,
            width=150,
            height=35
        )
        self.back_btn.pack(anchor="nw", padx=20, pady=10)
        
        # Content container for book details
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1E1E1E", corner_radius=10)
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Book image and info container
        self.info_container = ctk.CTkFrame(self.content_frame, fg_color="#2D2D2D", corner_radius=10)
        self.info_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side for image
        self.img_frame = ctk.CTkFrame(self.info_container, fg_color="#2D2D2D", corner_radius=0, width=200)
        self.img_frame.pack(side="left", fill="y", padx=(20, 20))
        
        # Placeholder for book cover
        self.img_label = ctk.CTkLabel(self.img_frame, text="")
        self.img_label.pack(pady=10)
        
        # Right side for book info
        self.details_frame = ctk.CTkFrame(self.info_container, fg_color="#2D2D2D", corner_radius=0)
        self.details_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Button container di bawah
        self.button_container = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=60)
        self.button_container.pack(fill="x", pady=(10, 20))
        
        # Dua kolom untuk tombol
        self.button_container.columnconfigure(0, weight=1)
        self.button_container.columnconfigure(1, weight=1)
        
        # Borrow button
        self.borrow_btn = ctk.CTkButton(
            self.button_container,
            text="Pinjam Buku",
            command=self.borrow_book if hasattr(self, 'borrow_book') else None,
            fg_color="#00CC00",
            hover_color="#00AA00",
            text_color="black",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=200
        )
        self.borrow_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        # Wishlist button
        self.wishlist_btn = ctk.CTkButton(
            self.button_container,
            text="Tambah ke Wishlist",
            command=self.add_to_wishlist if hasattr(self, 'add_to_wishlist') else None,
            fg_color="#4C0086",
            hover_color="#3C0066",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=200
        )
        self.wishlist_btn.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Update book details if provided
        if self.selectedBook is not None:
            self.update_book_details()

    def borrow_book(self):
        print("Pinjam buku clicked")
        
    def add_to_wishlist(self):
        print("Tambah ke wishlist clicked")

    def show_book_detail(self, book):
        self.selectedBook = book
        if hasattr(self.controller, 'show_frame'):
            self.controller.show_frame("detail")
        self.update_book_details()

    def update_book_details(self):
        """Update the detail frame with selected book info"""
        if self.selectedBook is None:
            return
            
        # Clear existing content
        for widget in self.details_frame.winfo_children():
            widget.destroy()
            
        # Load book image
        size = (180, 270)
        isbn = str(self.selectedBook.get('ISBN', ''))
        img_path = os.path.join(self.dataDir, f"{isbn}.jpeg")

        if not os.path.exists(img_path) or not isbn:
            img_path = self.defaultCover
            
        try:
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.img_label.configure(image=photo_img)
            self.img_label.image = photo_img
        except Exception as e:
            print(f"Error loading image: {e}")
            
        # Title frame with textbox for better wrapping
        title_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        title_frame.pack(fill="x", anchor="w", pady=(0, 20))

        title_textbox = ctk.CTkTextbox(
            title_frame,
            height=60,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white",
            wrap="word",
            fg_color="transparent",
            border_width=0,
            activate_scrollbars=False
        )
        title_textbox.pack(fill="x", anchor="w")
        title_textbox.insert("1.0", self.selectedBook.get('Judul', 'Tidak Ada Judul'))
        title_textbox.configure(state="disabled")

        # Info fields
        fields = [
            ("Penulis", "Penulis", "Tidak Diketahui"),
            ("Penerbit", "Penerbit", "Tidak Diketahui"),
            ("Tahun", "Tahun", "Tidak Diketahui"),
            ("Kategori", "Kategori", "Tidak Diketahui"),
            ("ISBN", "ISBN", "Tidak Diketahui"),
            ("Halaman", "Halaman", "Tidak Diketahui")
        ]
        
        for label_text, key, default in fields:
            field_label = ctk.CTkLabel(
                self.details_frame,
                text=f"{label_text}: {self.selectedBook.get(key, default)}",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                wraplength=600,
                justify="left"
            )
            field_label.pack(anchor="w", pady=5)

        # Description with scrollable textbox
        if 'Deskripsi' in self.selectedBook and str(self.selectedBook['Deskripsi']) != 'nan':
            desc_title = ctk.CTkLabel(
                self.details_frame,
                text="Deskripsi:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="white",
                wraplength=600,
                justify="left"
            )
            desc_title.pack(anchor="w", pady=(20, 5))
            
            # Frame for scrollable description
            desc_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
            desc_frame.pack(fill="both", expand=True, anchor="w", pady=5)
            
            # Description textbox with scrollbar
            desc_textbox = ctk.CTkTextbox(
                desc_frame,
                width=600,
                height=150,
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="white",
                wrap="word",
                fg_color="#333333",
                border_width=0,
                activate_scrollbars=True
            )
            desc_textbox.pack(fill="both", expand=True, padx=(0, 10))
            
            desc_textbox.insert("1.0", str(self.selectedBook['Deskripsi']))
            desc_textbox.configure(state="disabled")
            desc_textbox.see("1.0")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Book Details")
    root.geometry("1024x768")
    
    # Untuk testing, buat sample data sederhana jika BookManager tidak berfungsi
    try:
        book = L('D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku.xlsx', 'Cover', "img.jpg")
        sample_book = L.getBookByIndeks(book, 14)
    except Exception as e:
        print(f"Error loading book data: {e}")
        # Fallback data
        sample_book = {
            'Judul': 'Quidditch Through the Ages: the Illustrated Edition',
            'Penulis': 'J. K. Rowling',
            'Penerbit': 'Tidak Diketahui',
            'Tahun': '2020',
            'Kategori': 'Juvenile Fiction',
            'ISBN': '9781338340563',
            'Halaman': '0',
            'Deskripsi': 'Kennilworthy Whisp is a fictitious author created by J.K. Rowling.'
        }
    
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    
    app = DetailsBookFrame(frame, root, sample_book)
    root.mainloop()