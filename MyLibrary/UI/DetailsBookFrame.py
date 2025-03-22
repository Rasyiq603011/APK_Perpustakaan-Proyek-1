import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
from tkinter import messagebox
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Moduls.Book_Manager import BookManager as L


class DetailsBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background
        
        self.controller = controller
        self.selectedBook = self.controller.selectedBook
        self.defaultCover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.dataDir = os.path.join(os.path.dirname(__file__), "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover")
        
        # Main frame layout - Optimized for 1024x768
        self.columnconfigure(0, weight=3)  # Detail content
        self.columnconfigure(1, weight=2)  # Cover image
        self.rowconfigure(0, weight=0)  # Header row - fixed height
        self.rowconfigure(1, weight=1)  # Content row - expands
        self.rowconfigure(2, weight=0)  # Footer row - fixed height
        
        # ===== HEADER SECTION =====
        # Simplified header with less padding for more compact layout
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))
        self.header_frame.columnconfigure(0, weight=1)  # Back button
        self.header_frame.columnconfigure(1, weight=2)  # Title
        self.header_frame.columnconfigure(2, weight=1)  # Empty space for symmetry
        
        # Back button - made slightly more compact
        self.back_btn = ctk.CTkButton(
            self.header_frame, 
            text="← Kembali", 
            command=lambda: self.controller.showFrame("DataBookFrame"),
            fg_color="#6200EA",  # Deeper purple matching React design
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            corner_radius=15,
            width=120,
            height=30
        )
        self.back_btn.grid(row=0, column=0, sticky="w", padx=10)
        
        # Title - same size but centered better
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="DETAIL BUKU",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=1)
        
        # ===== CONTENT SECTION =====
        # Info container (left side)
        self.info_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Slightly lighter background for info
        self.info_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=5)
        
        # Initialize info frame - will be populated in update_book_details
        self.info_frame = ctk.CTkFrame(self.info_container, fg_color="transparent")
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cover container (right side)
        self.cover_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Matching info container color
        self.cover_container.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=5)
        
        # Setup cover section
        self.setup_cover_section()
        
        # ===== FOOTER SECTION =====
        # More compact footer
        self.footer = ctk.CTkFrame(self, fg_color="#232323", height=60, corner_radius=10)  # Darker footer
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 10))
        # Prevent height from changing
        self.footer.pack_propagate(False)
        
        # Edit button - Left side
        self.edit_btn = ctk.CTkButton(
            self.footer,
            text="Edit Data",
            command=lambda: self.controller.showFrame("UpdateBookFrame"),
            fg_color="#6200EA",  # Purple like other UI elements
            hover_color="#5000D0",  # Slightly lighter purple for hover
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=40,
            width=150
        )
        self.edit_btn.pack(side="left", padx=40, pady=10)
        
        # Borrow button - Right side
        self.borrow_btn = ctk.CTkButton(
            self.footer,
            text="Pinjam Buku",
            command=self.borrow_book,
            fg_color="#4CAF50",  # Material design green
            hover_color="#388E3C",  # Darker green for hover
            text_color="white",  # White text for better contrast
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=40,
            width=180
        )
        self.borrow_btn.pack(side="right", padx=40, pady=10)
        
        # Update book details if provided
        if self.selectedBook is not None:
            self.update_book_details()

    def setup_cover_section(self):
        """Setup the cover preview section"""
        # Configure cover container layout
        self.cover_container.columnconfigure(0, weight=1)
        self.cover_container.rowconfigure(0, weight=0)  # Label
        self.cover_container.rowconfigure(1, weight=1)  # Cover image
        self.cover_container.rowconfigure(2, weight=0)  # Info
        
        # Cover title
        cover_title = ctk.CTkLabel(
            self.cover_container,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        cover_title.grid(row=0, column=0, pady=(15, 10))
        
        # Cover image frame - Light background like in React design
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color="#F5F5F5", corner_radius=5)  # Light background for cover
        self.cover_frame.grid(row=1, column=0, pady=5)
        
        # Cover image label - using the recommended 180x270 ratio
        self.img_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.img_label.pack(padx=10, pady=10)
        
        # Book status info
        status_frame = ctk.CTkFrame(self.cover_container, fg_color="#363636", corner_radius=5)  # Slightly darker info frame
        status_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Status: Tersedia",  # Default status, will be updated
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#FFFFFF",
            justify="center"
        )
        self.status_label.pack(pady=8, padx=10)

    def borrow_book(self):
        """Handle borrowing book functionality"""
        # Make sure we have a valid book before attempting to borrow
        if self.selectedBook is None:
            messagebox.showerror("Error", "No book selected or book data is missing!")
            return
            
        if hasattr(self.controller, 'borrowBook'):
            self.controller.borrowBook(self.selectedBook)

    def update_book_details(self):
        """Update the detail frame with selected book info"""
        if self.selectedBook is None:
            return
            
        # Clear existing content in info frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        # Load book cover image
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
        
        # Update status
        status = self.selectedBook.get('Status', 'Tersedia')
        status_color = "#4CAF50" if status == "Tersedia" else "#FF6B6B"  # Green if available, red otherwise
        self.status_label.configure(text=f"Status: {status}", text_color=status_color)
            
        # Book title in larger font
        title_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent", height=70)
        title_frame.pack(fill="x", anchor="w", pady=(0, 15))
        title_frame.pack_propagate(False)  # Keep fixed height

        title_textbox = ctk.CTkTextbox(
            title_frame,
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="white",
            wrap="word",
            fg_color="transparent",
            border_width=0,
            activate_scrollbars=False
        )
        title_textbox.pack(fill="both", expand=True)
        title_textbox.insert("1.0", self.selectedBook.get('Judul', 'Tidak Ada Judul'))
        title_textbox.configure(state="disabled")

        # Book details in grid layout
        details_grid = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        details_grid.pack(fill="x", pady=10)
        
        # Configure grid
        details_grid.columnconfigure(0, weight=0)  # Label 1
        details_grid.columnconfigure(1, weight=1)  # Value 1
        details_grid.columnconfigure(2, weight=0)  # Label 2
        details_grid.columnconfigure(3, weight=1)  # Value 2
        
        # Info fields (first group in a grid)
        fields = [
            ("Penulis", "Penulis", "Tidak Diketahui"),
            ("Penerbit", "Penerbit", "Tidak Diketahui"),
            ("Tahun", "Tahun", "Tidak Diketahui"),
            ("Kategori", "Kategori", "Tidak Diketahui"),
            ("ISBN", "ISBN", "Tidak Diketahui"),
            ("Halaman", "Halaman", "Tidak Diketahui")
        ]
        
        for i, (label_text, key, default) in enumerate(fields):
            # Calculate row and column
            row = i // 2
            base_col = (i % 2) * 2
            
            # Label
            label = ctk.CTkLabel(
                details_grid,
                text=f"{label_text}:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="white",
                anchor="w",
                width=70
            )
            label.grid(row=row, column=base_col, padx=(5, 5), pady=8, sticky="w")
            
            # Value
            value = ctk.CTkLabel(
                details_grid,
                text=f"{self.selectedBook.get(key, default)}",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                anchor="w"
            )
            value.grid(row=row, column=base_col+1, padx=(0, 10), pady=8, sticky="w")

        # Description section
        if 'Deskripsi' in self.selectedBook and str(self.selectedBook['Deskripsi']) != 'nan':
            desc_title = ctk.CTkLabel(
                self.info_frame,
                text="Deskripsi:",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white",
                anchor="w"
            )
            desc_title.pack(anchor="w", pady=(20, 5))
            
            # Description textbox with scrollbar
            desc_textbox = ctk.CTkTextbox(
                self.info_frame,
                height=150,
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                wrap="word",
                fg_color="#3D3D3D",  # Lighter background for textarea
                border_color="#666666",  # Matching border color
                corner_radius=8,
                border_width=1,
                activate_scrollbars=True
            )
            desc_textbox.pack(fill="both", expand=True, pady=(0, 10))
            
            desc_textbox.insert("1.0", str(self.selectedBook['Deskripsi']))
            desc_textbox.configure(state="disabled")
            desc_textbox.see("1.0")


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Detail Buku")
    root.geometry("1024x768")
    
    # For testing, make a simple controller class
    class TestController:
        def show_frame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def showFrame(self, frame_name):
            print(f"Would show frame (camelCase): {frame_name}")
        
        def borrowBook(self, book):
            print(f"Would borrow book: {book.get('Judul', 'Unknown')}")
    
    # Sample book data for testing
    test_controller = TestController()
    test_controller.selectedBook = {
        'Judul': 'Laskar Pelangi',
        'Penulis': 'Andrea Hirata',
        'Penerbit': 'Bentang Pustaka',
        'Tahun': '2005',
        'Kategori': 'Novel',
        'ISBN': '9789793062792',
        'Halaman': '529',
        'Status': 'Tersedia',
        'Deskripsi': 'Novel ini bercerita tentang kehidupan 10 anak dari keluarga miskin yang bersekolah di sebuah sekolah Muhammadiyah di Belitung yang penuh dengan keterbatasan. Meskipun sekolah itu sangat sederhana, mereka menjadikan masa kanak-kanak mereka yang bahagia, dan Ikal menjadi penulis buku bertaraf internasional.'
    }
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = DetailsBookFrame(frame, test_controller)
    app.pack(expand=True, fill="both")
    
    root.mainloop()
