import os
from datetime import datetime

class HomeManager:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    
    def get_current_date(self):
        """Get formatted current date"""
        return datetime.now().strftime("%A, %d %B %Y")
    
    def get_user_info(self, current_user):
        if current_user:
            return {
                "name": current_user.get("name", "Guest"),
                "role": current_user.get("role", "guest")
            }
        return {"name": "Guest", "role": "guest"}
    
    def get_navigation_config(self, user_role):
        """Get navigation button configuration based on user role"""
        if user_role == "admin":
            return [
                {"text": "Manage Books", "icon": "books.png", "frame": "DataBookFrame", "color": "#6200EA"},
                {"text": "Add New Book", "icon": "add_book.png", "frame": "AddBookFrame", "color": "#00C853"},
                {"text": "Access Logs", "icon": "logs.png", "frame": "LogFrame", "color": "#FF6D00"}
            ]
        elif user_role == "user":
            return [
                {"text": "Browse Books", "icon": "books.png", "frame": "DataBookFrame", "color": "#6200EA"},
                {"text": "My Penalties", "icon": "penalty.png", "frame": "PenaltyFrame", "color": "#D50000"},
                {"text": "My Books", "icon": "my_books.png", "frame": "MyBookFrame", "color": "#00B0FF"}
            ]
        else:  # guest
            return [
                {"text": "Browse Books", "icon": "books.png", "frame": "DataBookFrame", "color": "#6200EA"},
                {"text": "Login", "icon": "login.png", "frame": "LoginFrame", "color": "#00C853"},
                {"text": "About", "icon": "about.png", "frame": "AboutFrame", "color": "#FF6D00"}
            ]
    
    def get_copyright_text(self):
        """Get copyright text with current year"""
        return f"© {datetime.now().year} BOOK-KU Library Management System"
    
    def get_asset_path(self, asset_name):
        """Get full path for an asset file"""
        return os.path.join(self.assets_dir, asset_name)
    
    def adjust_color(self, hex_color, amount=20):
        """Adjust hex color brightness"""
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - amount)
        g = max(0, int(hex_color[2:4], 16) - amount)
        b = max(0, int(hex_color[4:6], 16) - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
