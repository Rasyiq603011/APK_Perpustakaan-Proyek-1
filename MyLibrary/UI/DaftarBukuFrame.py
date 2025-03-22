import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import math


# Create our own Tooltip class instead of importing from tkcalendar
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Create a toplevel window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        # Create the tooltip content
        label = tk.Label(self.tooltip, text=self.text,
                         background="#1E1E1E", foreground="white",
                         relief="solid", borderwidth=1, padx=5, pady=3)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DataBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="#1E1E1E", corner_radius=0)  # Dark background

        self.controller = controller
        self.MyLibrary = controller.bookManager

        self.search_query = ""
        self.selected_genre = None  # Ubah dari list kosong menjadi None
        self.selected_status = None  # Ubah dari list kosong menjadi None

        # Pagination settings
        self.books_per_page = 50  # 10 rows of 5 books
        self.current_page = 1
        self.total_pages = 1

        # Create main container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Header
        self.rowconfigure(1, weight=0)  # Search & Filter
        self.rowconfigure(2, weight=1)  # Content / Book Grid
        self.rowconfigure(3, weight=0)  # Pagination controls

        # Set up the UI components
        self.setup_header()
        self.setup_misc_bar()
        self.setup_content_area()
        self.setup_pagination()

        # Populate grid with books
        self.populate_book_grid()

    # =================== WIDGET FACTORY FUNCTIONS ===================

    def create_button(self, parent, text, command=None, fg_color="#6200EA", hover_color="#5000D0",
                      text_color="white", font_size=14, corner_radius=10, width=100, height=36,
                      font_weight="normal", **kwargs):
        """Membuat tombol dengan styling yang konsisten"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(family="Arial", size=font_size, weight=font_weight),
            corner_radius=corner_radius,
            width=width,
            height=height,
            **kwargs
        )

    def create_label(self, parent, text, font_size=14, text_color="white", font_weight="normal",
                     **kwargs):
        """Membuat label dengan styling yang konsisten"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(family="Arial", size=font_size, weight=font_weight),
            text_color=text_color,
            **kwargs
        )

    def create_entry(self, parent, placeholder_text="", width=300, height=36, **kwargs):
        """Membuat entry field dengan styling yang konsisten"""
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder_text,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            border_color="#666666",
            text_color="white",
            corner_radius=6,
            width=width,
            height=height,
            **kwargs
        )

    def create_frame(self, parent, fg_color="#2B2B2B", corner_radius=0, height=None, **kwargs):
        """Membuat frame dengan styling yang konsisten"""
        frame = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=corner_radius,
            **kwargs
        )

        if height:
            frame.configure(height=height)
            frame.pack_propagate(False)

        return frame

    # =================== COMPONENT SETUP FUNCTIONS ===================

    def setup_header(self):
        """Membangun header aplikasi"""
        self.header_frame = self.create_frame(self, fg_color="#232323", height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # Back button
        back_btn = self.create_button(
            self.header_frame,
            text="Back",
            command=lambda: self.controller.showFrame("MainMenuFrame")  # Added back button command
        )
        back_btn.pack(side="left", padx=20, pady=12)

        # Title
        title_label = self.create_label(
            self.header_frame,
            text="DAFTAR BUKU",
            font_size=28,
            font_weight="bold"
        )
        title_label.pack(side="left", padx=28, pady=12)

        # Add Book button
        self.add_btn = self.create_button(
            self.header_frame,
            text="+ Tambah Buku",
            command=lambda: self.controller.showFrame("AddBookFrame"),
            font_weight="bold",
            height=40,
            width=150
        )
        self.add_btn.pack(side="right", padx=20, pady=12)

    def setup_misc_bar(self):
        """Membangun bar pencarian"""
        search_filter_frame = self.create_frame(self, fg_color="#2B2B2B", height=80)
        search_filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 10))

        # Frame pencarian
        search_frame = self.create_frame(search_filter_frame, fg_color="transparent")
        search_frame.pack(side="left", fill="both", padx=20, pady=10)

        search_label = self.create_label(
            search_frame,
            text="Search :",
            font_size=14
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_entry = self.create_entry(
            search_frame,
            placeholder_text="Cari buku",
            width=300,
            height=36
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Frame filter
        filter_frame = self.create_frame(search_filter_frame, fg_color="transparent")
        filter_frame.pack(side="right", fill="both", padx=20, pady=10)

        # Gunakan dropdown genre kustom
        self.setup_genre_filter(filter_frame)

        # Status filter tetap menggunakan CTkOptionMenu standar
        status_label = self.create_label(
            filter_frame,
            text="Status:",
            font_size=14
        )
        status_label.pack(side="left", padx=(0, 10))

        status_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Available", "Borrowed", "Booked"],
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            button_color="#6200EA",
            button_hover_color="#5000D0",
            dropdown_fg_color="#1E1E1E",
            text_color="white",
            width=120,
            height=36,
            command=self.on_status_filter_change
        )
        status_dropdown.pack(side="left", padx=(0, 20))
        status_dropdown.set("All")

    def setup_genre_filter(self, parent_frame):
        """Membuat filter genre kustom dengan kemampuan scrolling"""
        # Frame untuk filter genre
        genre_filter_frame = self.create_frame(parent_frame, fg_color="transparent")
        genre_filter_frame.pack(side="left", fill="y", padx=(0, 20))

        # Label genre
        genre_label = self.create_label(
            genre_filter_frame,
            text="Genre:",
            font_size=14
        )
        genre_label.pack(side="left", padx=(0, 10))

        # Variabel untuk menyimpan genre yang terpilih
        self.genre_text = tk.StringVar()
        self.genre_text.set("All Genre")

        # Frame container untuk dropdown
        self.dropdown_container = self.create_frame(
            genre_filter_frame,
            fg_color="#1E1E1E",
            corner_radius=6
        )
        self.dropdown_container.pack(side="left")

        # Tombol dropdown utama
        self.genre_button = ctk.CTkButton(
            self.dropdown_container,
            textvariable=self.genre_text,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            text_color="white",
            hover_color="#333333",
            width=120,
            height=36,
            corner_radius=6,
            command=self.toggle_genre_dropdown
        )
        self.genre_button.pack(fill="x", expand=True)

        # Indikator dropdown (panah bawah)
        self.dropdown_indicator = ctk.CTkLabel(
            self.genre_button,
            text="▼",
            text_color="#AAAAAA",
            font=ctk.CTkFont(size=9)
        )
        self.dropdown_indicator.place(relx=0.9, rely=0.5, anchor="center")

        # Frame dropdown yang dapat di-scroll (awalnya tersembunyi)
        self.dropdown_frame = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#444444",
            corner_radius=6
        )

        # Membuat frame scrollable untuk daftar genre
        self.genre_list_frame = ctk.CTkScrollableFrame(
            self.dropdown_frame,
            fg_color="transparent",
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#666666",
            width=200,
            height=300  # Tinggi maksimal dropdown
        )
        self.genre_list_frame.pack(fill="both", expand=True)

        # Dropdown terbuka atau tidak
        self.is_dropdown_open = False

        # Populate genre options (akan dipanggil saat perlu menampilkan dropdown)

    def populate_genre_options(self):
        """Mengisi dropdown dengan opsi genre"""
        # Hapus semua item yang ada
        for widget in self.genre_list_frame.winfo_children():
            widget.destroy()

        # Tambahkan opsi "All Genre"
        all_genre_btn = ctk.CTkButton(
            self.genre_list_frame,
            text="All Genre",
            fg_color="transparent",
            hover_color="#333333",
            text_color="white",
            height=30,
            anchor="w",
            command=lambda: self.select_genre("All Genre")
        )
        all_genre_btn.pack(fill="x", padx=5, pady=2)

        # Tambahkan semua genre yang tersedia
        genres = self.get_available_genres()
        for genre in genres:
            truncated_genre = self.truncate_text(genre, 25)
            genre_btn = ctk.CTkButton(
                self.genre_list_frame,
                text=truncated_genre,
                fg_color="transparent",
                hover_color="#333333",
                text_color="white",
                height=30,
                anchor="w",
                command=lambda g=genre: self.select_genre(g)
            )
            genre_btn.pack(fill="x", padx=5, pady=2)

            # Add tooltip functionality for truncated genres
            if truncated_genre != genre:
                self.create_tooltip(genre_btn, genre)

    def toggle_genre_dropdown(self):
        """Menampilkan atau menyembunyikan dropdown genre"""
        if not self.is_dropdown_open:
            # Posisikan dropdown di bawah tombol
            x = self.genre_button.winfo_rootx()
            y = self.genre_button.winfo_rooty() + self.genre_button.winfo_height()

            self.dropdown_frame.place(x=x, y=y)
            self.populate_genre_options()  # Isi dropdown dengan genre
            self.is_dropdown_open = True

            # Bind event untuk menutup dropdown saat klik di luar
            self.bind_clickaway = self.winfo_toplevel().bind("<Button-1>", self.close_dropdown_if_clickaway)
        else:
            self.close_dropdown()

    def close_dropdown_if_clickaway(self, event):
        """Menutup dropdown jika klik di luar area dropdown"""
        if not (self.dropdown_frame.winfo_containing(event.x_root, event.y_root) or
                self.genre_button.winfo_containing(event.x_root, event.y_root)):
            self.close_dropdown()

    def close_dropdown(self):
        """Menutup dropdown genre"""
        if self.is_dropdown_open:
            self.dropdown_frame.place_forget()
            self.is_dropdown_open = False

            # Unbind clickaway event
            if hasattr(self, 'bind_clickaway'):
                self.winfo_toplevel().unbind("<Button-1>", self.bind_clickaway)

    def select_genre(self, genre):
        """Menangani pemilihan genre"""
        self.genre_text.set(genre)
        if genre == "All Genre":
            self.selected_genre = None
        else:
            self.selected_genre = genre

        self.close_dropdown()
        self.current_page = 1
        self.load_books()

    def setup_content_area(self):
        """Menyiapkan area konten untuk grid buku"""
        # Content frame
        self.content_frame = self.create_frame(self, fg_color="#1E1E1E")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # Create scrollable frame for books
        self.book_container = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#1E1E1E",
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#666666"
        )
        self.book_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Book grid inside scrollable container
        self.book_grid = self.create_frame(self.book_container, fg_color="transparent")
        self.book_grid.pack(fill="both", expand=True)

    def setup_pagination(self):
        """Membangun kontrol paginasi"""
        self.pagination_frame = self.create_frame(self, fg_color="#232323", height=50)
        self.pagination_frame.grid(row=3, column=0, sticky="ew", padx=0, pady=0)

        # Configure grid columns
        columns = 5
        for i in range(columns):
            weight = 1 if i in [0, 4] else 0
            self.pagination_frame.columnconfigure(i, weight=weight)

        # Previous page button
        self.prev_btn = self.create_button(
            self.pagination_frame,
            text="<",
            command=self.previous_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=80,
            height=30
        )
        self.prev_btn.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Page indicator
        self.page_label = self.create_label(
            self.pagination_frame,
            text=f"Page {self.current_page} of {self.total_pages}",
            font_size=12
        )
        self.page_label.grid(row=0, column=2, padx=10, pady=10)

        # Next page button
        self.next_btn = self.create_button(
            self.pagination_frame,
            text=">",
            command=self.next_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=80,
            height=30
        )
        self.next_btn.grid(row=0, column=3, padx=(10, 5), pady=10)

    # =================== BOOK CARD FUNCTIONS ===================

    def create_book_card(self, book):
        """Membuat kartu buku individual"""
        # Create book frame - card-like appearance
        book_frame = self.create_frame(
            self.book_grid,
            fg_color="#2B2B2B",
            corner_radius=10,
            border_width=0
        )

        # Load book cover
        img = self.MyLibrary.LoadCover(book.get('ISBN', ''))

        # Book cover button
        btn = ctk.CTkButton(
            book_frame,
            image=img,
            text="",
            fg_color="transparent",
            hover_color="#3D3D3D",
            border_width=0,
            command=lambda b=book: self.controller.showBookDetail(b)
        )
        btn.image = img  # Keep reference
        btn.pack(padx=5, pady=5, fill="x")

        # Book title (truncate if too long)
        title = book.get('Judul', 'Judul Tidak Ada')
        title_truncated = self.truncate_text(title, 20)

        title_label = self.create_label(
            book_frame,
            text=title_truncated,
            font_size=14,
            font_weight="bold",
            wraplength=120,
            anchor="center"
        )
        title_label.pack(padx=5, pady=5, fill="x")

        # Add tooltip for truncated titles
        if title_truncated != title:
            self.create_tooltip(title_label, title)

        # Author (optional)
        author = book.get('Penulis', '')
        if author:
            author_truncated = self.truncate_text(author, 25)

            author_label = self.create_label(
                book_frame,
                text=author_truncated,
                text_color="#AAAAAA",
                font_size=12,
                wraplength=120,
                anchor="center"
            )
            author_label.pack(padx=5, pady=(0, 5), fill="x")

            # Add tooltip for truncated author names
            if author_truncated != author:
                self.create_tooltip(author_label, author)

            # Status label
            status = book.get('Status', 'Unknown')
            status_color = self.get_status_color(status)

            status_label = self.create_label(
                book_frame,
                text=status,
                font_size=12,
                font_weight="bold",
                text_color=status_color
            )
            status_label.pack(padx=10, pady=(0, 10))

        return book_frame

    def truncate_text(self, text, max_length):
        """Memotong teks jika terlalu panjang"""
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    def get_status_color(self, status):
        """Mendapatkan warna berdasarkan status buku"""
        if status == "Available":
            return "#4CAF50"  # Green
        elif status == "Booked":
            return "#FF6D00"  # Orange
        else:
            return "#F44336"  # Red

    # =================== PAGINATION FUNCTIONS ===================

    def update_pagination_info(self, total_books):
        """Update informasi paginasi berdasarkan jumlah total buku"""
        self.total_pages = math.ceil(total_books / self.books_per_page)
        # Hindari halaman 0
        if self.total_pages < 1:
            self.total_pages = 1

        self.page_label.configure(text=f"Page {self.current_page} of {self.total_pages}")

        # Update button states
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.total_pages else "disabled")

    def get_page_slice(self, all_books):
        """Mendapatkan potongan data untuk halaman saat ini"""
        start_idx = (self.current_page - 1) * self.books_per_page
        end_idx = min(start_idx + self.books_per_page, len(all_books))
        return all_books.iloc[start_idx:end_idx]

    def next_page(self):
        """Pindah ke halaman berikutnya"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_books()  # Gunakan load_books daripada populate_book_grid

    def previous_page(self):
        """Pindah ke halaman sebelumnya"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_books()  # Gunakan load_books daripada populate_book_grid

    # =================== GRID MANAGEMENT FUNCTIONS ===================

    def populate_book_grid(self):
        """Mengisi grid dengan buku-buku untuk halaman saat ini"""
        # Metode ini digunakan untuk populasi awal dan refresh total
        # Clear existing content
        for widget in self.book_grid.winfo_children():
            widget.destroy()

        # Get all books from manager
        all_books = self.controller.getBook()

        if all_books is None or len(all_books) == 0:
            self.show_no_books_message()
            return

        # Update pagination information
        self.update_pagination_info(len(all_books))

        # Get books for current page
        page_books = self.get_page_slice(all_books)

        # Grid configuration
        cols = 5  # Number of books per row
        for i in range(cols):
            self.book_grid.columnconfigure(i, weight=1)

        # Display books in grid
        for i, (_, book) in enumerate(page_books.iterrows()):
            row = i // cols
            col = i % cols

            # Create book card
            book_card = self.create_book_card(book)
            book_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def load_books(self):
        """Memuat ulang daftar buku berdasarkan pencarian, genre, dan status dengan perbaikan bug."""
        # Hapus semua buku yang saat ini ada di halaman
        for widget in self.book_grid.winfo_children():
            widget.destroy()

        # Ambil semua buku yang sudah difilter
        filtered_books = self.get_filtered_books()

        if filtered_books is None or len(filtered_books) == 0:
            self.show_no_books_message()
            return

        # Hitung paginasi setelah memastikan buku tersedia
        self.update_pagination_info(len(filtered_books))

        # Ambil buku untuk halaman saat ini
        start_idx = (self.current_page - 1) * self.books_per_page
        end_idx = min(start_idx + self.books_per_page, len(filtered_books))
        page_books = filtered_books.iloc[start_idx:end_idx]

        # Konfigurasi grid tampilan buku
        cols = 5  # 5 buku per baris
        for i in range(cols):
            self.book_grid.columnconfigure(i, weight=1)

        # Tampilkan buku di grid
        for i, (_, book) in enumerate(page_books.iterrows()):
            row = i // cols
            col = i % cols

            book_card = self.create_book_card(book)
            book_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def show_no_books_message(self):
        """Menampilkan pesan jika tidak ada buku"""
        no_books_label = self.create_label(
            self.book_grid,
            text="Tidak ada buku yang tersedia",
            fg_color="transparent",  # Ubah dari "black" ke "transparent"
            font_size=14
        )
        no_books_label.pack(pady=50)

    def get_filtered_books(self):
        """Memfilter buku berdasarkan pencarian, genre, dan status."""
        if not hasattr(self.controller, 'bookManager') or not hasattr(self.controller.bookManager, 'getBook'):
            return None

        books = self.controller.getBook()  # Menggunakan controller.getBook() bukan bookManager.getBook()

        if books is None or books.empty:
            return None

        # Apply search filter
        if isinstance(self.search_query, str) and self.search_query.strip():  # Pastikan tidak kosong
            search_columns = ['Judul', 'Penulis', 'Penerbit', 'ISBN', 'Kategori']
            available_columns = [col for col in search_columns if col in books.columns]

            if available_columns:  # Pastikan kolom tersedia sebelum melakukan apply
                mask = books[available_columns].apply(
                    lambda col: col.astype(str).str.contains(self.search_query, case=False, na=False)
                ).any(axis=1)

                books = books[mask]

        # Apply genre filter
        if self.selected_genre is not None and 'Kategori' in books.columns:
            books = books[books['Kategori'].astype(str) == self.selected_genre]  # Gunakan == bukan isin

        # Apply status filter
        if self.selected_status is not None and 'Status' in books.columns:
            books = books[books['Status'] == self.selected_status]  # Gunakan == bukan isin

        return books

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget with the specified text"""
        # Use our custom Tooltip class instead of CalendarTooltip
        tooltip = Tooltip(widget, text)
        return tooltip

    def on_search_change(self, event=None):
        """Handle search input changes"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_books()

    def get_available_genres(self):
        if hasattr(self.controller, 'bookManager') and hasattr(self.controller.bookManager, 'getBook'):
            books = self.controller.getBook()  # Gunakan controller.getBook()
            if books is not None and 'Kategori' in books.columns:
                genre = sorted(books['Kategori'].astype(str).unique().tolist())
                return genre
        return []

    def on_genre_filter_change(self, choice):
        """Handle genre filter changes"""
        if choice == "All Genre":
            self.selected_genre = None
        else:
            self.selected_genre = choice  # Simpan sebagai string tunggal, bukan list
        self.current_page = 1
        self.load_books()

    def on_status_filter_change(self, choice):
        """Handle status filter changes"""
        if choice == "All":
            self.selected_status = None
        else:
            self.selected_status = choice  # Simpan sebagai string tunggal, bukan list
        self.current_page = 1  # Reset to first page
        self.load_books()


if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Daftar Buku")
    root.geometry("1024x768")
