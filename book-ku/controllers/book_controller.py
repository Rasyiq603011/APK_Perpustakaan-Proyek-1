from models.book_model import BookModel

class BookController:
    """
    Controller for handling book-related operations
    """
    def __init__(self, book_model=None):
        """Initialize controller with book model"""
        self.book_model = book_model if book_model else BookModel()
    
    def get_all_books(self):
        """Get all books"""
        return self.book_model.get_all_books()
    
    def get_book_by_isbn(self, isbn):
        """Get book by ISBN"""
        return self.book_model.get_book_by_isbn(isbn)
    
    def search_books(self, query, field="all"):
        """Search books by query in specified field"""
        return self.book_model.search_books(query, field)
    
    def add_book(self, isbn, title, author, publisher, year, category, pages, description, image=None):
        """
        Add a new book
        Returns: (success, message)
        """
        # Validate inputs
        if not isbn or not title or not author or not publisher or not year:
            return False, "ISBN, title, author, publisher, and year are required!"
        
        try:
            year = int(year)
            pages = int(pages)
        except ValueError:
            return False, "Year and pages must be numbers!"
        
        # Add book
        success = self.book_model.add_book(
            ISBN=isbn,
            Judul=title,
            Penulis=author,
            Penerbit=publisher,
            Tahun=year,
            Kategori=category,
            Halaman=pages,
            Deskripsi=description,
            Image=image
        )
        
        if success:
            self.book_model.save()
            return True, f"Book '{title}' added successfully!"
        else:
            return False, f"Book with ISBN '{isbn}' already exists!"
    
    def update_book(self, isbn, **kwargs):
        """
        Update book details
        Returns: (success, message)
        """
        book = self.book_model.get_book_by_isbn(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found!"
        
        success = self.book_model.update_book(isbn, **kwargs)
        
        if success:
            self.book_model.save()
            return True, "Book updated successfully!"
        else:
            return False, "Failed to update book!"
    
    def delete_book(self, isbn):
        """
        Delete a book
        Returns: (success, message)
        """
        book = self.book_model.get_book_by_isbn(isbn)
        if not book:
            return False, f"Book with ISBN '{isbn}' not found!"
        
        success = self.book_model.delete_book(isbn)
        
        if success:
            self.book_model.save()
            return True, f"Book '{book['Judul']}' deleted successfully!"
        else:
            return False, "Failed to delete book!"
    
    def get_categories(self):
        """Get list of book categories"""
        return self.book_model.get_categories()
    
    def get_authors(self):
        """Get list of authors"""
        return self.book_model.get_authors()
    
    def get_publishers(self):
        """Get list of publishers"""
        return self.book_model.get_publishers()
