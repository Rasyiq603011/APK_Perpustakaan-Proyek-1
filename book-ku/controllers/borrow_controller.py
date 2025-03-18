from models.book_model import BookModel
from models.user_model import UserModel
from models.borrowing_model import BorrowingModel

class BorrowController:
    """
    Controller for handling book borrowing operations
    """
    def __init__(self, book_model=None, user_model=None, borrowing_model=None):
        """Initialize controller with required models"""
        self.book_model = book_model if book_model else BookModel()
        self.user_model = user_model if user_model else UserModel()
        self.borrowing_model = borrowing_model if borrowing_model else BorrowingModel()
    
    def borrow_book(self, isbn):
        """
        Handle book borrowing process
        Returns: (success, message)
        """
        # Check if user is logged in
        user = self.user_model.get_current_user()
        if not user:
            return False, "You must be logged in to borrow books!"
        
        # Check if book exists
        book = self.book_model.get_book_by_isbn(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found!"
        
        # Check if book is available
        if book['Status'] != 'Available':
            return False, f"Book '{book['Judul']}' is not available for borrowing!"
        
        # Record borrowing in both systems
        success, borrow_id, due_date = self.borrowing_model.borrow_book(isbn, user['username'])
        
        if success:
            # Update book status
            self.book_model.change_book_status(isbn, 'Borrowed')
            self.book_model.save()
            
            # Update user's borrowed books
            self.user_model.borrow_book(isbn, book['Judul'], due_date)
            
            return True, f"You have successfully borrowed '{book['Judul']}'. Due date: {due_date}"
        else:
            return False, "Failed to borrow book!"
    
    def return_book(self, isbn):
        """
        Handle book return process
        Returns: (success, message)
        """
        # Check if user is logged in
        user = self.user_model.get_current_user()
        if not user:
            return False, "You must be logged in to return books!"
        
        # Check if book exists
        book = self.book_model.get_book_by_isbn(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found!"
        
        # Find borrowing record
        borrowings = self.borrowing_model.get_active_borrowings(user['username'])
        borrowings = borrowings[borrowings['ISBN'] == isbn]
        
        if len(borrowings) == 0:
            return False, "You haven't borrowed this book!"
        
        borrow_id = borrowings.iloc[0]['BorrowID']
        
        # Record return
        success, message = self.borrowing_model.return_book(borrow_id)
        
        if success:
            # Update book status
            self.book_model.change_book_status(isbn, 'Available')
            self.book_model.save()
            
            # Update user's borrowed books
            self.user_model.return_book(isbn)
            
            return True, f"You have successfully returned '{book['Judul']}'."
        else:
            return False, message
    
    def get_borrowed_books(self):
        """Get books borrowed by current user"""
        user = self.user_model.get_current_user()
        if not user:
            return []
        
        return self.user_model.get_borrowed_books()
    
    def get_borrow_history(self):
        """Get borrowing history of current user"""
        user = self.user_model.get_current_user()
        if not user:
            return []
        
        return self.user_model.get_borrow_history()
    
    def get_all_borrowed_books(self):
        """Get all borrowed books (admin only)"""
        user = self.user_model.get_current_user()
        if not user or not user.get('is_admin', False):
            return None
        
        return self.borrowing_model.get_active_borrowings()
    
    def get_overdue_books(self):
        """Get overdue books (admin only)"""
        user = self.user_model.get_current_user()
        if not user or not user.get('is_admin', False):
            return None
        
        return self.borrowing_model.get_overdue_books()
