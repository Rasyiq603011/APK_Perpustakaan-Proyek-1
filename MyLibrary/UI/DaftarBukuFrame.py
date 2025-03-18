    
import tkinter as tk
from tkinter import ttk

class DataBookFrame(tk.Frame):
     def __init__(self, parent, controller):
          tk.Frame.__init__(self, parent)
          self.controller = controller
def update_book_details(self):
        pass

def populate_book_grid(self, frame):
        for widget in frame.book_grid.winfo_children():
            widget.destroy()
            
        # Get books from manager
        books = self.controller.getBook()
        
        if len(books) == 0:
            # Show message if no books
            no_books_label = tk.Label(
                frame.book_grid,
                text="Tidak ada buku yang tersedia",
                fg="white",
                bg="black",
                font=("Arial", 14)
            )
            no_books_label.pack(pady=50)
            return
            
        # Grid configuration
        cols = 5
        for i in range(cols):
            frame.book_grid.columnconfigure(i, weight=1)
            
        # Display books in grid
        for i, (_, book) in enumerate(books.iterrows()):
            row = i // cols
            col = i % cols
            
            # Create book frame
            book_frame = tk.Frame(frame.book_grid, bg="white", bd=2, relief="solid")
            book_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Load book image
            img = self.MyLibrary.loadCover(book.get('ISBN', ''))
            
            # Book cover button
            btn = tk.Button(
                book_frame,
                image=img,
                bg="white",
                borderwidth=0,
                command=lambda b=book: self.show_book_detail(b)
            )
            btn.image = img  # Keep reference
            btn.pack(padx=5, pady=5)
            
            # Book title (truncate if too long)
            title = book.get('Judul', 'Judul Tidak Ada')
            if len(title) > 20:
                title = title[:17] + "..."
                
            title_label = tk.Label(
                book_frame, 
                text=title,
                bg="white",
                wraplength=100
            )
            title_label.pack(padx=5, pady=5)