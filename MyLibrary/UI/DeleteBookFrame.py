import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import shutil
from PIL import Image, ImageTk

class AddBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        self.controller = controller
        self.default_cover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.cover_dir = "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover"
        self.temp_cover_path = None  # Path to temporarily selected cover
        
        # Ensure cover directory exists
        os.makedirs(self.cover_dir, exist_ok=True)
        
        # Main content container
        self.main_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header with back button
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=10)
        
        self.back_btn = ctk.CTkButton(
            self.header_frame, 
            text="← Kembali", 
            command=self.go_back,
            fg_color="#4C0086",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            corner_radius=15,
            width=150,
            height=35
        )
        self.back_btn.pack(side="left", padx=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="TAMBAH BUKU BARU",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)
        
        # Form container
        self.form_container = ctk.CTkFrame(self.main_frame, fg_color="#2D2D2D", corner_radius=10)
        self.form_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Create two columns
        self.left_column = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.left_column.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.right_column = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.right_column.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Left column - Text fields
        self.create_form_fields()
        
        # Right column - Cover selection and preview
        self.create_cover_section()
        
        # Button container
        self.button_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_container.pack(fill="x", pady=20)
        
        # Save button
        self.save_btn = ctk.CTkButton(
            self.button_container,
            text="Simpan Buku",
            command=self.save_book,
            fg_color="#00CC00",
            hover_color="#00AA00",
            text_color="black",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=200
        )
        self.save_btn.pack(side="right", padx=20)
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.button_container,
            text="Batal",
            command=self.go_back,
            fg_color="#FF6B6B",
            hover_color="#FF5555",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=120
        )
        self.cancel_btn.pack(side="right", padx=20)
        
        # Clear the form
        self.clear_form()
    
    def create_form_fields(self):
        # Define fields with their labels
        fields = [
            ("Judul", "title"),
            ("Penulis", "author"),
            ("Penerbit", "publisher"),
            ("Tahun", "year"),
            ("Kategori", "category"),
            ("ISBN", "isbn"),
            ("Halaman", "pages"),
        ]
        
        # Create entry fields
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            frame = ctk.CTkFrame(self.left_column, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            label = ctk.CTkLabel(
                frame,
                text=f"{label_text}:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="white",
                width=100,
                anchor="w"
            )
            label.pack(side="left")
            
            entry = ctk.CTkEntry(
                frame,
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#333333",
                border_color="#555555",
                text_color="white",
                corner_radius=8,
                height=35
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            self.entries[field_name] = entry
        
        # Description field (multiline)
        desc_frame = ctk.CTkFrame(self.left_column, fg_color="transparent")
        desc_frame.pack(fill="x", pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Deskripsi:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="white",
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        self.desc_text = ctk.CTkTextbox(
            self.left_column,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#333333",
            border_color="#555555",
            text_color="white",
            corner_radius=8,
            height=150
        )
        self.desc_text.pack(fill="both", expand=True, pady=10)
    
    def create_cover_section(self):
        # Cover label
        cover_title = ctk.CTkLabel(
            self.right_column,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="white"
        )
        cover_title.pack(pady=(0, 10))
        
        # Cover preview frame
        self.cover_frame = ctk.CTkFrame(self.right_column, fg_color="#333333", corner_radius=5)
        self.cover_frame.pack(pady=10)
        
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=10, pady=10)
        
        # Default "No Image" display
        self.load_default_cover()
        
        # Upload button
        self.upload_btn = ctk.CTkButton(
            self.right_column,
            text="Pilih Gambar Cover",
            command=self.browse_cover,
            fg_color="#4C0086",
            hover_color="#3C0066",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=10,
            height=40
        )
        self.upload_btn.pack(pady=10)
        
        # Cover info
        self.cover_info = ctk.CTkLabel(
            self.right_column,
            text="Format: JPEG/JPG\nUkuran yang disarankan: 180x270 px",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#888888",
            justify="center"
        )
        self.cover_info.pack(pady=5)
        
        # Selected file info
        self.selected_file_label = ctk.CTkLabel(
            self.right_column,
            text="Tidak ada file dipilih",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#888888",
            justify="center"
        )
        self.selected_file_label.pack(pady=5)
    
    def load_default_cover(self):
        """Load default cover image"""
        size = (180, 270)
        try:
            img = Image.open(self.default_cover)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.cover_label.configure(image=photo_img)
            self.cover_label.image = photo_img
        except Exception as e:
            print(f"Error loading default cover: {e}")
            self.cover_label.configure(text="No Image")
    
    def browse_cover(self):
        """Open file dialog to select cover image"""
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        )
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select Book Cover",
            filetypes=filetypes
        )
        
        if not file_path:
            return
        
        # Check file size and type
        try:
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            
            if file_size > 5000:  # 5MB limit
                messagebox.showerror("Error", "File terlalu besar. Maksimum ukuran: 5MB")
                return
            
            # Load and preview image
            self.load_cover_preview(file_path)
            
            # Update selected file info
            file_name = os.path.basename(file_path)
            self.selected_file_label.configure(text=f"File: {file_name}")
            
            # Save temp path for later saving
            self.temp_cover_path = file_path
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memproses file: {e}")
    
    def load_cover_preview(self, file_path):
        """Load and display cover preview from selected file"""
        size = (180, 270)
        try:
            img = Image.open(file_path)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.cover_label.configure(image=photo_img)
            self.cover_label.image = photo_img
        except Exception as e:
            print(f"Error loading cover preview: {e}")
            messagebox.showerror("Error", f"Gagal menampilkan preview: {e}")
    
    def validate_form(self):
        """Validate form inputs"""
        required_fields = ["title", "author", "publisher", "year", "category", "isbn"]
        
        for field in required_fields:
            if not self.entries[field].get().strip():
                messagebox.showerror("Error", f"Field {field} tidak boleh kosong")
                return False
        
        # Validate ISBN format (basic validation)
        isbn = self.entries["isbn"].get().strip()
        if not isbn.isdigit() or len(isbn) < 10:
            messagebox.showerror("Error", "ISBN harus berupa angka dengan minimal 10 digit")
            return False
        
        # Validate year is a number
        try:
            year = int(self.entries["year"].get())
            if year < 1000 or year > 3000:
                messagebox.showerror("Error", "Tahun harus berupa angka valid (1000-3000)")
                return False
        except ValueError:
            messagebox.showerror("Error", "Tahun harus berupa angka")
            return False
        
        # Validate pages is a number
        try:
            pages = int(self.entries["pages"].get())
            if pages < 0:
                messagebox.showerror("Error", "Halaman harus berupa angka positif")
                return False
        except ValueError:
            messagebox.showerror("Error", "Halaman harus berupa angka")
            return False
        
        # Check if cover image is selected
        if not self.temp_cover_path:
            result = messagebox.askyesno("Konfirmasi", "Anda belum memilih gambar cover. Gunakan cover default?")
            if not result:
                return False
        
        return True
    
    def save_book(self):
        """Save new book with form data"""
        if not self.validate_form():
            return
        
        isbn = self.entries["isbn"].get().strip()
        
        # Check if book with ISBN already exists
        if hasattr(self.controller, "check_isbn_exists"):
            if self.controller.check_isbn_exists(isbn):
                messagebox.showerror("Error", "Buku dengan ISBN tersebut sudah ada")
                return
        
        # Save cover image
        cover_filename = f"{isbn}.jpeg"
        cover_path = os.path.join(self.cover_dir, cover_filename)
        
        try:
            if self.temp_cover_path:
                # Copy and convert image to JPEG if needed
                img = Image.open(self.temp_cover_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(cover_path, "JPEG")
            else:
                # Use default cover
                shutil.copy(self.default_cover, cover_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan gambar cover: {e}")
            return
        
        # Collect book data
        new_book = {
            "Judul": self.entries["title"].get(),
            "Penulis": self.entries["author"].get(),
            "Penerbit": self.entries["publisher"].get(),
            "Tahun": self.entries["year"].get(),
            "Kategori": self.entries["category"].get(),
            "ISBN": isbn,
            "Halaman": self.entries["pages"].get(),
            "Deskripsi": self.desc_text.get("1.0", "end-1c"),
            "available": True  # New book is available by default
        }
        
        # Call controller to add book
        if hasattr(self.controller, "add_book"):
            result = self.controller.add_book(new_book)
            if result:
                messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
                self.clear_form()
        else:
            print("Warning: Controller does not have add_book method")
            messagebox.showinfo("Demo", "Fitur tambah buku akan terintegrasi dengan controller")
            self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, "end")
        
        self.desc_text.delete("1.0", "end")
        self.load_default_cover()
        self.temp_cover_path = None
        self.selected_file_label.configure(text="Tidak ada file dipilih")
    
    def go_back(self):
        """Go back to previous page"""
        if hasattr(self.controller, "show_frame"):
            self.controller.show_frame("home")  # Adjust as needed based on your navigation structure


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Add Book")
    root.geometry("1024x768")
    
    # Create simple controller class for testing
    class TestController:
        def show_frame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def add_book(self, book_data):
            print("Book added:", book_data)
            return True
        
        def check_isbn_exists(self, isbn):
            # For testing - pretend ISBN 1234567890 already exists
            return isbn == "1234567890"
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = AddBookFrame(frame, TestController())
    app.pack(expand=True, fill="both")
    
    root.mainloop()