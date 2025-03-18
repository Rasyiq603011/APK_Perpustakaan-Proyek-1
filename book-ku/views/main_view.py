import tkinter as tk
from tkinter import messagebox

from models.book_model import BookModel
from models.user_model import UserModel
from models.borrowing_model import BorrowingModel

from controllers.auth_controller import AuthController
from controllers.book_controller import BookController
from controllers.borrow_controller import BorrowController

from views.login_view import LoginView
from views.home_view import HomeView
from views.book_view import BookView
from views.library_view import LibraryView

class MainView:
    """Main application view that coordinates all other views"""
    
    def __init__(self, root):
        """Initialize main application view"""
        self.root = root
        self.current_view = None
        self.current_user = None
        
        # Set up window properties
        self.setup_window()
        
        # Initialize models
        self.book_model = BookModel()
        self.user_model = UserModel()
        self.borrowing_model = BorrowingModel()
        
        # Initialize controllers
        self.auth_controller = AuthController(self.user_model)
        self.book_controller = BookController(self.book_model)
        self.borrow_controller = BorrowController(
            self.book_model, 
            self.user_model, 
            self.borrowing_model
        )
        
        # Show login view by default
        self.show_login()
    
    def setup_window(self):
        """Set up the main window properties"""
        self.root.title("BOOK-KU!")
        
        # Set window size (fullscreen or specific dimensions)
        # Uncomment to use fullscreen
        # self.root.attributes('-fullscreen', True)
        
        # Or use specific dimensions
        window_width = 1000
        window_height = 800
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def show_login(self):
        """Show login view"""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = LoginView(
            self.root,
            self.auth_controller,
            on_login_success=self.on_login_success
        )
    
    def show_home(self):
        """Show home view"""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = HomeView(
            self.root,
            self.book_controller,
            on_book_select=self.show_book_details,
            on_nav_callback=self.handle_navigation
        )
    
    def show_book_details(self, isbn):
        """Show book details view"""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = BookView(
            self.root,
            self.book_controller,
            self.borrow_controller,
            on_back=self.show_home
        )
        self.current_view.display_book(isbn)
    
    def show_library(self):
        """Show library view (borrowed books)"""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = LibraryView(
            self.root,
            self.borrow_controller,
            self.book_controller,
            on_book_select=self.show_book_details,
            on_nav_callback=self.handle_navigation
        )
    
    def handle_navigation(self, destination):
        """Handle navigation between views"""
        if destination == "home":
            self.show_home()
        elif destination == "library":
            self.show_library()
        elif destination == "logout":
            self.logout()
        else:
            messagebox.showinfo("Info", f"Navigation to {destination} not yet implemented")
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.show_home()
    
    def logout(self):
        """Handle logout"""
        # Log out from controller
        self.auth_controller.logout()
        self.current_user = None
        
        # Show login view
        self.show_login()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()