import pandas as pd
import os
from datetime import datetime, timedelta

class BorrowingModel:
    """
    Model for managing book borrowing and returns
    """
    def __init__(self, file_path="data/borrowings.xlsx"):
        """Initialize borrowing model with data from Excel file"""
        self.file_path = file_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if os.path.exists(file_path):
            self.borrowings = pd.read_excel(file_path)
        else:
            # Create empty DataFrame with required columns
            self.borrowings = pd.DataFrame(columns=[
                'BorrowID', 'ISBN', 'Username', 'BorrowDate', 
                'DueDate', 'ReturnDate', 'Status'
            ])
            self.save()
    
    def save(self):
        """Save borrowing data to Excel file"""
        self.borrowings.to_excel(self.file_path, index=False)
        return True
    
    def borrow_book(self, isbn, username):
        """
        Record a book borrowing
        Returns: (success, borrow_id, due_date)
        """
        # Generate borrow ID
        if len(self.borrowings) > 0:
            borrow_id = self.borrowings['BorrowID'].max() + 1
        else:
            borrow_id = 1
        
        # Calculate due date (14 days from now)
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        
        # Create new borrowing record
        new_borrowing = {
            'BorrowID': borrow_id,
            'ISBN': isbn,
            'Username': username,
            'BorrowDate': borrow_date,
            'DueDate': due_date,
            'ReturnDate': None,
            'Status': 'Borrowed'
        }
        
        self.borrowings = pd.concat([self.borrowings, pd.DataFrame([new_borrowing])], ignore_index=True)
        self.save()
        
        return True, borrow_id, due_date.strftime("%Y-%m-%d")
    
    def return_book(self, borrow_id):
        """
        Record a book return
        Returns: (success, message)
        """
        if borrow_id not in self.borrowings['BorrowID'].values:
            return False, "Invalid borrow ID!"
        
        # Check if book is already returned
        if self.borrowings.loc[self.borrowings['BorrowID'] == borrow_id, 'Status'].iloc[0] == 'Returned':
            return False, "This book has already been returned!"
        
        # Update borrowing record
        self.borrowings.loc[self.borrowings['BorrowID'] == borrow_id, 'ReturnDate'] = datetime.now()
        self.borrowings.loc[self.borrowings['BorrowID'] == borrow_id, 'Status'] = 'Returned'
        self.save()
        
        return True, "Book returned successfully!"
    
    def get_active_borrowings(self, username=None):
        """Get active borrowings for a user or all users"""
        if username:
            return self.borrowings[(self.borrowings['Username'] == username) & 
                                  (self.borrowings['Status'] == 'Borrowed')]
        else:
            return self.borrowings[self.borrowings['Status'] == 'Borrowed']
    
    def get_user_borrowings(self, username):
        """Get all borrowings for a specific user"""
        return self.borrowings[self.borrowings['Username'] == username]
    
    def get_book_borrowing_status(self, isbn):
        """
        Check if book is currently borrowed
        Returns: (is_borrowed, borrower, due_date)
        """
        active_borrows = self.borrowings[(self.borrowings['ISBN'] == isbn) & 
                                        (self.borrowings['Status'] == 'Borrowed')]
        
        if len(active_borrows) > 0:
            borrow = active_borrows.iloc[0]
            return True, borrow['Username'], borrow['DueDate']
        else:
            return False, None, None
    
    def get_overdue_books(self):
        """Get list of overdue books"""
        today = datetime.now()
        
        overdue = self.borrowings[(self.borrowings['Status'] == 'Borrowed') & 
                                 (self.borrowings['DueDate'] < today)]
        
        return overdue