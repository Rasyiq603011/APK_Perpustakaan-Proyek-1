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
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background
        
        self.controller = controller
        self.default_cover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.cover_dir = "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover"
        self.UploadCoverpath = None  # Path to temporarily selected cover
        
        # Ensure cover directory exists
        os.makedirs(self.cover_dir, exist_ok=True)
        
        # Main frame layout - Optimized for 1024x768
        self.columnconfigure(0, weight=3)  # Form container gets more space
        self.columnconfigure(1, weight=2)  # Cover container
        self.rowconfigure(0, weight=0)  # Header row - fixed height
        self.rowconfigure(1, weight=1)  # Content row - expands
        self.rowconfigure(2, weight=0)  # Footer row - fixed height
        
        # ===== HEADER SECTION =====
        # Simplified header with less padding for more compact layout
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))
        self.header_frame.columnconfigure(0, weight=1)  # Back button
        self.header_frame.columnconfigure(1, weight=2)  # Title
        self.header_frame.columnconfigure(2, weight=1)  # Empty space for symmetry
        
        # Back button - made slightly more compact
        self.back_btn = ctk.CTkButton(
            self.header_frame, 
            text="← Kembali", 
            command=lambda: self.controller.show_frame("DataBookFrame") if hasattr(self.controller, 'show_frame') else None,
            fg_color="#6200EA",  # Deeper purple matching React design
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
            text="TAMBAH BUKU BARU",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=1)
        
        # ===== CONTENT SECTION =====
        # Form container (left side) - more compact with grid layout
        self.form_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Slightly lighter background for form
        self.form_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=5)
        
        # Create form fields with optimized layout
        self.create_form_fields()
        
        # Cover container (right side) - more compact
        self.cover_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Matching form container color
        self.cover_container.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=5)
        
        # Add cover section
        self.create_cover_section()
        
        # ===== FOOTER SECTION =====
        # More compact footer
        self.footer = ctk.CTkFrame(self, fg_color="#232323", height=60, corner_radius=10)  # Darker footer
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 10))
        # Prevent height from changing
        self.footer.pack_propagate(False)
        
        # Cancel button - Left side
        self.cancel_btn = ctk.CTkButton(
            self.footer,
            text="Batal",
            command=lambda: self.controller.show_frame("DataBookFrame") if hasattr(self.controller, 'show_frame') else None,
            fg_color="#F44336",  # Material design red
            hover_color="#D32F2F",  # Darker red for hover
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=40,
            width=120
        )
        self.cancel_btn.pack(side="left", padx=40, pady=10)
        
        # Save button - Right side
        self.save_btn = ctk.CTkButton(
            self.footer,
            text="Simpan Buku",
            command=self.save_book,
            fg_color="#4CAF50",  # Material design green
            hover_color="#388E3C",  # Darker green for hover
            text_color="white",  # White text for better contrast
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=40,
            width=180
        )
        self.save_btn.pack(side="right", padx=40, pady=10)
        
        # Clear the form initially
        self.clear_form()
        
    def create_form_fields(self):
        """Create entry fields for book data using grid layout for better space utilization"""
        # Define fields with their labels
        fields = [
            ("Judul", "Judul"),
            ("Penulis", "Penulis"),
            ("Penerbit", "Penerbit"),
            ("Tahun", "Tahun"),
            ("Kategori", "Kategori"),
            ("ISBN", "ISBN"),
            ("Halaman", "Halaman"),
        ]
        
        # Create entry fields
        self.entries = {}
        
        # Configure form container with grid layout
        # Use 2 columns to make more efficient use of space
        self.form_container.columnconfigure(0, weight=0)  # Label 1
        self.form_container.columnconfigure(1, weight=1)  # Entry 1
        self.form_container.columnconfigure(2, weight=0)  # Label 2
        self.form_container.columnconfigure(3, weight=1)  # Entry 2
        
        # Create fields in a grid layout - 2 columns side by side
        for i, (label_text, field_name) in enumerate(fields):
            # Calculate row and column
            row = i // 2
            base_col = (i % 2) * 2
            
            # Label
            label = ctk.CTkLabel(
                self.form_container,
                text=f"{label_text}:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="white",
                anchor="w",
                width=70  # Reduced width
            )
            label.grid(row=row, column=base_col, padx=(10, 5), pady=8, sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(
                self.form_container,
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#3D3D3D",  # Lighter input field background
                border_color="#666666",  # Lighter border for better visibility
                text_color="white",
                corner_radius=8,
                height=30  # Reduced height
            )
            entry.grid(row=row, column=base_col+1, padx=(0, 10), pady=8, sticky="ew")
            
            self.entries[field_name] = entry
        
        # Description label (spans all columns)
        desc_label = ctk.CTkLabel(
            self.form_container,
            text="Deskripsi:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="white",
            anchor="w"
        )
        desc_label.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Description textbox (spans all columns)
        self.desc_text = ctk.CTkTextbox(
            self.form_container,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#3D3D3D",  # Lighter input field background
            border_color="#666666",  # Lighter border
            text_color="white",
            corner_radius=8,
            height=120  # Reduced height
        )
        self.desc_text.grid(row=5, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="nsew")
        
        # Make the description row expandable
        self.form_container.rowconfigure(5, weight=1)
    
    def create_cover_section(self):
        """Create the cover preview and upload section"""
        # Configure cover container layout
        self.cover_container.columnconfigure(0, weight=1)
        self.cover_container.rowconfigure(0, weight=0)  # Label
        self.cover_container.rowconfigure(1, weight=1)  # Cover image
        self.cover_container.rowconfigure(2, weight=0)  # Button
        self.cover_container.rowconfigure(3, weight=0)  # Info
        
        # Cover title
        cover_title = ctk.CTkLabel(
            self.cover_container,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        cover_title.grid(row=0, column=0, pady=(15, 10))
        
        # Cover image frame - Light background like in React design
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color="#F5F5F5", corner_radius=5)  # Light background for cover like in design
        self.cover_frame.grid(row=1, column=0, pady=5)
        
        # Cover image label - using the recommended 180x270 ratio
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=10, pady=10)
        
        # Update cover button
        self.upload_btn = ctk.CTkButton(
            self.cover_container,
            text="Pilih Gambar Cover",
            command=self.browse_cover,
            fg_color="#6200EA",  # Deeper purple matching React design
            hover_color="#5000D0",  # Slightly lighter purple for hover
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=10,
            height=30
        )
        self.upload_btn.grid(row=2, column=0, pady=10)
        
        # Cover info
        info_frame = ctk.CTkFrame(self.cover_container, fg_color="#363636", corner_radius=5)  # Slightly darker info frame
        info_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="Format: JPEG/JPG\nUkuran yang disarankan: 180x270 px",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#FFFFFF",
            justify="center"
        )
        info_text.pack(pady=8, padx=10)
        
        # Selected file info
        self.selected_file_label = ctk.CTkLabel(
            self.cover_container,
            text="Tidak ada file dipilih",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA",  # Lighter text for better readability
            justify="center"
        )
        self.selected_file_label.grid(row=4, column=0, pady=5)
        
        # Load default cover image
        self.load_default_cover()
    
    def load_default_cover(self):
        """Load default cover image"""
        size = (180, 270)
        try:
            img = Image.open(self.default_cover)
            img = img.resize(size, Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=size)
            self.cover_label.configure(image=photo_img)
            self.cover_label.image = photo_img  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Error loading default cover: {e}")
            self.cover_label.configure(text="No Image")
    
    def browse_cover(self):
        """Allow user to select a new cover image"""
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
            
            # Save path for later updating
            self.UploadCoverpath = file_path
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memproses file: {e}")
    
    def load_cover_preview(self, file_path):
        """Preview selected cover image"""
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
        required_fields = ["Judul", "Penulis", "Penerbit", "Tahun", "Kategori", "ISBN", "Halaman"]
        
        for field in required_fields:
            if not self.entries[field].get().strip():
                messagebox.showerror("Error", f"Field {field} tidak boleh kosong")
                return False
        
        # Validate ISBN format (basic validation)
        isbn = self.entries["ISBN"].get().strip()
        if not isbn.isdigit() or len(isbn) < 10:
            messagebox.showerror("Error", "ISBN harus berupa angka dengan minimal 10 digit")
            return False
        
        # Validate year is a number
        try:
            year = int(self.entries["Tahun"].get())
            if year < 1000 or year > 3000:
                messagebox.showerror("Error", "Tahun harus berupa angka valid (1000-3000)")
                return False
        except ValueError:
            messagebox.showerror("Error", "Tahun harus berupa angka")
            return False
        
        # Validate pages is a number
        try:
            pages = int(self.entries["Halaman"].get())
            if pages < 0:
                messagebox.showerror("Error", "Halaman harus berupa angka positif")
                return False
        except ValueError:
            messagebox.showerror("Error", "Halaman harus berupa angka")
            return False
        
        # Check if cover image is selected
        if not self.UploadCoverpath:
            result = messagebox.askyesno("Konfirmasi", "Anda belum memilih gambar cover. Gunakan cover default?")
            if not result:
                return False
        
        return True
    
    def save_book(self):
        """Save book information and cover"""
        if not self.validate_form():
            return
        
        isbn = self.entries["ISBN"].get().strip()
        
        # Check if book with ISBN already exists
        if hasattr(self.controller, "ISBNexists"):
            if self.controller.ISBNexists(isbn):
                messagebox.showerror("Error", "Buku dengan ISBN tersebut sudah ada")
                return
        
        # Get book information for confirmation message
        judul = self.entries["Judul"].get()
        penulis = self.entries["Penulis"].get()
        
        # Show confirmation dialog
        confirm_message = f"Yakin ingin menyimpan buku berikut?\n\nJudul: {judul}\nPenulis: {penulis}\nISBN: {isbn}"
        
        # Ask for confirmation before proceeding
        user_confirm = messagebox.askokcancel(
            "Konfirmasi Simpan Buku", 
            confirm_message,
            icon="question"
        )
        
        if not user_confirm:
            return
        
        # Save cover image
        cover_filename = f"{isbn}.jpeg"
        cover_path = os.path.join(self.cover_dir, cover_filename)
        
        try:
            if self.UploadCoverpath:
                # Copy and convert image to JPEG if needed
                img = Image.open(self.UploadCoverpath)
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
        book = {
            "Judul": self.entries["Judul"].get(),
            "Penulis": self.entries["Penulis"].get(),
            "Penerbit": self.entries["Penerbit"].get(),
            "Tahun": self.entries["Tahun"].get(),
            "Kategori": self.entries["Kategori"].get(),
            "ISBN": isbn,
            "Halaman": self.entries["Halaman"].get(),
            "Deskripsi": self.desc_text.get("1.0", "end-1c"),
            "Status": "Available",
        }
        
        # Add a loading indicator
        self.save_btn.configure(state="disabled", text="Menyimpan...")
        self.update_idletasks()  # Force UI update
        
        # Call controller to add book
        try:
            if hasattr(self.controller, "save_book"):
                result = self.controller.save_book(book)
                if result:
                    messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
                    self.clear_form()
            else:
                print("Warning: Controller does not have save_book method")
                messagebox.showinfo("Demo", "Fitur tambah buku akan terintegrasi dengan controller")
                self.clear_form()
        finally:
            # Restore button state
            self.save_btn.configure(state="normal", text="Simpan Buku")
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, "end")
        
        self.desc_text.delete("1.0", "end")
        self.load_default_cover()
        self.UploadCoverpath = None
        self.selected_file_label.configure(text="Tidak ada file dipilih")


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tambah Buku")
    root.geometry("1024x768")
    
    # Create simple controller class for testing
    class TestController:
        def show_frame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def save_book(self, book_data):
            print("Book added:", book_data)
            return True
        
        def ISBNexists(self, isbn):
            # For testing - pretend ISBN 1234567890 already exists
            return isbn == "1234567890"
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    app = AddBookFrame(frame, TestController())
    app.pack(expand=True, fill="both")
    
    root.mainloop()