import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
from tkinter import messagebox
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Moduls.Book_Manager import BookManager as L
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constans import COLOR_DARK, COLOR_LIGHT 

class DetailsBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background
        self.is_dark_mode = True
        self.color = COLOR_DARK if self.is_dark_mode else COLOR_LIGHT
        self.controller = controller

        self.StatusUser = self.controller.GetStatusUser()
        self.selectedBook = self.controller.selectedBook
        self.defaultCover = self.controller.defaultCover
        self.dataDir = self.controller.data_dir
        
        # Main frame layout - Optimized for 1024x768
        self.columnconfigure(0, weight=3)  # Detail content
        self.columnconfigure(1, weight=2)  # Cover image
        self.rowconfigure(0, weight=0)  # Header row - fixed height
        self.rowconfigure(1, weight=1)  # Content row - expands
        self.rowconfigure(2, weight=0)  # Footer row - fixed height
        
        self.CreateLayout()


    def CreateLayout(self):
        self.Header()
        self.Content()
        self.Footer()

    def Header(self):
       # ===== HEADER SECTION =====
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 0))
        self.header_frame.columnconfigure(0, weight=1)  # Back button
        self.header_frame.columnconfigure(1, weight=2)  # Title
        self.header_frame.columnconfigure(2, weight=1)  # empty (saran radit)
            
            # Back button - made slightly more compact
        self.back_btn = ctk.CTkButton(
                self.header_frame, 
                text="← Kembali", 
                command=lambda: self.controller.showFrame("DataBookFrame"),
                fg_color=self.color["primary"],
                hover_color= self.color["primaryText"],
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
                corner_radius=15,
                width=120,
                height=30
        )
        self.back_btn.grid(row=0, column=0, sticky="w", padx=10)
            
            # Title - same size but centered better
        self.title_label = ctk.CTkLabel(
                self.header_frame,
                text="DETAIL BUKU", 
                font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
                text_color=self.color["primaryText"]
        )
        self.title_label.grid(row=0, column=1)
        
    def Content(self):
        # ===== CONTENT SECTION =====
        # Info container (left side)
        self.info_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Slightly lighter background for info
        self.info_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        # Initialize info frame - will be populated in update_book_details
        self.info_frame = ctk.CTkFrame(self.info_container, fg_color="transparent")
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cover container (right side)
        self.cover_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Matching info container color
        self.cover_container.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        self.setup_cover_section()
        self.update_book_details()
        
    def Footer(self):
        # ===== FOOTER SECTION =====
        self.footer = ctk.CTkFrame(self, fg_color="transparent", height=60, corner_radius=10)
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        self.footer.pack_propagate(False)
            
        self.editBtn = ctk.CTkButton(
                self.footer,
                text="Back Home",
                command=lambda: self.controller.showFrame("UpdateBookFrame"),
                fg_color=self.color["primary"],
                hover_color=self.color["hover"]["primary"],
                text_color=self.color["primaryText"],
                font=ctk.CTkFont(family="Arial", size=14),
                corner_radius=10,
                height=40,
                width=120
            )
        self.editBtn.pack(side="left", padx=40, pady=10)
        
        if self.StatusUser == "Administrator":
            self.editBtn.configure(command=lambda: self.controller.showFrame("UpdateBookFrame"), text = "Edit Buku")
        
            # Update button - Right side
        self.borrow_btn = ctk.CTkButton(
                self.footer,
                text="Borrow", 
                command=self.borrow_book,
                fg_color=self.color["success"], 
                hover_color=self.color["active"]["accent"],
                text_color=self.color["primaryText"],
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                corner_radius=10,
                height=40,
                width=150
            )
        self.borrow_btn.pack(side="right", padx=40, pady=10)
        
        self.update_borrow_button()
        if self.selectedBook is not None:
            self.update_book_details()

    def setup_cover_section(self):
        self.cover_container.columnconfigure(0, weight=1)
        self.cover_container.rowconfigure(0, weight=0)  # Label
        self.cover_container.rowconfigure(1, weight=1)  # Cover image
        self.cover_container.rowconfigure(2, weight=0)  # Info
        
        # Cover title
        cover_title = ctk.CTkLabel(
            self.cover_container,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        cover_title.pack(pady =(30,40))
        
        # Cover image frame - Light background like in React design
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color=self.color["background"], corner_radius=10)  # Light background for cover like in design
        self.cover_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Cover image label - using the recommended 180x270 ratio
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=20, pady=20)
        
        # Book status info
        status_frame = ctk.CTkFrame(self.cover_container, fg_color="#363636", corner_radius=5)  # Slightly darker info frame
        status_frame.pack(padx=20, pady=(40,60))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Status: Tersedia",  # Default status, will be updated
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#FFFFFF",
            justify="center"
        )
        self.status_label.pack(pady=8, padx=10)

    def borrow_book(self):
        if self.selectedBook is None:
            messagebox.showerror("Error", "No book selected or book data is missing!")
            return
            
        if hasattr(self.controller, 'borrowBook'):
            self.controller.borrowBook(self.selectedBook)

    def update_borrow_button(self):
        if self.selectedBook is None:
            return
        
        status = self.selectedBook.get('Status', 'Unknown')
        
        if status == "Available":
            self.borrow_btn.configure(
                text="Borrow Book",
                fg_color="#4CAF50",
                hover_color="#388E3C",
                command=self.borrow_book,
                state="normal"
            )
        elif status == "Booked":
            self.borrow_btn.configure(
                text="Book Already Reserved",
                fg_color="#FF6D00",
                hover_color="#E65100",
                state="disabled"
            )
        else:  # Borrowed or other status
            self.borrow_btn.configure(
                text="Book Now",
                fg_color="#FF6D00",
                hover_color="#E65100",
                command=self.book_now,
                state="normal"
            )

    def book_now(self):
        pass
    def update_book_details(self):
        if self.selectedBook is None:
            return
            
        # Clear existing content in info frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        # Load book cover image
        size = (180, 270)
        isbn = str(self.selectedBook.get('ISBN', ''))
        img_path = os.path.join(self.dataDir, f"{isbn}.jpeg")

        if not os.path.exists(img_path) or not isbn:
            img_path = self.defaultCover
            
        try:
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.cover_label.configure(image=photo_img)
            self.cover_label.image = photo_img
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Update status
        status = self.selectedBook.get('Status', 'Available')
        status_color = self.color["success"] if status == "Available" else self.color["error"]  # Green if available, red otherwise
        self.status_label.configure(text=f"Status: {status}", text_color=status_color)
            

        # Book details in grid layout
        details_grid = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        details_grid.pack(fill="both")
        
        # Configure grid
        details_grid.columnconfigure(0, weight=0)
        details_grid.columnconfigure(1, weight=1)  
        details_grid.columnconfigure(2, weight=0)  
        details_grid.columnconfigure(3, weight=1)  
        
        # Info fields (first group in a grid)
        fields = [
            ("Judul", 0, 0),
            ("Penulis", 1, 0),
            ("Penerbit", 1, 2),
            ("Tahun", 2, 0),
            ("Kategori", 2, 2),
            ("Halaman", 3, 0),
            ("ISBN", 3, 2)
        ]

        for field in fields:
            field_name, row, col = field

            if field_name == "Judul":
                parent = details_grid.winfo_width()
                value = ctk.CTkLabel(
                    details_grid,
                    text=self.selectedBook.get(field_name, ""),
                    font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                    text_color="white",
                    anchor="w",
                    wraplength=int(parent * 0.9),  
                    justify="left"
                )
                value.grid(row=row, column=col, columnspan = 4,padx=(0, 10), pady=8, sticky="w")

            else:
                # Label
                label = ctk.CTkLabel(
                    details_grid,
                    text=f"{field_name}:",
                    font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                    text_color=self.color["primaryText"],
                    anchor="w",
                    width=70  # Reduced width
                )
                label.grid(row=row, column=col, padx=(0,20), pady=15, sticky="w")
                
                
                # Value
                value = ctk.CTkLabel(
                    details_grid,
                    text=self.selectedBook.get(field_name, ""),
                    font=ctk.CTkFont(family="Arial", size=14),
                    text_color="white",
                    anchor="w"
                )
                value.grid(row=row, column=col+1, padx=(0, 10), pady=8, sticky="w")

        # Description section
        if 'Deskripsi' in self.selectedBook and str(self.selectedBook['Deskripsi']) != 'nan':
            desc_title = ctk.CTkLabel(
                self.info_frame,
                text="Deskripsi:",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white",
                anchor="w"
            )
            desc_title.pack(anchor="w", pady=(20, 5))
            
            # Description textbox with scrollbar
            desc_textbox = ctk.CTkTextbox(
                self.info_frame,
                height=150,
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                wrap="word",
                fg_color="#3D3D3D",  # Lighter background for textarea
                border_color="#666666",  # Matching border color
                corner_radius=8,
                border_width=1,
                activate_scrollbars=True
            )
            desc_textbox.pack(fill="both", expand=True, pady=(0, 10))
            
            desc_textbox.insert("1.0", str(self.selectedBook['Deskripsi']))
            desc_textbox.configure(state="disabled")
            desc_textbox.see("1.0")


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Detail Buku")
    root.geometry("1024x768")
    
    # For testing, make a simple controller class
    class TestController:
        def __init__(self):
            self.selectedBook = None
            self.setupDirectories()
        def setupDirectories(self):
        # Base directory
            self.base_dir = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__))))
            
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
        def show_frame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def showFrame(self, frame_name):
            print(f"Would show frame (camelCase): {frame_name}")
        
        def borrowBook(self, book):
            print(f"Would borrow book: {book.get('Judul', 'Unknown')}")

        def GetStatusUser(self):
            return "Administrator"
    
    # Sample book data for testing
    test_controller = TestController()
    test_controller.selectedBook = {
        'Judul': 'Laskar Pelangi Laskar Pelangi Laskar Pelangi Laskar Pelangi Laskar Pelangi',
        'Penulis': 'Andrea Hirata',
        'Penerbit': 'Bentang Pustaka',
        'Tahun': '2005',
        'Kategori': 'Novel',
        'ISBN': '9789793062792',
        'Halaman': '529',
        'Status': 'Booked',
        'Deskripsi': 'Novel ini bercerita tentang kehidupan 10 anak dari keluarga miskin yang bersekolah di sebuah sekolah Muhammadiyah di Belitung yang penuh dengan keterbatasan. Meskipun sekolah itu sangat sederhana, mereka menjadikan masa kanak-kanak mereka yang bahagia, dan Ikal menjadi penulis buku bertaraf internasional.'
    }
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = DetailsBookFrame(frame, test_controller)
    app.pack(expand=True, fill="both")
    
    root.mainloop()
