import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import math
import pandas as pd

from MyLibrary.constans import CATEGORY_MAPPING


def categorize_genre(genre):
    for category, keywords in CATEGORY_MAPPING.items():
        if genre in keywords:
            return category
    return "Other"


def load_genre_data():
    file_path = "Asset/data_buku_2.xlsx"  # Menggunakan file data_buku_2.xlsx
    df = pd.read_excel(file_path)
    if "Kategori" in df.columns:
        df["Category"] = df["Kategori"].apply(categorize_genre)
        return df["Category"].unique().tolist()
    return []


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
        self.genre_options = load_genre_data()

        self.controller = controller
        self.MyLibrary = controller.bookManager

        self.search_query = ""
        self.selected_genre = None
        self.selected_status = None

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

        # Update genre dropdown with available genres
        self.update_genre_dropdown()

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

        # Configure grid for header frame
        self.header_frame.columnconfigure(0, weight=1)  # For left items
        self.header_frame.columnconfigure(1, weight=1)  # For center title
        self.header_frame.columnconfigure(2, weight=1)  # For right items

        # Back button
        back_btn = self.create_button(
            self.header_frame,
            text="Back",
            command=lambda: self.controller.showFrame("MainMenuFrame")
        )
        back_btn.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        # Title
        title_label = self.create_label(
            self.header_frame,
            text="DAFTAR BUKU",
            font_size=28,
            font_weight="bold"
        )
        title_label.grid(row=0, column=1, padx=28, pady=12)

        # Removed the Add Book button

    def setup_misc_bar(self):
        """Membangun bar pencarian menggunakan grid"""
        search_filter_frame = self.create_frame(self, fg_color="#2B2B2B", height=80)
        search_filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 10))

        # Configure grid
        search_filter_frame.columnconfigure(0, weight=1)  # Search section
        search_filter_frame.columnconfigure(1, weight=0)  # Genre filter
        search_filter_frame.columnconfigure(2, weight=0)  # Status filter

        # Frame pencarian
        search_frame = self.create_frame(search_filter_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Configure search frame grid
        search_frame.columnconfigure(0, weight=0)  # Label
        search_frame.columnconfigure(1, weight=1)  # Entry

        search_label = self.create_label(
            search_frame,
            text="Search :",
            font_size=14
        )
        search_label.grid(row=0, column=0, padx=(0, 10))

        self.search_entry = self.create_entry(
            search_frame,
            placeholder_text="Cari buku",
            width=300,
            height=36
        )
        self.search_entry.grid(row=0, column=1, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.start_search_timer)

        self.search_timer = None

        # Genre filter frame
        genre_frame = self.create_frame(search_filter_frame, fg_color="transparent")
        genre_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        genre_label = self.create_label(
            genre_frame,
            text="Genre:",
            font_size=14
        )
        genre_label.grid(row=0, column=0, padx=(0, 10))

        # Create the dropdown list with initial value "All Genre"
        self.genre_dropdown = ctk.CTkOptionMenu(
            genre_frame,
            values=["All Genre"],
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            button_color="#6200EA",
            button_hover_color="#5000D0",
            dropdown_fg_color="#1E1E1E",
            text_color="white",
            width=120,
            height=36,
            command=self.on_genre_filter_change
        )
        self.genre_dropdown.grid(row=0, column=1)
        self.genre_dropdown.set("All Genre")

        # Status filter frame
        status_frame = self.create_frame(search_filter_frame, fg_color="transparent")
        status_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        status_label = self.create_label(
            status_frame,
            text="Status:",
            font_size=14
        )
        status_label.grid(row=0, column=0, padx=(0, 10))

        status_dropdown = ctk.CTkOptionMenu(
            status_frame,
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
        status_dropdown.grid(row=0, column=1)
        status_dropdown.set("All")

    def update_genre_dropdown(self):
        """Update the genre dropdown with available genres"""
        # Get available genres
        genres = self.get_available_genres()

        # Create the dropdown values list with "All Genre" at the beginning
        dropdown_values = ["All Genre"] + genres

        # Update the dropdown menu with these values
        self.genre_dropdown.configure(values=dropdown_values)
        self.genre_dropdown.set("All Genre")

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
        self.pagination_frame.columnconfigure(0, weight=1)  # Left spacer
        self.pagination_frame.columnconfigure(1, weight=0)  # Navigation buttons
        self.pagination_frame.columnconfigure(2, weight=1)  # Right spacer with Go to components

        # Membuat frame untuk navigasi
        nav_buttons_frame = self.create_frame(self.pagination_frame, fg_color="transparent")
        nav_buttons_frame.grid(row=0, column=1, padx=0, pady=10)

        # First page button
        self.first_btn = self.create_button(
            nav_buttons_frame,
            text="<<",
            command=self.first_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=40,
            height=30
        )
        self.first_btn.pack(side="left", padx=(0, 0))

        # Previous page button - Setelah first button
        self.prev_btn = self.create_button(
            nav_buttons_frame,
            text="<",
            command=self.previous_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=40,
            height=30
        )
        self.prev_btn.pack(side="left", padx=(0, 10))

        # Page indicator
        self.page_label = self.create_label(
            nav_buttons_frame,
            text=f"Page {self.current_page} of {self.total_pages}",
            font_size=12
        )
        self.page_label.pack(side="left", padx=10)

        # Next page button
        self.next_btn = self.create_button(
            nav_buttons_frame,
            text=">",
            command=self.next_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=40,
            height=30
        )
        self.next_btn.pack(side="left", padx=(10, 0))

        # Last page button - Setelah next button
        self.last_btn = self.create_button(
            nav_buttons_frame,
            text=">>",
            command=self.last_page,
            fg_color="#333333",
            hover_color="#444444",
            font_size=12,
            corner_radius=8,
            width=40,
            height=30
        )
        self.last_btn.pack(side="left", padx=(0, 0))

        # Create a frame for "Go to" components on the right
        goto_frame = self.create_frame(self.pagination_frame, fg_color="transparent")
        goto_frame.grid(row=0, column=2, padx=(0, 20), pady=10, sticky="e")

        # Go to page label - Di dalam goto_frame
        goto_label = self.create_label(
            goto_frame,
            text="Go to:",
            font_size=12
        )
        goto_label.pack(side="left", padx=(0, 5))

        # Page number entry - Sebelah kanan label
        self.page_entry = self.create_entry(
            goto_frame,
            placeholder_text="Page #",
            width=60,
            height=30
        )
        self.page_entry.pack(side="left", padx=(0, 5))

        # Go button - Sebelah kanan entry
        go_btn = self.create_button(
            goto_frame,
            text="Go",
            command=self.go_to_page,
            fg_color="#6200EA",
            hover_color="#5000D0",
            font_size=12,
            corner_radius=8,
            width=50,
            height=30
        )
        go_btn.pack(side="left")

        # Add Enter key binding to page entry
        self.page_entry.bind("<Return>", lambda event: self.go_to_page())

    # =================== BOOK CARD FUNCTIONS ===================

    def create_book_card(self, book):
        """Membuat kartu buku individual"""
        # Membuat frame buku
        book_frame = self.create_frame(
            self.book_grid,
            fg_color="#2B2B2B",
            corner_radius=10,
            border_width=0
        )

        book_frame.columnconfigure(0, weight=1)
        book_frame.rowconfigure(0, weight=0)  # Cover image
        book_frame.rowconfigure(1, weight=0)  # Title
        book_frame.rowconfigure(2, weight=0)  # Author
        book_frame.rowconfigure(3, weight=0)  # Status

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
        btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

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
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

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
            author_label.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")

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
            status_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

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
            self.load_books()

    def first_page(self):
        """Pindah ke halaman pertama"""
        if self.current_page != 1:
            self.current_page = 1
            self.load_books()

    def previous_page(self):
        """Pindah ke halaman sebelumnya"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_books()

    def last_page(self):
        """Pindah ke halaman terakhir"""
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.load_books()

    def go_to_page(self):
        """Menampilkan halaman sesuai user input"""
        try:
            # Mengambil halaman dari entry
            page_num = int(self.page_entry.get())

            # Check input
            if 1 <= page_num <= self.total_pages:
                self.current_page = page_num
                self.load_books()
                # Membersihkan entry
                self.page_entry.delete(0, tk.END)
            else:
                # Case untuk angka yang dimasukkan tidak valid
                self.show_page_error(f"Please enter a page number between 1 and {self.total_pages}")
        except ValueError:
            # Case untuk masukkan selain angka / integer
            self.show_page_error("Please enter a valid page number")

    def show_page_error(self, message):
        """Display error message for invalid page navigation"""
        # Create or update error tooltip near the page entry
        if hasattr(self, 'error_tooltip'):
            # Memperbaharui tooltip jika ada
            if self.error_tooltip.tooltip:
                self.error_tooltip.tooltip.destroy()
            self.error_tooltip.text = message
            self.error_tooltip.show_tooltip()
        else:
            # Membuat tooltip untuk error
            self.error_tooltip = Tooltip(self.page_entry, message)
            self.error_tooltip.show_tooltip()

        # Menampilkan tooltip error
        self.page_entry.after(2000,
                              lambda: self.error_tooltip.hide_tooltip() if hasattr(self, 'error_tooltip') else None)

        # Tampilan merah yang menandakan error di border
        original_border = self.page_entry.cget("border_color")
        self.page_entry.configure(border_color="#F44336")  # Red border
        self.page_entry.after(100, lambda: self.page_entry.configure(border_color=original_border))

    # =================== GRID MANAGEMENT FUNCTIONS ===================

    def populate_book_grid(self):
        """Mengisi grid dengan buku-buku untuk halaman saat ini"""
        # Metode ini digunakan untuk populasi awal dan refresh total
        for widget in self.book_grid.winfo_children():
            widget.destroy()

        # Get all books from manager
        all_books = self.controller.getBook()

        if all_books is None or len(all_books) == 0:
            self.show_no_books_message()
            return

        # Memperbaharui pagination
        self.update_pagination_info(len(all_books))

        # Mengambil buku untuk halaman saat ini
        page_books = self.get_page_slice(all_books)

        # Konfig grid
        cols = 5  # Number of books per row
        for i in range(cols):
            self.book_grid.columnconfigure(i, weight=1)

        # Menampilkan books di grid
        for i, (_, book) in enumerate(page_books.iterrows()):
            row = i // cols
            col = i % cols

            # Create book_card
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
        self.book_grid.columnconfigure(0, weight=1)
        self.book_grid.rowconfigure(0, weight=1)

        no_books_label = self.create_label(
            self.book_grid,
            text="Tidak ada buku yang tersedia",
            fg_color="transparent",
            font_size=14
        )
        no_books_label.grid(row=0, column=0, pady=50)

    def get_filtered_books(self):
        """Memfilter buku berdasarkan pencarian, genre, dan status."""
        if not hasattr(self.controller, 'bookManager') or not hasattr(self.controller.bookManager, 'getBook'):
            return None

        books = self.controller.getBook()

        if books is None or books.empty:
            return None

        # Apply search filter
        if isinstance(self.search_query, str) and self.search_query.strip():
            search_columns = ['Judul', 'Penulis', 'Penerbit', 'ISBN', 'Kategori']
            available_columns = [col for col in search_columns if col in books.columns]

            if available_columns:
                mask = books[available_columns].apply(
                    lambda col: col.astype(str).str.contains(self.search_query, case=False, na=False)
                ).any(axis=1)

                books = books[mask]

        # Apply genre filter - Ubah untuk menggunakan kategori dari CATEGORY_MAPPING
        if self.selected_genre is not None and 'Kategori' in books.columns:
            if self.selected_genre in CATEGORY_MAPPING:
                # Filter berdasarkan genre yang termasuk dalam kategori yang dipilih
                category_genres = CATEGORY_MAPPING[self.selected_genre]
                mask = books['Kategori'].astype(str).apply(lambda x: x in category_genres)
                books = books[mask]
            elif self.selected_genre == 'Other':
                # Filter semua genre yang tidak termasuk dalam kategori manapun
                all_mapped_genres = [genre for genres in CATEGORY_MAPPING.values() for genre in genres]
                mask = ~books['Kategori'].astype(str).isin(all_mapped_genres)
                books = books[mask]
            else:
                # Filter untuk kategori spesifik (jika tidak termasuk dalam CATEGORY_MAPPING)
                books = books[books['Kategori'].astype(str) == self.selected_genre]

        # Apply status filter
        if self.selected_status is not None and 'Status' in books.columns:
            books = books[books['Status'] == self.selected_status]

        return books

    def create_tooltip(self, widget, text):
        """Membuat text panjang dari text yang di truncated dengan tooltip custom"""
        tooltip = Tooltip(widget, text)
        return tooltip

    def start_search_timer(self, event=None):
        # Memulai timer untuk pencarian
        if self.search_timer is not None:
            self.after_cancel(self.search_timer)

        # Memulai ulang timer setelah 1 detik
        self.search_timer = self.after(1000, self.perform_search)

    def perform_search(self):
        """Program Search"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1
        self.load_books()

        # Reset timer
        self.search_timer = None

    def get_available_genres(self):
        """Mendapatkan daftar kategori dari CATEGORY_MAPPING"""
        # Gunakan kategori dari CATEGORY_MAPPING yang sudah didefinisikan
        categories = list(CATEGORY_MAPPING.keys())
        # Tambahkan 'Other' jika ada dalam data tetapi tidak dalam mapping
        if hasattr(self.controller, 'bookManager') and hasattr(self.controller.bookManager, 'getBook'):
            books = self.controller.getBook()
            if books is not None and 'Kategori' in books.columns:
                # Cek apakah ada kategori 'Other' dalam data
                for genre in books['Kategori'].astype(str).unique():
                    categorized = False
                    for category, keywords in CATEGORY_MAPPING.items():
                        if genre in keywords:
                            categorized = True
                            break
                    if not categorized and 'Other' not in categories:
                        categories.append('Other')
                        break
        return sorted(categories)

    def on_genre_filter_change(self, choice):
        """Mengatur perubahan dari filter genre"""
        if choice == "All Genre":
            self.selected_genre = None
        else:
            self.selected_genre = choice
        self.current_page = 1
        self.load_books()

    def on_status_filter_change(self, choice):
        """Mengatur perubahan dari filter status"""
        if choice == "All":
            self.selected_status = None
        else:
            self.selected_status = choice  # Simpan sebagai string tunggal, bukan list
        self.current_page = 1
        self.load_books()


if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Daftar Buku")
    root.geometry("1024x768")
