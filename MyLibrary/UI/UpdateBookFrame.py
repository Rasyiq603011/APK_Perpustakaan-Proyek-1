import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
import sys
from PIL import Image

class UpdateBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, book=None):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        self.controller = controller
        self.book = book
        self.default_cover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.cover_dir = "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover"
        
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
            text="UPDATE BUKU",
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
        
        # Right column - Cover preview
        self.cover_frame = ctk.CTkFrame(self.right_column, fg_color="#333333", corner_radius=5)
        self.cover_frame.pack(pady=20)
        
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=10, pady=10)
        
        # Cannot update cover in update mode - only in add mode
        self.cover_info = ctk.CTkLabel(
            self.right_column,
            text="Cover tidak dapat diubah di mode update.\nUntuk mengubah cover, gunakan mode tambah buku baru.",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#888888",
            justify="center"
        )
        self.cover_info.pack(pady=10)
        
        # Button container
        self.button_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_container.pack(fill="x", pady=20)
        
        # Update button
        self.update_btn = ctk.CTkButton(
            self.button_container,
            text="Simpan Perubahan",
            command=self.update_book,
            fg_color="#00CC00",
            hover_color="#00AA00",
            text_color="black",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=200
        )
        self.update_btn.pack(side="right", padx=20)
        
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
        
        # Load book data if provided
        if self.book:
            self.load_book_data()
    
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
        
        # Add ISBN field as read-only in update mode
        self.entries["isbn"].configure(state="disabled")
    
    def load_book_data(self):
        """Load book data into form fields"""
        if not self.book:
            return
        
        # Map book dictionary keys to form field names
        field_mapping = {
            "Judul": "title",
            "Penulis": "author",
            "Penerbit": "publisher", 
            "Tahun": "year",
            "Kategori": "category",
            "ISBN": "isbn",
            "Halaman": "pages"
        }
        
        # Set values in entry fields
        for book_key, field_name in field_mapping.items():
            if book_key in self.book and field_name in self.entries:
                self.entries[field_name].delete(0, "end")
                self.entries[field_name].insert(0, str(self.book.get(book_key, "")))
        
        # Set description
        if "Deskripsi" in self.book:
            self.desc_text.delete("1.0", "end")
            self.desc_text.insert("1.0", str(self.book.get("Deskripsi", "")))
        
        # Load cover image
        self.load_cover_image()
    
    def load_cover_image(self):
        """Load book cover image for preview"""
        size = (180, 270)
        isbn = self.book.get("ISBN", "")
        img_path = os.path.join(self.cover_dir, f"{isbn}.jpeg")
        
        if not os.path.exists(img_path) or not isbn:
            img_path = self.default_cover
        
        try:
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.cover_label.configure(image=photo_img)
            self.cover_label.image = photo_img
        except Exception as e:
            print(f"Error loading cover image: {e}")
    
    def validate_form(self):
        """Validate form inputs"""
        required_fields = ["title", "author", "publisher", "year", "category", "isbn"]
        
        for field in required_fields:
            if not self.entries[field].get().strip():
                messagebox.showerror("Error", f"Field {field} tidak boleh kosong")
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
        
        return True
    
    def update_book(self):
        """Update book with form data"""
        if not self.validate_form():
            return
        
        # Collect updated data
        updated_book = {
            "Judul": self.entries["title"].get(),
            "Penulis": self.entries["author"].get(),
            "Penerbit": self.entries["publisher"].get(),
            "Tahun": self.entries["year"].get(),
            "Kategori": self.entries["category"].get(),
            "ISBN": self.entries["isbn"].get(),
            "Halaman": self.entries["pages"].get(),
            "Deskripsi": self.desc_text.get("1.0", "end-1c")
        }
        
        # Call controller update method (to be implemented by the parent application)
        if hasattr(self.controller, "update_book"):
            result = self.controller.update_book(updated_book)
            if result:
                messagebox.showinfo("Sukses", "Buku berhasil diperbarui!")
                self.go_back()
        else:
            print("Warning: Controller does not have update_book method")
            messagebox.showinfo("Demo", "Fitur update akan terintegrasi dengan controller")
            self.go_back()
    
    def go_back(self):
        """Go back to previous page"""
        if hasattr(self.controller, "show_frame"):
            self.controller.show_frame("home")  # Adjust as needed based on your navigation structure


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Update Book")
    root.geometry("1024x768")
    
    # Create simple controller class for testing
    class TestController:
        def show_frame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def update_book(self, book_data):
            print("Book updated:", book_data)
            return True
    
    # Sample book data for testing
    sample_book = {
        "Judul": "Quidditch Through the Ages: the Illustrated Edition",
        "Penulis": "J. K. Rowling",
        "Penerbit": "Bloomsbury",
        "Tahun": "2020",
        "Kategori": "Juvenile Fiction",
        "ISBN": "9781338340563",
        "Halaman": "158",
        "Deskripsi": "Kennilworthy Whisp is a fictitious author created by J.K. Rowling."
    }
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = UpdateBookFrame(frame, TestController(), sample_book)
    app.pack(expand=True, fill="both")
    
    root.mainloop()