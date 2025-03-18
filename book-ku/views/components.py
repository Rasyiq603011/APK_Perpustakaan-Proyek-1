import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Constants
PURPLE_COLOR = "#4C0086"  # Purple background
GREEN_COLOR = "#00FF11"   # Green for input fields
WHITE_COLOR = "#FFFFFF"   # White for text

class UIComponents:
    """Class containing reusable UI components for the application"""
    
    @staticmethod
    def create_header(parent, title="BOOK-KU!", welcome_text="Welcome, User! What would you like to read today?"):
        """Create header with logo, title and welcome text"""
        frame_head = tk.Frame(parent, bg=PURPLE_COLOR, pady=10)
        frame_head.pack(fill="x")
        
        # Configure rows
        frame_head.rowconfigure([0, 1], weight=1)
        frame_head.columnconfigure(0, weight=1)
        
        # Title with book emoji
        title_label = tk.Label(
            frame_head, 
            text=f"📖 {title}", 
            font=("Comic Sans MS", 40, "bold"), 
            fg="black", 
            bg=PURPLE_COLOR
        )
        title_label.grid(row=0, column=0, sticky="nsew")
        
        # Welcome text
        welcome_label = tk.Label(
            frame_head, 
            text=welcome_text,
            font=("Arial", 14), 
            fg="black", 
            bg=PURPLE_COLOR
        )
        welcome_label.grid(row=1, column=0, sticky="nsew")
        
        return frame_head
    
    @staticmethod
    def create_search_bar(parent, placeholder="Search Your Book Here", command=None):
        """Create search bar with placeholder text"""
        search_frame = tk.Frame(parent, bg=PURPLE_COLOR, pady=10)
        search_frame.pack(fill="x", padx=200)
        search_frame.columnconfigure(0, weight=1)
        
        search_entry = tk.Entry(
            search_frame, 
            font=("Arial", 16), 
            bg=GREEN_COLOR, 
            fg="grey", 
            justify="center",
            relief="flat"
        )
        search_entry.insert(0, placeholder)
        search_entry.pack(fill="x", ipady=8)
        
        def on_focus_in(event):
            if search_entry.get() == placeholder:
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")
        
        def on_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, placeholder)
                search_entry.config(fg="grey")
        
        def on_return(event):
            if command and search_entry.get() != placeholder:
                command(search_entry.get())
        
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.bind("<Return>", on_return)
        
        return search_entry
    
    @staticmethod
    def create_scrollable_frame(parent, bg_color="white"):
        """Create a scrollable frame"""
        # Main frame
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg=bg_color)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Place the scrollable frame in the canvas
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas to fill width
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width=canvas_width)
        
        canvas.bind("<Configure>", configure_canvas)
        
        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Pack canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        return scrollable_frame, canvas
    
    @staticmethod
    def create_book_grid(parent, books, command=None, cols=5):
        """Create a grid of book thumbnails"""
        # Container for grid
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Configure grid columns
        for i in range(cols):
            grid_frame.columnconfigure(i, weight=1)
        
        # Load default book image
        try:
            if os.path.exists("assets/images/default.jpg"):
                default_img = Image.open("assets/images/default.jpg")
            else:
                # Create a blank image if default not found
                default_img = Image.new('RGB', (100, 150), color = (200, 200, 200))
        except Exception as e:
            print(f"Error loading default image: {e}")
            default_img = Image.new('RGB', (100, 150), color = (200, 200, 200))
        
        default_img = default_img.resize((100, 150))
        default_photo = ImageTk.PhotoImage(default_img)
        
        # Create book items
        row, col = 0, 0
        for index, book in enumerate(books.iterrows()):
            book = book[1]  # Get the data from the row
            
            # Frame for book
            book_frame = tk.Frame(grid_frame, bg="white", bd=1, relief="solid", padx=5, pady=5)
            book_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Try to load book image
            try:
                if os.path.exists(f"assets/images/{book['Image']}"):
                    img = Image.open(f"assets/images/{book['Image']}")
                    img = img.resize((100, 150))
                    photo = ImageTk.PhotoImage(img)
                else:
                    photo = default_photo
            except:
                photo = default_photo
            
            # Button with image
            img_btn = tk.Button(
                book_frame,
                image=photo,
                bg="white",
                bd=0,
                command=lambda isbn=book['ISBN']: command(isbn) if command else None
            )
            img_btn.image = photo  # Keep reference to prevent garbage collection
            img_btn.pack(padx=5, pady=5)
            
            # Book title label
            title_label = tk.Label(
                book_frame, 
                text=book['Judul'],
                font=("Arial", 10),
                bg="white",
                wraplength=120
            )
            title_label.pack(padx=5, pady=5)
            
            # Increment grid position
            col += 1
            if col >= cols:
                col = 0
                row += 1
        
        return grid_frame
    
    @staticmethod
    def create_footer(parent):
        """Create footer with navigation buttons"""
        footer_frame = tk.Frame(parent, bg=PURPLE_COLOR, height=80)
        footer_frame.pack(fill="x", side="bottom")
        
        # Make buttons stay at fixed positions
        footer_frame.pack_propagate(False)
        
        # Center container for buttons
        button_frame = tk.Frame(footer_frame, bg=PURPLE_COLOR)
        button_frame.pack(expand=True)
        
        # Profile button
        profile_btn = tk.Button(
            button_frame,
            text="👤",
            bg=PURPLE_COLOR,
            fg="black",
            font=("Arial", 20),
            bd=0,
            padx=20,
            activebackground=PURPLE_COLOR
        )
        profile_btn.pack(side="left", padx=20)
        
        # Library button
        library_btn = tk.Button(
            button_frame,
            text="📚",
            bg=GREEN_COLOR,
            fg="black",
            font=("Arial", 20),
            bd=0,
            padx=20,
            activebackground=GREEN_COLOR
        )
        library_btn.pack(side="left", padx=20)
        
        # Home button
        home_btn = tk.Button(
            button_frame,
            text="🏠",
            bg=GREEN_COLOR,
            fg="black",
            font=("Arial", 20),
            bd=0,
            padx=20,
            activebackground=GREEN_COLOR
        )
        home_btn.pack(side="left", padx=20)
        
        # Notifications button
        notif_btn = tk.Button(
            button_frame,
            text="📝",
            bg=GREEN_COLOR,
            fg="black",
            font=("Arial", 20),
            bd=0,
            padx=20,
            activebackground=GREEN_COLOR
        )
        notif_btn.pack(side="left", padx=20)
        
        # Logout button
        logout_btn = tk.Button(
            button_frame,
            text="🚪",
            bg=PURPLE_COLOR,
            fg="black",
            font=("Arial", 20),
            bd=0,
            padx=20,
            activebackground=PURPLE_COLOR
        )
        logout_btn.pack(side="left", padx=20)
        
        return {
            "profile": profile_btn,
            "library": library_btn,
            "home": home_btn,
            "notifications": notif_btn,
            "logout": logout_btn
        }
    
    @staticmethod
    def create_back_button(parent, command=None):
        """Create a back button"""
        back_btn = tk.Button(
            parent,
            text="←",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black",
            bd=0,
            padx=20,
            command=command
        )
        back_btn.pack(side="left", anchor="nw", padx=10, pady=10)
        return back_btn
    
    @staticmethod
    def create_entry_field(parent, placeholder, show=None):
        """Create entry field with placeholder text"""
        entry = tk.Entry(
            parent,
            font=("Arial", 16),
            bg=GREEN_COLOR,
            fg="grey",
            bd=0,
            justify="center",
            insertbackground="black",
            width=40
        )
        entry.insert(0, placeholder)
        entry.placeholder_active = True
        
        def on_focus_in(event):
            if entry.placeholder_active:
                entry.delete(0, tk.END)
                if show:
                    entry.config(show=show)
                entry.config(fg="black")
                entry.placeholder_active = False
        
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                if show:
                    entry.config(show="")
                entry.config(fg="grey")
                entry.placeholder_active = True
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry
    
    @staticmethod
    def create_button(parent, text, command=None, width=10, height=1, font=("Arial", 12), bg=PURPLE_COLOR, fg="white"):
        """Create a styled button"""
        button = tk.Button(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            relief="raised",
            command=command,
            width=width,
            height=height,
            bd=5,
            cursor="hand2"
        )
        return button
