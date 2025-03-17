import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random

class Book:
    def __init__(self, id, title):
        self.id = id
        self.title = title
    
    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title

class BookKuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BOOK-KU!")
        
        # Make window fullscreen and prevent resizing
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        
        # Configure colors from the image
        self.light_blue = "#b0c4d9"
        self.cream = "#f9f5e3"
        self.beige = "#e8d8b0"
        self.dark_purple = "#2d2d43"
        
        # Configure ttk style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), background=self.beige)
        self.style.map("TButton",
            background=[("active", self.beige), ("pressed", "#d9c99f")],
            relief=[("pressed", "sunken")]
        )
        
        # Configure root with dark purple border
        self.root.configure(bg=self.dark_purple)
        
        # Create main frame with light blue header and cream content area
        self.main_frame = tk.Frame(root, bg=self.dark_purple, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        self.header_frame = tk.Frame(self.main_frame, bg=self.light_blue, height=120)
        self.header_frame.pack(fill=tk.X)
        
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.cream)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar for book display
        self.canvas = tk.Canvas(self.content_frame, bg=self.cream, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create book frame inside the canvas
        self.book_frame = tk.Frame(self.canvas, bg=self.cream)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.book_frame, anchor="nw")
        
        # Configure grid
        for i in range(4):  # 4 columns
            self.book_frame.columnconfigure(i, weight=1)
        
        # Footer frame
        self.footer_frame = tk.Frame(self.main_frame, bg=self.light_blue, height=50)
        self.footer_frame.pack(fill=tk.X)
        
        # Add header content
        self.logo_label = tk.Label(
            self.header_frame,
            text="BOOK-KU!",
            font=("Arial Black", 24, "bold"),
            bg=self.light_blue
        )
        self.logo_label.pack(pady=(10, 0))
        
        # Welcome text
        self.welcome_label = tk.Label(
            self.header_frame,
            text="WELCOME, USER! WHAT WOULD YOU LIKE TO READ TODAY?",
            font=("Arial", 10),
            bg=self.light_blue
        )
        self.welcome_label.pack(pady=(5, 5))
        
        # Search entry with ttk styling
        self.search_frame = tk.Frame(self.header_frame, bg=self.light_blue)
        self.search_frame.pack(pady=(0, 10))
        
        # Use ttk Entry for modern look
        self.style.configure("Search.TEntry", 
                             fieldbackground=self.beige, 
                             borderwidth=0,
                             font=("Arial", 10))
        
        self.search_entry = ttk.Entry(
            self.search_frame,
            width=50,
            style="Search.TEntry",
            justify="center"
        )
        self.search_entry.insert(0, "Search Your Book Here")
        self.search_entry.pack(ipady=5)
        
        # Footer with navigation buttons
        self.button_frame = tk.Frame(self.footer_frame, bg=self.light_blue)
        self.button_frame.pack(pady=10)
        
        # Create custom ttk style for navigation buttons
        self.style.configure("Nav.TButton", 
                            background=self.beige,
                            width=3,
                            padding=(10, 10))
        
        # Library/bookshelf button with ttk
        self.library_button = ttk.Button(
            self.button_frame,
            text="📚",
            style="Nav.TButton"
        )
        self.library_button.pack(side=tk.LEFT, padx=5)
        
        # Home button with ttk
        self.home_button = ttk.Button(
            self.button_frame,
            text="🏠",
            style="Nav.TButton"
        )
        self.home_button.pack(side=tk.LEFT, padx=5)
        
        # Notes/document button with ttk
        self.notes_button = ttk.Button(
            self.button_frame,
            text="📋",
            style="Nav.TButton"
        )
        self.notes_button.pack(side=tk.LEFT, padx=5)
        
        # Bookmark button with ttk
        self.bookmark_button = ttk.Button(
            self.button_frame,
            text="📑",
            style="Nav.TButton"
        )
        self.bookmark_button.pack(side=tk.LEFT, padx=5)
        
        # Add hover effect to buttons
        for button in [self.library_button, self.home_button, self.notes_button, self.bookmark_button]:
            button.bind("<Enter>", lambda e, btn=button: self.on_enter(btn))
            button.bind("<Leave>", lambda e, btn=button: self.on_leave(btn))
        
        # Setup book display
        self.photo_references = {}  # Store references to images
        self.total_books = 12  # Simulate having 12 books
        
        # Bind events for scrolling
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # For Windows and MacOS
        self.canvas.bind("<Button-4>", self.on_mousewheel)  # For Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mousewheel)  # For Linux scroll down
        
        # Display books
        self.display_books()

    def on_enter(self, button):
        """Add hover effect"""
        self.style.map("Nav.TButton",
            background=[("active", "#d9c99f")])
    
    def on_leave(self, button):
        """Remove hover effect"""
        self.style.map("Nav.TButton",
            background=[("active", self.beige)])
    
    def on_canvas_configure(self, event):
        """Update the scroll region when the canvas changes size"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:  # Scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
    
    def on_book_click(self, book):
        """Handle book button click"""
        print(f"Book clicked: {book.get_title()} (ID: {book.get_id()})")
        # Here you would add code to open the book or show details
    
    def load_image(self):
        """Create a placeholder book cover image"""
        # Create a colorful placeholder image
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33F5", "#F5FF33", "#33FFF5"]
        color = random.choice(colors)
        
        # Create a blank image with the chosen color
        img = Image.new('RGB', (100, 150), color)
        
        # Convert to PhotoImage for Tkinter
        photo = ImageTk.PhotoImage(img)
        return photo
    
    def display_books(self):
        """Display books in a grid layout"""
        cek = True
        i = 0
        count = 0
        # Implementation of algorithm as requested
        while cek:
            for j in range(4):  # 4 columns
                if count < self.total_books:
                    book_id = count + 1
                    book = Book(book_id, f"Buku #{book_id}")
                    self.create_book_button(book, i, j)
                    count += 1
                else:
                    cek = False
                    break
            i += 1

    def create_book_button(self, book, row, col):
        """Create a button for each book with cover image"""
        # Frame for each book
        book_frame = tk.Frame(self.book_frame, padx=5, pady=5, bg=self.cream)
        book_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        # Load image cover (use the same image for all books)
        photo = self.load_image()
        self.photo_references[book.get_id()] = photo
        
        # Button with cover image
        btn = tk.Button(
            book_frame, 
            image=photo, 
            text=book.get_title(),
            compound=tk.BOTTOM,
            width=110,
            height=180,
            wraplength=100,
            bg=self.cream,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        btn.pack(fill=tk.BOTH, expand=True)
        
        # Add handler
        btn.configure(command=lambda b=book: self.on_book_click(b))
        
        # Binding scroll on button too
        btn.bind("<MouseWheel>", self.on_mousewheel)
        btn.bind("<Button-4>", self.on_mousewheel)
        btn.bind("<Button-5>", self.on_mousewheel)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookKuApp(root)
    
    # Add escape key binding to exit fullscreen mode
    root.bind("<Escape>", lambda event: root.destroy())
    
    root.mainloop()