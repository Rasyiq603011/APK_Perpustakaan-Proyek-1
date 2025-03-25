import tkinter as tk
from tkinter import messagebox
import os
import json
from PIL import Image, ImageTk

# Import all frames and modules
from constans import *
from Moduls.Book_Manager import BookManager
from UI.DaftarBukuFrame import DataBookFrame
from UI.DetailsBookFrame import DetailsBookFrame
from UI.UpdateBookFrame import UpdateBookFrame
from UI.AddBookFrame import AddBookFrame
from UI.MyBookFrame import MyBookFrame
from UI.LoginFrame import LoginFrame
from UI.HomeFrame import HomeFrame
# from UI.PenaltyBookFrame import PenaltyBookFrame


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Book-Ku")
        self.root.geometry("1024x768")
        self.currentFrame = None
        
        self.setupDirectories()
        self.bookManager = BookManager(
            os.path.join(self.data_dir, "data_buku_2.xlsx"),
            os.path.join(self.assets_dir, "Cover"),
            os.path.join(self.assets_dir, "IMG.jpg")
        )
        self.color= None
        self.selectedBook = None
        self.current_user = None
        self.createWidgets()
        
    
    def setupDirectories(self):
        # Base directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Data directory
        self.data_dir = os.path.join(self.base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Assets directory
        self.assets_dir = os.path.join(self.base_dir, "assets")
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Covers directory
        self.covers_dir = os.path.join(self.assets_dir, "Cover")
        os.makedirs(self.covers_dir, exist_ok=True)

        self.defaultCover = os.path.join(self.assets_dir, "IMG.jpg")
        
        # Create required files if they don't exist
        required_files = [
            ("users.json", {"admin@bookku.com": {"name": "Administrator","password": "admin123","role": "admin"},}),
            ("logs.json", []),
            ("loans.json", []),
            ("bookings.json", []),
            ("penalties.json", [])
        ]
        
        for filename, default_content in required_files:
            file_path = os.path.join(self.data_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_content, f, indent=2)

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
            "MyBookFrame": MyBookFrame,
            "LoginFrame" : LoginFrame,
            "HomeFrame" : HomeFrame,
            # "PenaltyBookFrame": PenaltyBookFrame,    
        }

        self.setupFrames()
        self.showFrame("LoginFrame")  # Start with book list

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
            if frameName == "UpdateBookFrame":
                frame.book = self.selectedBook
                if hasattr(frame, "load_book_data"):
                    frame.load_book_data()
            
            # For DataBookFrame, refresh the book grid
            if frameName == "DataBookFrame":
                if hasattr(frame, "populate_book_grid"):
                    frame.populate_book_grid()

            if frameName == "HomeFrame":
                OldFrame = self.frames["HomeFrame"]
                OldFrame.destroy()
                print(self.current_user)
                Newframe = HomeFrame(self.container, self)
                Newframe.grid(row=0, column=0, sticky="nsew")
                frame = Newframe
            
            frame.tkraise()
            self.currentFrame = frameName

    def GetStatusUser(self):
        pass
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

