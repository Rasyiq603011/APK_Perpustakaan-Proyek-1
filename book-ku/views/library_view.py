import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from views.components import UIComponents, PURPLE_COLOR, GREEN_COLOR

class LibraryView:
    """View for displaying user's borrowed books"""
    
    def __init__(self, parent, borrow_controller, book_controller, on_book_select=None, on_nav_callback=None):
        """Initialize library view"""
        self.parent = parent
        self.borrow_controller = borrow_controller
        self.book_controller = book_controller
        self.on_book_select = on_book_select
        self.on_nav_callback = on_nav_callback
        self.main_frame = None
    
    def _create_view(self):
        """Create the library view"""
        # Clear existing frame if any
        if self.main_frame:
            self.main_frame.destroy()
        
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill="both")
        
        # Header
        UIComponents.create_header(
            self.main_frame, 
            welcome_text="My Library - Books You've Borrowed"
        )
        
        # Search bar
        search_entry = UIComponents.create_search_bar(
            self.main_frame,
            placeholder="Search Your Library",
            command=self._on_search
        )
        
        # Content frame
        content_frame, _ = UIComponents.create_scrollable_frame(self.main_frame)
        
        # Title
        title_frame = tk.Frame(content_frame, bg="white")
        title_frame.pack(fill="x", pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="MY LIBRARY",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title_label.pack()
        
        # Get borrowed books
        borrowed_books = self.borrow_controller.get_borrowed_books()
        
        if not borrowed_books or len(borrowed_books) == 0:
            # No books borrowed
            empty_label = tk.Label(
                content_frame,
                text="You haven't borrowed any books yet.",
                font=("Arial", 14),
                bg="white",
                fg="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Create grid for books
            self._create_borrowed_books_grid(content_frame, borrowed_books)
        
        # Footer
        nav_buttons = UIComponents.create_footer(self.main_frame)
        
        # Bind navigation buttons
        if self.on_nav_callback:
            nav_buttons["profile"].config(command=lambda: self.on_nav_callback("profile"))
            nav_buttons["library"].config(command=lambda: self.on_nav_callback("library"))
            nav_buttons["home"].config(command=lambda: self.on_nav_callback("home"))
            nav_buttons["notifications"].config(command=lambda: self.on_nav_callback("notifications"))
            nav_buttons["logout"].config(command=lambda: self.on_nav_callback("logout"))
    
    def _create_borrowed_books_grid(self, parent, borrowed_books):
        """Create a grid of borrowed books"""
        # Container frame
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get default image
        try:
            if os.path.exists("assets/images/default.jpg"):
                default_img = Image.open("assets/images/default.jpg")
            else:
                default_img = Image.new('RGB', (100, 150), color = (200, 200, 200))
            default_img = default_img.resize((100, 150))
            default_photo = ImageTk.PhotoImage(default_img)
        except:
            default_img = Image.new('RGB', (100, 150), color = (200, 200, 200))
            default_img = default_img.resize((100, 150))
            default_photo = ImageTk.PhotoImage(default_img)
        
        # Create book items
        for index, book in enumerate(borrowed_books):
            # Book item frame
            book_frame = tk.Frame(grid_frame, bg="white", bd=1, relief="solid")
            book_frame.pack(fill="x", pady=10, padx=50)
            
            # Book image
            img_frame = tk.Frame(book_frame, bg="white")
            img_frame.pack(side="left", padx=20, pady=10)
            
            # Try to get book details
            book_data = self.book_controller.get_book_by_isbn(book['isbn'])
            
            # Load image
            try:
                if book_data and 'Image' in book_data and os.path.exists(f"assets/images/{book_data['Image']}"):
                    img = Image.open(f"assets/images/{book_data['Image']}")
                    img = img.resize((100, 150))
                    photo = ImageTk.PhotoImage(img)
                else:
                    photo = default_photo
            except:
                photo = default_photo
            
            img_label = tk.Label(img_frame, image=photo, bg="white")
            img_label.image = photo  # Keep reference
            img_label.pack()
            
            # Book details
            info_frame = tk.Frame(book_frame, bg="white")
            info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10, anchor="w")
            
            # Title
            title_label = tk.Label(
                info_frame,
                text=book['title'],
                font=("Arial", 14, "bold"),
                bg="white",
                anchor="w"
            )
            title_label.pack(fill="x", anchor="w")
            
            # Dates
            borrow_date_label = tk.Label(
                info_frame,
                text=f"Borrowed: {book['borrow_date']}",
                font=("Arial", 12),
                bg="white",
                anchor="w"
            )
            borrow_date_label.pack(fill="x", pady=5, anchor="w")
            
            due_date_label = tk.Label(
                info_frame,
                text=f"Due: {book['due_date']}",
                font=("Arial", 12),
                bg="white",
                anchor="w"
            )
            due_date_label.pack(fill="x", anchor="w")
            
            # Buttons frame
            buttons_frame = tk.Frame(book_frame, bg="white")
            buttons_frame.pack(side="right", padx=20, pady=10)
            
            # Return button
            return_btn = UIComponents.create_button(
                buttons_frame,
                "Return",
                command=lambda isbn=book['isbn']: self._on_return(isbn),
                bg=GREEN_COLOR,
                fg="black"
            )
            return_btn.pack(pady=5)
            
            # View details button
            view_btn = UIComponents.create_button(
                buttons_frame,
                "Details",
                command=lambda isbn=book['isbn']: self._on_view_details(isbn)
            )
            view_btn.pack(pady=5)
    
    def _on_return(self, isbn):
        """Handle book return"""
        if not self.borrow_controller:
            return
        
        # Confirm return
        confirm = messagebox.askyesno(
            "Confirm Return",
            "Are you sure you want to return this book?"
        )
        
        if not confirm:
            return
        
        # Return book
        success, message = self.borrow_controller.return_book(isbn)
        
        if success:
            messagebox.showinfo("Success", message)
            # Refresh view
            self.refresh()
        else:
            messagebox.showerror("Error", message)
    
    def _on_view_details(self, isbn):
        """Handle view book details"""
        if self.on_book_select:
            self.on_book_select(isbn)
    
    def _on_search(self, query):
        """Handle search in library"""
        # Not implemented in this version
        messagebox.showinfo("Search", f"Searching for '{query}' in your library")
    
    def refresh(self):
        """Refresh the view"""
        self._create_view()
    
    def show(self):
        """Show the view"""
        self._create_view()
        self.main_frame.pack(expand=True, fill="both")
    
    def hide(self):
        """Hide the view"""
        if self.main_frame:
            self.main_frame.pack_forget()
    
    def destroy(self):
        """Destroy the view"""
        if self.main_frame:
            self.main_frame.destroy()