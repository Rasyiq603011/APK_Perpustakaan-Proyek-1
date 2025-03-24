import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import shutil
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constans import COLOR_DARK, COLOR_LIGHT 

class AddBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background
        self.is_dark_mode = True
        self.color = COLOR_DARK if self.is_dark_mode else COLOR_LIGHT

        self.controller = controller
        self.default_cover = "C:\\Users\\R d t\\Desktop\\Project Learning\\tkinter\\Last Week\\APK_Perpustakaan-Proyek-1\\assets\\IMG.jpg"
        self.cover_dir = "C:\\Users\\R d t\\Desktop\\Project Learning\\tkinter\\Last Week\\APK_Perpustakaan-Proyek-1\\assets\\Cover"
        self.UploadCoverpath = None  # Path to temporarily selected cover
        self.Layout()
    
    def Layout(self):
         # Main frame layout 
        self.columnconfigure(0, weight=3) # From Section
        self.columnconfigure(1, weight=2)  # Cover Section
        self.rowconfigure(0, weight=0)  # Header
        self.rowconfigure(1, weight=1)  # content
        self.rowconfigure(2, weight=0)  # Footer 
        
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
                text="TAMBAH BUKU", 
                font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
                text_color=self.color["primaryText"]
        )
        self.title_label.grid(row=0, column=1)
            
    def Content(self):
    # ===== CONTENT SECTION =====
    # Form container
        self.form_container = ctk.CTkFrame(self, fg_color=self.color["surface"], corner_radius=10)  # Slightly lighter background for form
        self.form_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=20)
            
        self.form_container.columnconfigure(0, weight= 0)
        self.form_container.columnconfigure(1, weight= 1)
        self.form_container.columnconfigure(2, weight= 0)
        self.form_container.columnconfigure(3, weight= 1)

        self.create_form_fields()
            
    # Cover container (right side) - more compact
        self.cover_container = ctk.CTkFrame(self, fg_color=self.color["surface"], corner_radius=10)  # Matching form container color
        self.cover_container.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.create_cover_section()
            
    def Footer(self):
    # ===== FOOTER SECTION =====
        self.footer = ctk.CTkFrame(self, fg_color="transparent", height=60, corner_radius=10)
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        self.footer.pack_propagate(False)
            
            # Cancel button - Left side
        self.cancelBtn = ctk.CTkButton(
                self.footer,
                text="Batal",
                command=lambda: self.controller.showFrame("DetailsBookFrame"),
                fg_color=self.color["cancelButton"],
                hover_color=self.color["error"],
                text_color=self.color["primaryText"],
                font=ctk.CTkFont(family="Arial", size=14),
                corner_radius=10,
                height=40,
                width=120
            )
        self.cancelBtn.pack(side="left", padx=40, pady=10)
            
            # Update button - Right side
        self.updateBtn = ctk.CTkButton(
                self.footer,
                text="save book", 
                command=self.save_book,
                fg_color=self.color["success"], 
                hover_color=self.color["active"]["accent"],
                text_color=self.color["primaryText"],
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                corner_radius=10,
                height=40,
                width=150
            )
        self.updateBtn.pack(side="right", padx=40, pady=10)
    
        
    def create_form_fields(self):
        fields = [
            ("Judul", 0, 0),
            ("Penulis", 0, 2),
            ("Penerbit", 1, 0),
            ("Tahun", 1, 2),
            ("Kategori", 2, 0),
            ("Halaman", 2, 2),
            ("ISBN", 3, 0)
        ]
        
        self.entries = {}
        
        # Create fields in a grid layout - 2 columns side by side
        for field in fields:
            field_name, row, col = field

            # Label
            label = ctk.CTkLabel(
                self.form_container,
                text=f"{field_name}:",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color=self.color["primaryText"],
                anchor="w",
                width=70  # Reduced width
            )
            label.grid(row=row, column=col, padx=(20), pady=15, sticky="w")
            
            if field_name == "Kategori":

                dropdown = ctk.CTkOptionMenu(
                    self.form_container,
                    values=["Science Fiction","Young Adult","Graphic Novels","Fiction","Non-Fiction", "Education","Arts & Humanities","Religion & Spirituality", "Social Sciences","Nature & Environment"],
                    font=ctk.CTkFont(family="Arial", size=14),
                    fg_color=self.color["inputField"],
                    button_color=self.color["primary"],
                    button_hover_color=self.color["hover"]["primary"],
                    dropdown_fg_color=self.color["surface"],
                    dropdown_text_color=self.color["primaryText"],
                    dropdown_hover_color=self.color["hover"]["primary"],
                    text_color=self.color["primaryText"],
                    height=30,
                    dynamic_resizing=False
                )

                dropdown.grid(row=row, column=col+1, padx=(20), pady=15, sticky="ew")
                dropdown.configure(width=entry.winfo_width())
                self.entries[field_name] = dropdown
            else:
                # Create regular entry for other fields
                entry = ctk.CTkEntry(
                    self.form_container,
                    font=ctk.CTkFont(family="Arial", size=14),
                    fg_color=self.color["inputField"],
                    border_color=self.color["border"],
                    text_color=self.color["primaryText"],
                    corner_radius=8,
                    height=30
                )
                entry.grid(row=row, column=col+1, padx=(20), pady=15, sticky="ew")
                self.entries[field_name] = entry

            

        
        # Description label (spans all columns)
        self.desc_label = ctk.CTkLabel(
            self.form_container,
            text="Deskripsi:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color=self.color["primaryText"],
            anchor="w"
        )
        self.desc_label.grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")
        
        # Description textbox (spans all columns)
        self.desc_text = ctk.CTkTextbox(
            self.form_container,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color=self.color["inputField"],  # Lighter input field background
            border_color=self.color["border"],  # Lighter border
            text_color=self.color["primaryText"],
            corner_radius=8,
            height=120  # Reduced height
        )
        self.desc_text.grid(row=5, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="nsew")

        # Make the description row expandable
        self.form_container.rowconfigure(5, weight=1)
    
    def create_cover_section(self):
        
        # Cover title
        cover_title = ctk.CTkLabel(
            self.cover_container,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=self.color["primaryText"]
        )
        cover_title.pack(pady=(20, 10))
        
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color=self.color["background"], corner_radius=10)  # Light background for cover like in design
        self.cover_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Cover image label - using the recommended 180x270 ratio
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=20, pady=20)
        
        # Update cover button
        self.upload_btn = ctk.CTkButton(
            self.cover_container,
            text="Upload cover",
            command=self.browse_cover,
            fg_color=self.color["accent"],
            hover_color=self.color["hover"]["accent"], 
            text_color=self.color["primaryText"],
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=8,
            height=36
        )
        self.upload_btn.pack(pady=10)
        
        # Selected file info
        self.selected_file_label = ctk.CTkLabel(
            self.cover_container,
            text="Tidak ada file dipilih",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.color["secondaryText"], 
            justify="center"
        )
        self.selected_file_label.pack()

        # Cover info
        info_frame = ctk.CTkFrame(self.cover_container, fg_color=self.color["inputField"], corner_radius=8) 
        info_frame.pack(padx=20, pady=20, fill="x")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="Format: JPEG/JPG\nUkuran yang disarankan: 180x270 px",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=self.color["primaryText"],
            justify="center"
        )
        info_text.pack(pady=15, padx=15)
    
       
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
            if hasattr(self.controller, "saveBook"):
                result = self.controller.saveBook(book)
                if result:
                    # Will be handled by controller
                    pass
            else:
                print("Warning: Controller does not have saveBook method")
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