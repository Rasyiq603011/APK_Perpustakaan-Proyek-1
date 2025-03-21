import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import shutil
from PIL import Image

class UpdateBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, book=None):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        self.controller = controller
        self.book = book
        self.default_cover = "D:\\Project 1\\Tubes Semester 1\\Asset\\IMG.jpg"
        self.cover_dir = "D:\\Project 1\\Tubes Semester 1\\Asset\\Cover"
        self.selected_cover_path = None  # Path to temporarily selected cover

        # Main frame - Sebenarnya kita tidak perlu membuat frame lagi di dalam frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)  # Header row
        self.rowconfigure(1, weight=1)  # Content row
        self.rowconfigure(2, weight=0)  # Footer row
        
        # ===== HEADER SECTION =====
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.header_frame.columnconfigure(0, weight=1)  # Back button
        self.header_frame.columnconfigure(1, weight=2)  # Title
        self.header_frame.columnconfigure(2, weight=1)  # Empty space for symmetry
        
        # Back button
        self.back_btn = ctk.CTkButton(
            self.header_frame, 
            text="← Kembali", 
            command=lambda: self.controller.showFrame("DataBookFrame") if hasattr(self.controller, 'showFrame') else None,
            fg_color="#4C0086",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            corner_radius=15,
            width=150,
            height=35
        )
        self.back_btn.grid(row=0, column=0, sticky="w", padx=10)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="UPDATE BUKU",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=1)
        
        # ===== CONTENT SECTION =====
        # Form container (left side)
        self.form_container = ctk.CTkFrame(self, fg_color="#2D2D2D", corner_radius=10)
        self.form_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        
        # Create form fields
        self.create_form_fields()
        
        # Cover container (right side)
        self.cover_container = ctk.CTkFrame(self, fg_color="#2D2D2D", corner_radius=10)
        self.cover_container.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
        
        # Add cover section
        self.create_cover_section()
        
        # ===== FOOTER SECTION =====
        self.footer = ctk.CTkFrame(self, fg_color="#262626", height=70, corner_radius=10)
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        # Prevent height from changing
        self.footer.pack_propagate(False)
        
        # Cancel button - Left side
        self.cancelBtn = ctk.CTkButton(
            self.footer,
            text="Batal",
            command=lambda: self.controller.showFrame("DataBookFrame") if hasattr(self.controller, 'showFrame') else None,
            fg_color="#FF6B6B",
            hover_color="#FF5555",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=15,
            height=45,
            width=150
        )
        self.cancelBtn.pack(side="left", padx=40, pady=12)
        
        # Update button - Right side
        self.updateBtn = ctk.CTkButton(
            self.footer,
            text="Simpan Perubahan",
            command=self.update_book,
            fg_color="#00CC00",
            hover_color="#00AA00",
            text_color="black",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            corner_radius=15,
            height=45,
            width=250
        )
        self.updateBtn.pack(side="right", padx=40, pady=12)
        
        # Load book data if provided
        if self.book:
            self.load_book_data()
    
    def create_form_fields(self):
        """Create entry fields for book data"""
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
        
        # Configure form container layout
        self.form_container.columnconfigure(0, weight=0)  # Labels
        self.form_container.columnconfigure(1, weight=1)  # Entry fields
        
        # Create fields
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                self.form_container,
                text=f"{label_text}:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="white",
                anchor="w",
                width=100
            )
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(
                self.form_container,
                font=ctk.CTkFont(family="Arial", size=14),
                fg_color="#333333",
                border_color="#555555",
                text_color="white",
                corner_radius=8,
                height=35
            )
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            
            self.entries[field_name] = entry
        
        # Make ISBN field read-only
        self.entries["ISBN"].configure(state="disabled")
        
        # Description label (one row below the last field)
        desc_label = ctk.CTkLabel(
            self.form_container,
            text="Deskripsi:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="white",
            anchor="w"
        )
        desc_label.grid(row=len(fields), column=0, padx=10, pady=(20, 5), sticky="nw")
        
        # Description textbox
        self.desc_text = ctk.CTkTextbox(
            self.form_container,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#333333",
            border_color="#555555",
            text_color="white",
            corner_radius=8,
            height=150
        )
        self.desc_text.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        
        # Make the description row expandable
        self.form_container.rowconfigure(len(fields)+1, weight=1)
    
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
        cover_title.grid(row=0, column=0, pady=(20, 10))
        
        # Cover image frame
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color="#333333", corner_radius=5)
        self.cover_frame.grid(row=1, column=0, pady=10)
        
        # Cover image label
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=10, pady=10)
        
        # Update cover button
        self.upload_btn = ctk.CTkButton(
            self.cover_container,
            text="Ubah Gambar Cover",
            command=self.browse_cover,
            fg_color="#4C0086",
            hover_color="#3C0066",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=10,
            height=35
        )
        self.upload_btn.grid(row=2, column=0, pady=10)
        
        # Cover info
        info_frame = ctk.CTkFrame(self.cover_container, fg_color="#3D3D3D", corner_radius=5)
        info_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="Format: JPEG/JPG\nUkuran yang disarankan: 180x270 px\nKlik tombol di atas untuk mengganti cover",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#FFFFFF",
            justify="center"
        )
        info_text.pack(pady=10, padx=10)
        
        # Selected file info
        self.selected_file_label = ctk.CTkLabel(
            self.cover_container,
            text="Tidak ada file baru dipilih",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#888888",
            justify="center"
        )
        self.selected_file_label.grid(row=4, column=0, pady=5)
    
    def load_book_data(self):
        """Load book data into form fields"""
        if not self.book:
            return
        
        # Set values in entry fields
        for field_name in self.entries:
            if field_name in self.book:
                self.entries[field_name].delete(0, "end")
                self.entries[field_name].insert(0, str(self.book.get(field_name, "")))
        
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
            self.selected_file_label.configure(text=f"File baru: {file_name}")
            
            # Save path for later updating
            self.selected_cover_path = file_path
            
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
        
        return True
    
    def update_book(self):
        """Update book information and cover if needed"""
        if not self.validate_form():
            return
        
        # Get book information for confirmation message
        judul = self.entries["Judul"].get()
        penulis = self.entries["Penulis"].get()
        
        # Show confirmation dialog with book details
        confirm_message = f"Yakin ingin menyimpan perubahan untuk buku berikut?\n\nJudul: {judul}\nPenulis: {penulis}"
        if self.selected_cover_path:
            confirm_message += "\n\nCover buku juga akan diperbarui."
            
        # Ask for confirmation before proceeding
        user_confirm = messagebox.askokcancel(
            "Konfirmasi Simpan Perubahan", 
            confirm_message,
            icon="question"
        )
        
        if not user_confirm:
            return
        
        # Get ISBN for cover file naming
        isbn = self.entries["ISBN"].get().strip()
        
        # Save new cover image if selected
        if self.selected_cover_path:
            try:
                cover_filename = f"{isbn}.jpeg"
                cover_path = os.path.join(self.cover_dir, cover_filename)
                
                # Create backup of existing cover
                if os.path.exists(cover_path):
                    backup_path = os.path.join(self.cover_dir, f"{isbn}_backup.jpeg")
                    shutil.copy2(cover_path, backup_path)
                
                # Copy and convert image to JPEG if needed
                img = Image.open(self.selected_cover_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(cover_path, "JPEG")
                print(f"Cover updated: {cover_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar cover: {e}")
                return
        
        # Collect updated data
        updated_book = {
            "Judul": self.entries["Judul"].get(),
            "Penulis": self.entries["Penulis"].get(),
            "Penerbit": self.entries["Penerbit"].get(),
            "Tahun": self.entries["Tahun"].get(),
            "Kategori": self.entries["Kategori"].get(),
            "ISBN": isbn,
            "Halaman": self.entries["Halaman"].get(),
            "Deskripsi": self.desc_text.get("1.0", "end-1c")
        }
        
        # Add a loading indicator
        self.updateBtn.configure(state="disabled", text="Menyimpan...")
        self.update_idletasks()  # Force UI update
        
        # Call controller update method
        try:
            if hasattr(self.controller, "UpdateBook"):
                result = self.controller.UpdateBook(updated_book)
                if result:
                    messagebox.showinfo("Sukses", "Buku berhasil diperbarui!")
                    if hasattr(self.controller, "showFrame"):
                        self.controller.showFrame("DataBookFrame")
            elif hasattr(self.controller.bookManager, "UpdateBook"):
                result = self.controller.bookManager.UpdateBook(updated_book)
                if result:
                    messagebox.showinfo("Sukses", "Buku berhasil diperbarui!")
                    if hasattr(self.controller, "showFrame"):
                        self.controller.showFrame("DataBookFrame")
            else:
                print("Warning: Controller does not have UpdateBook method")
                messagebox.showinfo("Demo", "Fitur update akan terintegrasi dengan controller")
                if hasattr(self.controller, "showFrame"):
                    self.controller.showFrame("DataBookFrame")
        finally:
            # Restore button state if we're still on this frame
            if self.winfo_exists():
                self.updateBtn.configure(state="normal", text="Simpan Perubahan")


# Test function if run directly
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Update Book")
    root.geometry("1024x768")
    
    # Create simple controller class for testing
    class TestController:
        def showFrame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def UpdateBook(self, book_data):
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