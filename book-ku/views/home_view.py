import tkinter as tk
from tkinter import messagebox
from views.components import UIComponents, PURPLE_COLOR

class HomeView:
    """View for home screen with book grid"""
    
    def __init__(self, parent, book_controller, on_book_select=None, on_nav_callback=None):
        """Initialize home view"""
        self.parent = parent
        self.book_controller = book_controller
        self.on_book_select = on_book_select
        self.on_nav_callback = on_nav_callback
        self.main_frame = None
        self.search_entry = None
        self.books_frame = None
        self.current_books = None
        
        # Create view
        self._create_view()
    
    def _create_view(self):
        """Create the home view"""
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill="both")
        
        # Header
        UIComponents.create_header(self.main_frame)
        
        # Search bar
        self.search_entry = UIComponents.create_search_bar(
            self.main_frame,
            command=self._on_search
        )
        
        # Scrollable content
        content_frame, _ = UIComponents.create_scrollable_frame(self.main_frame)
        
        # Load and display books
        self._load_books(content_frame)
        
        # Footer with navigation
        nav_buttons = UIComponents.create_footer(self.main_frame)
        
        # Bind navigation buttons
        if self.on_nav_callback:
            nav_buttons["profile"].config(command=lambda: self.on_nav_callback("profile"))
            nav_buttons["library"].config(command=lambda: self.on_nav_callback("library"))
            nav_buttons["home"].config(command=lambda: self.on_nav_callback("home"))
            nav_buttons["notifications"].config(command=lambda: self.on_nav_callback("notifications"))
            nav_buttons["logout"].config(command=lambda: self.on_nav_callback("logout"))
    
    def _load_books(self, parent_frame):
        """Load and display books in a grid"""
        # Get all books
        self.current_books = self.book_controller.get_all_books()
        
        # Create book grid
        self.books_frame = UIComponents.create_book_grid(
            parent_frame, 
            self.current_books, 
            command=self._on_book_selected
        )
    
    def _on_book_selected(self, isbn):
        """Handle book selection"""
        if self.on_book_select:
            self.on_book_select(isbn)
    
    def _on_search(self, query):
        """Handle search"""
        # Search books
        search_results = self.book_controller.search_books(query)
        
        # Update current books
        self.current_books = search_results
        
        # Recreate books frame
        if self.books_frame:
            self.books_frame.destroy()
        
        # Get parent frame for books
        parent_frame = self.main_frame.winfo_children()[2]  # Header, search, content frame
        
        # Create new book grid with search results
        self.books_frame = UIComponents.create_book_grid(
            parent_frame, 
            search_results, 
            command=self._on_book_selected
        )
    
    def refresh(self):
        """Refresh the view"""
        # Destroy current view
        if self.main_frame:
            self.main_frame.destroy()
        
        # Create new view
        self._create_view()
    
    def show(self):
        """Show the view"""
        self.main_frame.pack(expand=True, fill="both")
    
    def hide(self):
        """Hide the view"""
        self.main_frame.pack_forget()
    
    def destroy(self):
        """Destroy the view"""
        if self.main_frame:
            self.main_frame.destroy()