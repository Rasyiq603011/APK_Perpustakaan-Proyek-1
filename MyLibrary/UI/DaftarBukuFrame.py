import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background
        
        self.controller = controller
        self.MyLibrary = controller.bookManager
        
        # Pagination settings
        self.books_per_page = 50  # 10 rows of 5 books
        self.current_page = 1
        self.total_pages = 1
        
        # Create main container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Header
        self.rowconfigure(1, weight=1)  # Content
        self.rowconfigure(2, weight=0)  # Pagination controls
        
        # Header section
        self.header_frame = ctk.CTkFrame(self, fg_color="#232323", height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.pack_propagate(False)  # Fixed height
        
        # Title
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="DAFTAR BUKU",
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=(20, 0))
        
        # Add Book button
        self.add_btn = ctk.CTkButton(
            self.header_frame,
            text="+ Tambah Buku",
            command=lambda: self.controller.showFrame("AddBookFrame"),
            fg_color="#6200EA",  # Purple color
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=10,
            height=40,
            width=150
        )
        self.add_btn.pack(side="right", padx=30, pady=(20, 0))
        
        # Content section - scrollable grid of books
        self.content_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Create scrollable frame for books
        self.book_container = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#1E1E1E",
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#666666"
        )
        self.book_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Book grid inside scrollable container
        self.book_grid = ctk.CTkFrame(self.book_container, fg_color="transparent")
        self.book_grid.pack(fill="both", expand=True)
        
        # Pagination controls
        self.pagination_frame = ctk.CTkFrame(self, fg_color="#232323", height=50)
        self.pagination_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.pagination_frame.columnconfigure(0, weight=1)
        self.pagination_frame.columnconfigure(1, weight=0)
        self.pagination_frame.columnconfigure(2, weight=0)
        self.pagination_frame.columnconfigure(3, weight=0)
        self.pagination_frame.columnconfigure(4, weight=1)
        
        # Previous page button
        self.prev_btn = ctk.CTkButton(
            self.pagination_frame,
            text="◀ Prev",
            command=self.previous_page,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12),
            corner_radius=8,
            width=80,
            height=30
        )
        self.prev_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        # Page indicator
        self.page_label = ctk.CTkLabel(
            self.pagination_frame,
            text="Page 1 of 1",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="white"
        )
        self.page_label.grid(row=0, column=2, padx=10, pady=10)
        
        # Next page button
        self.next_btn = ctk.CTkButton(
            self.pagination_frame,
            text="Next ▶",
            command=self.next_page,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12),
            corner_radius=8,
            width=80,
            height=30
        )
        self.next_btn.grid(row=0, column=3, padx=(10, 5), pady=10)
        
        # Populate grid with books
        self.populate_book_grid(self)
    
    def populate_book_grid(self, frame):
        """Populate the grid with book entries for the current page"""
        # Clear existing content
        for widget in frame.book_grid.winfo_children():
            widget.destroy()
            
        # Get all books from manager
        all_books = self.controller.getBook()
        
        if all_books is None or len(all_books) == 0:
            # Show message if no books
            no_books_label = ctk.CTkLabel(
                frame.book_grid,
                text="Tidak ada buku yang tersedia",
                fg_color="black",
                text_color="white",
                font=("Arial", 14)
            )
            no_books_label.pack(pady=50)
            return
        
        # Calculate total pages
        self.total_pages = math.ceil(len(all_books) / self.books_per_page)
        
        # Update page indicator
        self.page_label.configure(text=f"Page {self.current_page} of {self.total_pages}")
        
        # Update button states
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.total_pages else "disabled")
        
        # Calculate start and end indices for current page
        start_idx = (self.current_page - 1) * self.books_per_page
        end_idx = min(start_idx + self.books_per_page, len(all_books))
        
        # Get books for current page
        page_books = all_books.iloc[start_idx:end_idx]
            
        # Grid configuration
        cols = 5  # Number of books per row
        for i in range(cols):
            frame.book_grid.columnconfigure(i, weight=1)
            
        # Display books in grid
        for i, (_, book) in enumerate(page_books.iterrows()):
            row = i // cols
            col = i % cols
            
            # Create book frame - card-like appearance
            book_frame = ctk.CTkFrame(
                frame.book_grid,
                fg_color="#2B2B2B",
                corner_radius=10,
                border_width=0
            )
            book_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Load book image
            img = self.MyLibrary.LoadCover(book.get('ISBN', ''))
            
            # Book cover button
            btn = ctk.CTkButton(
                book_frame,
                image=img,
                text="",
                fg_color="transparent", 
                hover_color="#3D3D3D",
                border_width=0,
                command=lambda b=book: self.controller.showBookDetail(b)
            )
            btn.image = img  # Keep reference
            btn.pack(padx=5, pady=5, fill="x")
            
            # Book title (truncate if too long)
            title = book.get('Judul', 'Judul Tidak Ada')
            if len(title) > 20:
                title = title[:17] + "..."
                
            title_label = ctk.CTkLabel(
                book_frame, 
                text=title,
                fg_color="transparent",
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
                wraplength=120,
                anchor="center"
            )
            title_label.pack(padx=5, pady=5, fill="x")
            
            # Author (optional)
            author = book.get('Penulis', '')
            if author:
                if len(author) > 20:
                    author = author[:17] + "..."
                author_label = ctk.CTkLabel(
                    book_frame, 
                    text=author,
                    fg_color="transparent",
                    text_color="#AAAAAA",
                    font=ctk.CTkFont(family="Arial", size=10),
                    wraplength=120,
                    anchor="center"
                )
                author_label.pack(padx=5, pady=(0, 5), fill="x")
    
    def next_page(self):
        """Go to the next page of books"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.populate_book_grid(self)
    
    def previous_page(self):
        """Go to the previous page of books"""
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_book_grid(self)
    
    def show_book_detail(self, book):
        """Show book details when clicked"""
        if hasattr(self.controller, "showBookDetail"):
            self.controller.showBookDetail(book)


if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Daftar Buku")
    root.geometry("1024x768")
    
    # For testing - create a mock controller
    class MockController:
        def showFrame(self, frame_name):
            print(f"Would show frame: {frame_name}")
            
        def showBookDetail(self, book):
            print(f"Would show details for: {book.get('Judul', 'Unknown')}")
            
        def getBook(self):
            # Return some mock data
            import pandas as pd
            data = {
                'Judul': ['Laskar Pelangi', 'Harry Potter', 'Lord of the Rings'],
                'Penulis': ['Andrea Hirata', 'J.K. Rowling', 'J.R.R. Tolkien'],
                'ISBN': ['123456789', '987654321', '456789123']
            }
            return pd.DataFrame(data)
        
        # Mock BookManager for testing
        class MockBookManager:
            def LoadCover(self, isbn):
                return None  # In real app this would return an image
                
        bookManager = MockBookManager()
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = DataBookFrame(frame, MockController())
    app.pack(expand=True, fill="both")
    
    root.mainloop()