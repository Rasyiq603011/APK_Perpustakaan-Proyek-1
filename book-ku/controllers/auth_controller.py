from models.user_model import UserModel

class AuthController:
    """
    Controller for handling user authentication operations
    """
    def __init__(self, user_model=None):
        """Initialize controller with user model"""
        self.user_model = user_model if user_model else UserModel()
    
    def register(self, name, username, password, confirm_password):
        """
        Register a new user
        Returns: (success, message)
        """
        # Validate inputs
        if not name or not username or not password:
            return False, "Name, username, and password are required!"
        
        if password != confirm_password:
            return False, "Passwords do not match!"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters!"
        
        # Register user
        return self.user_model.register_user(name, username, password)
    
    def login(self, username, password):
        """
        Authenticate user
        Returns: (success, message, user_data)
        """
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required!", None
        
        # Authenticate
        success, message = self.user_model.authenticate(username, password)
        
        if success:
            user_data = self.user_model.get_current_user()
            return True, message, user_data
        else:
            return False, message, None
    
    def logout(self):
        """Log out current user"""
        self.user_model.logout()
        return True, "You have been logged out."
    
    def get_current_user(self):
        """Get current user data"""
        return self.user_model.get_current_user()
    
    def is_logged_in(self):
        """Check if a user is currently logged in"""
        return self.user_model.get_current_user() is not None
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.user_model.is_admin()
