import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import shutil
from PIL import Image

class UpdateBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.configure(fg_color="#1E1E1E", corner_radius=0) 
        
        self.book = None
        self.selected_cover_path = None  
        if hasattr(controller, 'assets_dir'):
            self.cover_dir = os.path.join(controller.assets_dir, "Cover")
            self.default_cover = os.path.join(controller.assets_dir, "IMG.jpg")
        else:
            self.cover_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "Cover")
            self.default_cover = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "IMG.jpg")


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
                fg_color="#6200EA",
                hover_color= "#5000D0",
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
                text="UPDATE BUKU", 
                font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
                text_color="white"
        )
        self.title_label.grid(row=0, column=1)
            
    def Content(self):
    # ===== CONTENT SECTION =====
    # Form container
        self.form_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Slightly lighter background for form
        self.form_container.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=20)
            
        self.form_container.columnconfigure(0, weight= 0)
        self.form_container.columnconfigure(1, weight= 1)
        self.form_container.columnconfigure(2, weight= 0)
        self.form_container.columnconfigure(3, weight= 1)

        self.create_form_fields()
            
    # Cover container (right side) - more compact
        self.cover_container = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)  # Matching form container color
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
                fg_color="#F44336",
                hover_color="#D32F2F",
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=14),
                corner_radius=10,
                height=40,
                width=120
            )
        self.cancelBtn.pack(side="left", padx=40, pady=10)
            
            # Update button - Right side
        self.updateBtn = ctk.CTkButton(
                self.footer,
                text="Update book", 
                command=self.update_book,
                fg_color="#4CAF50", 
                hover_color="#388E3C",
                text_color="white",
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
                text_color="white",
                anchor="w",
                width=70  # Reduced width
            )
            label.grid(row=row, column=col, padx=(20), pady=15, sticky="w")
            
            if field_name == "Kategori":

                dropdown = ctk.CTkOptionMenu(
                    self.form_container,
                    values=["Science Fiction","Young Adult","Graphic Novels","Fiction","Non-Fiction", "Education","Arts & Humanities","Religion & Spirituality", "Social Sciences","Nature & Environment"],
                    font=ctk.CTkFont(family="Arial", size=14),
                    fg_color="#1E1E1E",
                    button_color="#6200EA",
                    button_hover_color="#5000D0",
                    dropdown_fg_color="#1E1E1E",
                    text_color="white",
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
                    fg_color="#3D3D3D",
                    border_color="#666666",
                    text_color="white",
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
            text_color="white",
            anchor="w"
        )
        self.desc_label.grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")
        
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
        self.desc_text.grid(row=5, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="nsew")

        # Make the description row expandable
        self.form_container.rowconfigure(5, weight=1)
    
    def create_cover_section(self):
        
        # Cover title
        cover_title = ctk.CTkLabel(
            self.cover_container,
            text="Cover Buku",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        cover_title.pack(pady=(20, 10))
        
        self.cover_frame = ctk.CTkFrame(self.cover_container, fg_color="#F5F5F5", corner_radius=10)  # Light background for cover like in design
        self.cover_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Cover image label - using the recommended 180x270 ratio
        self.cover_label = ctk.CTkLabel(self.cover_frame, text="", image=None)
        self.cover_label.pack(padx=20, pady=20)
        
        # Update cover button
        self.upload_btn = ctk.CTkButton(
            self.cover_container,
            text="Upload cover",
            command=self.browse_cover,
            fg_color="#6200EA",
            hover_color="#5000D0", 
            text_color="white",
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
            text_color="#AAAAAA", 
            justify="center"
        )
        self.selected_file_label.pack()

        # Cover info
        info_frame = ctk.CTkFrame(self.cover_container, fg_color="#363636", corner_radius=8) 
        info_frame.pack(padx=20, pady=20, fill="x")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="Format: JPEG/JPG\nUkuran yang disarankan: 180x270 px",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#FFFFFF",
            justify="center"
        )
        info_text.pack(pady=15, padx=15)
        
    def load_book_data(self):
        if self.book is None:
            return
            
        # Debug: Print the keys and the ISBN value
        print(f"Book data keys: {self.book.keys()}")
        print(f"ISBN value: {self.book.get('ISBN', 'Not found')}")
    
        # Check if book is a pandas Series
        if hasattr(self.book, 'keys'):
            # Set values in entry fields
            for field_name in self.entries:
                if field_name in self.book and field_name != "Kategori":
                    self.entries[field_name].delete(0, "end")
                    self.entries[field_name].insert(0, str(self.book.get(field_name, "")))
                
            # Make ISBN field read-only
            self.entries["ISBN"].configure(state="disabled")
            
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
        # Modified to skip ISBN validation since it's read-only
        required_fields = ["Judul", "Penulis", "Penerbit", "Tahun", "Kategori", "Halaman"]
        
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
        
        # Get ISBN for cover file naming (read-only, but we still need the value)
        isbn = self.entries["ISBN"].get().strip()
        
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
            if hasattr(self.controller, "updateBook"):
                result = self.controller.updateBook(updated_book)
                if result:
                    # Button state is updated by the controller
                    pass
            else:
                print("Warning: Controller does not have updateBook method")
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
    root.title("Update Buku")  # Changed to reflect this is updating, not adding
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
        "Judul": "Laskar Pelangi",
        "Penulis": "Andrea Hirata",
        "Penerbit": "Bentang Pustaka",
        "Tahun": "2005",
        "Kategori": "Novel",
        "ISBN": "9789793062792",
        "Halaman": "529",
        "Deskripsi": "Novel ini bercerita tentang kehidupan 10 anak dari keluarga miskin yang bersekolah di sebuah sekolah Muhammadiyah di Belitung yang penuh dengan keterbatasan."
    }
    
    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")
    
    control = TestController()

    app = UpdateBookFrame(frame, control)
    app.book = sample_book
    app.load_book_data()  # Populate form with book data
    app.pack(expand=True, fill="both")
    
    root.mainloop()