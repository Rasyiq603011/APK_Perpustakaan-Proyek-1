import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

# Import all frames and modules
from MyLibrary.constans import *
from MyLibrary.Moduls.Book_Manager import BookManager
from MyLibrary.UI.DaftarBukuFrame import DataBookFrame
from MyLibrary.UI.DetailsBookFrame import DetailsBookFrame
from MyLibrary.UI.UpdateBookFrame import UpdateBookFrame
from MyLibrary.UI.AddBookFrame import AddBookFrame


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Book-Ku")
        self.root.geometry("1024x768")
        self.currentFrame = None
        self.dataDir = "D:\\Project 1\\Tubes Semester 1\\Asset"
        self.bookManager = BookManager(
            os.path.join(self.dataDir, "data_buku_2.xlsx"),
            os.path.join(self.dataDir, "Cover"),
            os.path.join(self.dataDir, "IMG.jpg")
        )
        self.selectedBook = None
        self.createWidgets()
    
    def createWidgets(self):
        # Create the container frame
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Register all frame classes - include DataBookFrame
        self.frameClasses = {
            "DataBookFrame": DataBookFrame,  # Changed from DaftarBukuFrame for consistency
            "DetailsBookFrame": DetailsBookFrame,
            "UpdateBookFrame": UpdateBookFrame,
            "AddBookFrame": AddBookFrame,
        }

        self.setupFrames()
        self.showFrame("DataBookFrame")  # Start with book list

    def setupFrames(self):
        for name, FrameClass in self.frameClasses.items():
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def showFrame(self, frameName):
        """Show the specified frame and update it if needed"""
        if frameName in self.frames:
            frame = self.frames[frameName]
            
            # Update frame content if needed
            if frameName == "DetailsBookFrame":
                # Pass the selected book to the frame
                frame.selectedBook = self.selectedBook
                if hasattr(frame, "update_book_details"):
                    frame.update_book_details()
            
            # For UpdateBookFrame, pass the book data
            elif frameName == "UpdateBookFrame":
                frame.book = self.selectedBook
                if hasattr(frame, "load_book_data"):
                    frame.load_book_data()
            
            # For DataBookFrame, refresh the book grid
            elif frameName == "DataBookFrame":
                if hasattr(frame, "populate_book_grid"):
                    frame.populate_book_grid(frame)
            
            frame.tkraise()
            self.currentFrame = frameName

    
    def showBookDetail(self, book):
        """Show details of the selected book"""
        self.selectedBook = book
        self.showFrame("DetailsBookFrame")
    
    def saveBook(self, bookData):
        if hasattr(self.bookManager, "addBook"):
            result = self.bookManager.addBook(bookData)
            if result:
                messagebox.showinfo("Success", "Buku berhasil ditambahkan!")
                self.showFrame("DataBookFrame")
            return result
        return False
    
    def updateBook(self, book):
        """Update an existing book"""
        if hasattr(self.bookManager, "UpdateBook"):
            result = self.bookManager.UpdateBook(book)
            if result:
                messagebox.showinfo("Success", "Buku berhasil diperbarui!")
                # Update selectedBook with the new data
                self.selectedBook = book
                self.showFrame("DetailsBookFrame")
            return result
        return False
        
    def borrowBook(self, book):
        """Handle book borrowing functionality"""
        if book is None:
            messagebox.showerror("Error", "No book selected!")
            return False
            
        # Create a dictionary from the Series to avoid pandas Series issues
        if hasattr(book, 'to_dict'):
            book_copy = book.to_dict()
        else:
            book_copy = dict(book)
        
        # Change status to "Dipinjam"
        book_copy["Status"] = "Dipinjam"
        
        # Update the book in the database
        if hasattr(self.bookManager, "UpdateBook"):
            result = self.bookManager.UpdateBook(book_copy)
            if result:
                messagebox.showinfo("Success", f"Buku '{book_copy['Judul']}' berhasil dipinjam!")
                # Update the selectedBook with the new data
                if hasattr(self.bookManager, "getBookByIndeks"):
                    # Get the fresh data from the manager
                    # This assumes you have a way to get a book by ISBN in your manager
                    for idx, row in self.bookManager.getBook().iterrows():
                        if row['ISBN'] == book_copy['ISBN']:
                            self.selectedBook = row
                            break
                
                # Update the book details display
                if "DetailsBookFrame" in self.frames:
                    self.frames["DetailsBookFrame"].selectedBook = self.selectedBook
                    if hasattr(self.frames["DetailsBookFrame"], "update_book_details"):
                        self.frames["DetailsBookFrame"].update_book_details()
            return result
        return False
    
    def getBook(self):
        if hasattr(self.bookManager, "getBook"):
            return self.bookManager.getBook()
        return None
    
    def ISBNexists(self, isbn):
        if hasattr(self.bookManager, "ISBNexists"):
            return self.bookManager.ISBNexists(isbn)
        return False
    
    def loadCover(self, isbn):
        if hasattr(self.bookManager, "LoadCover"):
            return self.bookManager.LoadCover(isbn)
        return None

