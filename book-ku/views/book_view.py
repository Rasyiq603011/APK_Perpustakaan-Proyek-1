import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from views.components import UIComponents, PURPLE_COLOR, GREEN_COLOR

class BookView:
    """View for displaying book details"""
    
    def __init__(self, parent, book_controller, borrow_controller=None, on_back=None):
        """Initialize book view"""
        self.parent = parent
        self.book_controller = book_controller
        self.borrow_controller = borrow_controller
        self.on_back = on_back
        self.main_frame = None
        self.current_book = None
    
    def display_book(self, isbn):
        """Display book details by ISBN"""
        # Get book data
        self.current_book = self.book_controller.get_book_by_isbn(isbn)
        
        if not self.current_book:
            messagebox.showerror("Error", "Book not found!")
            if self.on_back:
                self.on_back()
            return
        
        # Create view
        self._create_view()
    
    def _create_view(self):
        """Create the book detail view"""
        # Clear existing frame if any
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill="both")
        
        # Header
        UIComponents.create_header(self.main_frame)
        
        # Content frame
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(expand=True, fill="both")
        
        # Back button
        back_btn = UIComponents.create_back_button(content_frame, command=self._on_back)
        
        # Book title
        title_label = tk.Label(
            content_frame,
            text="BOOK TITLE",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title_label.pack(pady=(10, 5))
        
        # Book details container
        details_frame = tk.Frame(content_frame, bg="white")
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Book image
        img_frame = tk.Frame(details_frame, bg="white")
        img_frame.pack(side="right", padx=20, pady=10)
        
        try:
            if os.path.exists(f"assets/images/{self.current_book['Image']}"):
                img = Image.open(f"assets/images/{self.current_book['Image']}")
            else:
                img = Image.open("assets/images/default.jpg")
        except:
            # Create blank image if loading fails
            img = Image.new('RGB', (200, 300), color = (200, 200, 200))
        
        img = img.resize((200, 300))
        photo = ImageTk.PhotoImage(img)
        
        img_label = tk.Label(img_frame, image=photo, bg="white")
        img_label.image = photo  # Keep reference
        img_label.pack()
        
        # Book details
        info_frame = tk.Frame(details_frame, bg="white")
        info_frame.pack(side="left", fill="both", expand=True, anchor="nw")
        
        # Author
        author_label = tk.Label(
            info_frame,
            text=f"Nama Penulis: {self.current_book['Penulis']}",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        )
        author_label.pack(fill="x", pady=5, anchor="w")
        
        # Genre
        genre_label = tk.Label(
            info_frame,
            text=f"Genre: {self.current_book['Kategori']}",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        )
        genre_label.pack(fill="x", pady=5, anchor="w")
        
        # Publication year
        year_label = tk.Label(
            info_frame,
            text=f"Tahun Terbit: {self.current_book['Tahun']}",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        )
        year_label.pack(fill="x", pady=5, anchor="w")
        
        # Page count
        pages_label = tk.Label(
            info_frame,
            text=f"Jumlah Halaman: {self.current_book['Halaman']}",
            font=("Arial", 12),
            bg="white",
            anchor="w"
        )
        pages_label.pack(fill="x", pady=5, anchor="w")
        
        # Description (with scrollable text)
        desc_label = tk.Label(
            info_frame,
            text="Description:",
            font=("Arial", 12, "bold"),
            bg="white",
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(15, 5), anchor="w")
        
        desc_text = tk.Text(
            info_frame,
            font=("Arial", 11),
            bg="white",
            wrap="word",
            height=10,
            width=50,
            borderwidth=0,
            highlightthickness=0
        )
        desc_text.insert("1.0", self.current_book['Deskripsi'])
        desc_text.config(state="disabled")  # Make read-only
        desc_text.pack(fill="both", expand=True, anchor="w")
        
        # Status frame
        status_frame = tk.Frame(content_frame, bg="white")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Book status
        status_label = tk.Label(
            status_frame,
            text=f"Status Buku: {self.current_book['Status']}",
            font=("Arial", 12),
            bg="white"
        )
        status_label.pack(side="left", padx=20)
        
        # Borrow button (only if book is available)
        if self.current_book['Status'] == 'Available' and self.borrow_controller:
            borrow_btn = UIComponents.create_button(
                status_frame,
                "BORROW",
                command=self._on_borrow,
                bg=GREEN_COLOR,
                fg="black",
                width=15
            )
            borrow_btn.pack(side="right", padx=20)
        
        # Footer
        footer = UIComponents.create_footer(self.main_frame)
        
        # Set title text after setup (to avoid too early garbage collection)
        title_label.config(text=self.current_book['Judul'])
    
    def _on_back(self):
        """Handle back button click"""
        if self.on_back:
            self.on_back()
    
    def _on_borrow(self):
        """Handle borrow button click"""
        if not self.borrow_controller:
            return
        
        # Attempt to borrow the book
        success, message = self.borrow_controller.borrow_book(self.current_book['ISBN'])
        
        if success:
            messagebox.showinfo("Success", message)
            # Refresh view to update status
            self.display_book(self.current_book['ISBN'])
        else:
            messagebox.showerror("Error", message)
    
    def show(self):
        """Show the view"""
        if self.main_frame:
            self.main_frame.pack(expand=True, fill="both")
    
    def hide(self):
        """Hide the view"""
        if self.main_frame:
            self.main_frame.pack_forget()
    
    def destroy(self):
        """Destroy the view"""
        if self.main_frame:
            self.main_frame.destroy()
