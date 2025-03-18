import pandas as pd
import os
from datetime import datetime, timedelta

class BookModel:
    """
    Model for managing book data and operations.
    """
    def __init__(self, file_path="data/data_buku.xlsx"):
        """Initialize the book model with data from Excel file"""
        self.file_path = file_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if os.path.exists(file_path):
            self.books = pd.read_excel(file_path)
        else:
            # Create empty DataFrame with required columns
            self.books = pd.DataFrame(columns=[
                'ISBN', 'Judul', 'Penulis', 'Penerbit', 'Tahun', 
                'Kategori', 'Halaman', 'Deskripsi', 'Status', 'Image'
            ])
            
            # Add some sample data if file doesn't exist
            self._add_sample_data()
            self.save()
    
    def _add_sample_data(self):
        """Add sample books data"""
        sample_books = [
            {
                'ISBN': '9780747532743', 
                'Judul': 'Harry Potter and the Philosopher\'s Stone', 
                'Penulis': 'J.K. Rowling',
                'Penerbit': 'Bloomsbury', 
                'Tahun': 1997, 
                'Kategori': 'Fantasy', 
                'Halaman': 223,
                'Deskripsi': 'Harry Potter, an orphaned boy, discovers he is a wizard and begins his education at Hogwarts School of Witchcraft and Wizardry.',
                'Status': 'Available',
                'Image': 'harry_potter.jpg'
            },
            {
                'ISBN': '9780061120084', 
                'Judul': 'To Kill a Mockingbird', 
                'Penulis': 'Harper Lee',
                'Penerbit': 'J. B. Lippincott & Co.', 
                'Tahun': 1960, 
                'Kategori': 'Fiction', 
                'Halaman': 281,
                'Deskripsi': 'The story of the trial of Tom Robinson, a Black man wrongly accused of raping a white woman, as seen through the eyes of Scout Finch.',
                'Status': 'Available',
                'Image': 'mockingbird.jpg'
            },
            {
                'ISBN': '9780451524935', 
                'Judul': '1984', 
                'Penulis': 'George Orwell',
                'Penerbit': 'Secker & Warburg', 
                'Tahun': 1949, 
                'Kategori': 'Dystopian', 
                'Halaman': 328,
                'Deskripsi': 'A dystopian novel set in Airstrip One, formerly Great Britain, a province of the superstate Oceania.',
                'Status': 'Available',
                'Image': '1984.jpg'
            }
        ]
        
        for book in sample_books:
            self.add_book(**book)
    
    def save(self):
        """Save book data to Excel file"""
        self.books.to_excel(self.file_path, index=False)
        return True
    
    def get_all_books(self):
        """Return all books"""
        return self.books
    
    def get_book_by_isbn(self, isbn):
        """Get a book by ISBN"""
        if isbn not in self.books['ISBN'].values:
            return None
        
        return self.books[self.books['ISBN'] == isbn].iloc[0].to_dict()
    
    def search_books(self, query, field="all"):
        """
        Search books by query. If field is "all", search in all text fields.
        Otherwise, search in the specified field.
        """
        query = str(query).lower()
        
        if field == "all":
            # Search in all text fields
            text_fields = ['ISBN', 'Judul', 'Penulis', 'Penerbit', 'Kategori', 'Deskripsi']
            mask = False
            
            for col in text_fields:
                if col in self.books.columns:
                    mask = mask | self.books[col].astype(str).str.contains(query, case=False, na=False)
            
            result = self.books[mask]
        elif field in self.books.columns:
            # Search in specific field
            result = self.books[self.books[field].astype(str).str.contains(query, case=False, na=False)]
        else:
            return pd.DataFrame()  # Return empty DataFrame if field is invalid
        
        return result
    
    def add_book(self, ISBN, Judul, Penulis, Penerbit, Tahun, Kategori, Halaman, Deskripsi, Status="Available", Image=None):
        """Add a new book"""
        if ISBN in self.books['ISBN'].values:
            return False  # Book with this ISBN already exists
        
        new_book = {
            'ISBN': ISBN,
            'Judul': Judul,
            'Penulis': Penulis,
            'Penerbit': Penerbit,
            'Tahun': int(Tahun),
            'Kategori': Kategori,
            'Halaman': int(Halaman),
            'Deskripsi': Deskripsi,
            'Status': Status,
            'Image': Image if Image else 'default.jpg'
        }
        
        self.books = pd.concat([self.books, pd.DataFrame([new_book])], ignore_index=True)
        return True
    
    def update_book(self, isbn, **kwargs):
        """Update book details by ISBN"""
        if isbn not in self.books['ISBN'].values:
            return False
        
        # Only update fields that are in the book DataFrame
        valid_fields = [field for field in kwargs.keys() if field in self.books.columns]
        
        for field in valid_fields:
            self.books.loc[self.books['ISBN'] == isbn, field] = kwargs[field]
        
        return True
    
    def delete_book(self, isbn):
        """Delete a book by ISBN"""
        if isbn not in self.books['ISBN'].values:
            return False
        
        self.books = self.books[self.books['ISBN'] != isbn].reset_index(drop=True)
        return True
    
    def get_categories(self):
        """Get list of unique categories"""
        if 'Kategori' in self.books.columns:
            return self.books['Kategori'].unique().tolist()
        return []
    
    def get_authors(self):
        """Get list of unique authors"""
        if 'Penulis' in self.books.columns:
            return self.books['Penulis'].unique().tolist()
        return []
    
    def get_publishers(self):
        """Get list of unique publishers"""
        if 'Penerbit' in self.books.columns:
            return self.books['Penerbit'].unique().tolist()
        return []
    
    def change_book_status(self, isbn, status):
        """Change the status of a book (Available/Borrowed)"""
        if isbn not in self.books['ISBN'].values:
            return False
        
        self.books.loc[self.books['ISBN'] == isbn, 'Status'] = status
        return True
