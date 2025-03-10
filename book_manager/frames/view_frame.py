import tkinter as tk
from tkinter import ttk, messagebox
from book_manager.constants import FONTS
from book_manager.utils import read_data, delete_book

class ViewBooksFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        tk.Label(
            self, 
            text="Daftar Buku", 
            font=FONTS["subheader"]
        ).pack(pady=10)
        
        # Back button (top left)
        back_button = tk.Button(
            self,
            text="← Kembali",
            command=lambda: controller.show_frame("HomeFrame")
        )
        back_button.place(x=10, y=10)
        
        # User status (top right)
        self.user_label = tk.Label(
            self,
            text="",
            font=FONTS["normal"]
        )
        self.user_label.place(relx=0.95, y=10, anchor="ne")
        
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(search_frame, text="Cari Buku:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search)
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=5)
        
        # Frame for book data display
        self.data_frame = ttk.LabelFrame(self, text="Data Buku")
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview to display book data
        self.tree = ttk.Treeview(self.data_frame, columns=("ID", "Judul", "Penulis", "Tahun","Penerbit", "Genre","ISBN"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Judul", text="Judul")
        self.tree.heading("Penulis", text="Penulis")
        self.tree.heading("Tahun", text="Tahun")
        self.tree.heading("Penerbit", text="Penerbit")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("ISBN", text="ISBN")
        
        
        # Column widths
        self.tree.column("ID", width=50)
        self.tree.column("Judul", width=200)
        self.tree.column("Penulis", width=150)
        self.tree.column("Tahun", width=100)
        self.tree.column("Penerbit", width=150)
        self.tree.column("Genre", width=150)
        self.tree.column("ISBN", width=150)
        
        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Place the treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons
        self.action_frame = ttk.Frame(self)
        self.action_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(
            self.action_frame, 
            text="Refresh Data", 
            command=self.refresh_data
        ).pack(side="left", padx=5)
        
        # Admin-only buttons
        self.edit_button = ttk.Button(
            self.action_frame, 
            text="Edit Buku", 
            command=self.edit_selected_book,
            state=tk.DISABLED  # Disabled by default
        )
        self.edit_button.pack(side="left", padx=5)
        
        self.delete_button = ttk.Button(
            self.action_frame, 
            text="Hapus Buku", 
            command=self.hapus_buku,
            state=tk.DISABLED  # Disabled by default
        )
        self.delete_button.pack(side="left", padx=5)
        
        # Store the original data for searching
        self.all_books = []
    
    def on_show_frame(self):
        """Dipanggil saat frame ini ditampilkan"""
        self.refresh_data()
        self.update_ui_for_role()
    
    def update_ui_for_role(self):
        """Update tampilan UI berdasarkan peran pengguna"""
        if self.controller.auth_manager.is_authenticated():
            if self.controller.auth_manager.is_admin_user():
                # Admin mode
                self.user_label.config(text="Mode: Administrator")
                self.edit_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
            else:
                # User mode
                self.user_label.config(text="Mode: User (Hanya Lihat)")
                self.edit_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
    
    def refresh_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Read data from file
        try:
            df = read_data()
            
            # Store all books for searching
            self.all_books = []
            
            # Insert data to treeview
            for _, row in df.iterrows():
                book_data = (row["ID"], row["Judul"], row["Penulis"], row["Tahun"],row["Penerbit"], row["Genre"], row["ISBN"])
                self.all_books.append(book_data)
                self.tree.insert("", "end", values=book_data)
                
            # Reset search
            self.search_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca data: {str(e)}")
    
    def update_search(self, *args):
        search_term = self.search_var.get().lower()
        
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filter and reload
        for book in self.all_books:
            # Search in all columns
            if (search_term in str(book[0]).lower() or  # ID
                search_term in str(book[1]).lower() or  # Judul
                search_term in str(book[2]).lower() or  # Penulis
                search_term in str(book[3]).lower()):   # Tahun
                self.tree.insert("", "end", values=book)
    
    def edit_selected_book(self):
        if not self.controller.auth_manager.is_admin_user():
            messagebox.showwarning("Akses Ditolak", "Hanya administrator yang dapat mengedit buku.")
            return
            
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin diedit!")
            return
        
        # Get data from selected item
        item = selected_items[0]
        values = self.tree.item(item, "values")
        
        # Pass the data to the update frame
        update_frame = self.controller.frames["UpdateBookFrame"]
        update_frame.populate_fields(values)
        
        # Show the update frame
        self.controller.show_frame("UpdateBookFrame")
    
    def hapus_buku(self):
        if not self.controller.auth_manager.is_admin_user():
            messagebox.showwarning("Akses Ditolak", "Hanya administrator yang dapat menghapus buku.")
            return
            
        # Check if an item is selected
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin dihapus!")
            return
        
        # Get ID from the selected item
        item = selected_items[0]
        values = self.tree.item(item, "values")
        id_buku = int(values[0])
        
        # Confirm deletion
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus buku dengan ID {id_buku}?")
        if not confirm:
            return
        
        # Delete the book
        success = delete_book(id_buku)
        
        if success:
            # Refresh all frames
            self.controller.refresh_all_frames()
            messagebox.showinfo("Sukses", "Buku berhasil dihapus!")
        else:
            messagebox.showwarning("Peringatan", "ID buku tidak ditemukan atau terjadi kesalahan.")