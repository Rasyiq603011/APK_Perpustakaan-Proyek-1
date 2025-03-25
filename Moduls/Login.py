import json
import os
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.logs_file = os.path.join(self.data_dir, "logs.json")
        
        os.makedirs(self.data_dir, exist_ok=True)
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize users and logs files if they don't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({
                    "admin@bookku.com": {
                        "name": "Administrator",
                        "password": "admin1234",
                        "role": "admin"
                    }
                }, f, indent=4)
        
        if not os.path.exists(self.logs_file):
            with open(self.logs_file, 'w') as f:
                json.dump([], f, indent=4)
    
    def register(self, name, email, password):
        """Register a new user"""
        # Basic validation
        if not name or not email or not password:
            return False, "Please fill all fields"
        
        # Password validation
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Email validation (basic)
        if "@" not in email or "." not in email:
            return False, "Please enter a valid email address"
        
        # Check if email already exists
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if email in users:
            return False, "Email already registered"
        
        # Add new user
        users[email] = {
            "name": name,
            "password": password,
            "role": "user"  # Default role is user
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
        
        return True, "Account created successfully"
    
    def login(self, email, password):
        """Login a user"""
        if not email or not password:
            return False, "Please enter both email and password", None
        
        # Check credentials
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if email not in users or users[email]["password"] != password:
            return False, "Invalid email or password", None
        
        # Log successful login
        self._log_login(email, users[email]["role"])
        
        # Return user info
        user_info = {
            "email": email,
            "name": users[email]["name"],
            "role": users[email]["role"]
        }
        
        return True, "Login successful", user_info
    
    def _log_login(self, email, role):
        """Log login activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.logs_file, 'r') as f:
            logs = json.load(f)
        
        logs.append({
            "email": email,
            "role": role,
            "action": "login",
            "timestamp": timestamp
        })
        
        with open(self.logs_file, 'w') as f:
            json.dump(logs, f, indent=4)
