import json
import os
import hashlib
from datetime import datetime, timedelta

class UserModel:
    """
    Model for managing user data and authentication.
    """
    def __init__(self, file_path="data/users.json"):
        """Initialize user model with data from JSON file"""
        self.file_path = file_path
        self.current_user = None
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Load user data or create empty dict if file doesn't exist
        self.users = self._load_users()
        
        # Initialize admin user if not exists
        self._initialize_admin()
    
    def _load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.file_path, "w") as file:
            json.dump(self.users, file, indent=4)
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _initialize_admin(self):
        """Initialize admin user if not exists"""
        admin_username = "admin"
        admin_password = "admin123"
        
        if admin_username not in self.users:
            self.users[admin_username] = {
                "name": "Administrator",
                "password": self._hash_password(admin_password),
                "is_admin": True,
                "borrowed_books": [],
                "history": []
            }
            self._save_users()
    
    def register_user(self, name, username, password):
        """Register a new user"""
        if not name or not username or not password:
            return False, "Name, username, and password cannot be empty!"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters!"
        
        if username in self.users:
            return False, "Username already exists!"
        
        # Create new user
        self.users[username] = {
            "name": name,
            "password": self._hash_password(password),
            "is_admin": False,
            "borrowed_books": [],
            "history": []
        }
        
        self._save_users()
        return True, "Registration successful! Please login."
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if not username or not password:
            return False, "Username and password cannot be empty!"
        
        if username not in self.users:
            return False, "Invalid username or password!"
        
        if self.users[username]["password"] != self._hash_password(password):
            return False, "Invalid username or password!"
        
        # Set current user
        self.current_user = username
        return True, f"Login successful! Welcome, {self.users[username]['name']}!"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged-in user info"""
        if not self.current_user:
            return None
        
        user_data = self.users[self.current_user].copy()
        user_data["username"] = self.current_user
        return user_data
    
    def is_admin(self):
        """Check if current user is admin"""
        if not self.current_user:
            return False
        
        return self.users[self.current_user].get("is_admin", False)
    
    def borrow_book(self, isbn, title, due_date=None):
        """
        Add a book to user's borrowed books
        Returns: (success, message)
        """
        if not self.current_user:
            return False, "You must be logged in to borrow books!"
        
        # Check if user already has this book
        for book in self.users[self.current_user]["borrowed_books"]:
            if book["isbn"] == isbn:
                return False, "You have already borrowed this book!"
        
        # Set due date (14 days from now by default)
        if not due_date:
            due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        # Add to borrowed books
        borrow_info = {
            "isbn": isbn,
            "title": title,
            "borrow_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date
        }
        
        self.users[self.current_user]["borrowed_books"].append(borrow_info)
        
        # Add to history
        history_entry = borrow_info.copy()
        history_entry["action"] = "borrow"
        self.users[self.current_user]["history"].append(history_entry)
        
        self._save_users()
        return True, f"You have successfully borrowed '{title}'."
    
    def return_book(self, isbn):
        """
        Remove a book from user's borrowed books
        Returns: (success, message)
        """
        if not self.current_user:
            return False, "You must be logged in to return books!"
        
        # Find the book in borrowed books
        borrowed_books = self.users[self.current_user]["borrowed_books"]
        for i, book in enumerate(borrowed_books):
            if book["isbn"] == isbn:
                # Remove from borrowed books
                returned_book = borrowed_books.pop(i)
                
                # Add to history
                history_entry = returned_book.copy()
                history_entry["action"] = "return"
                history_entry["return_date"] = datetime.now().strftime("%Y-%m-%d")
                self.users[self.current_user]["history"].append(history_entry)
                
                self._save_users()
                return True, f"You have successfully returned '{returned_book['title']}'."
        
        return False, "You haven't borrowed this book!"
    
    def get_borrowed_books(self):
        """Get list of books borrowed by current user"""
        if not self.current_user:
            return []
        
        return self.users[self.current_user]["borrowed_books"]
    
    def get_borrow_history(self):
        """Get borrow/return history of current user"""
        if not self.current_user:
            return []
        
        return self.users[self.current_user]["history"]