import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import os

class BookInformation(tk.Frame):
    def __init__(self, parent, book_title, on_borrow, on_back):
        super().__init__(parent)
        self.configure(bg="white")

        self.on_borrow = on_borrow  # Callback untuk borrow
        self.on_back = on_back      # Callback untuk kembali

        # Load data buku
        df = pd.read_excel("../data/data_buku.xlsx")
        book = df[df["Judul Buku"] == book_title].iloc[0]  # Ambil data buku

        isbn = str(book["ISBN"])
        author = book["Penulis Buku"]
        year = book["Tahun Terbit"]
        category = book["Kategori Buku"]
        pages = book["Halaman Buku"]
        description = book["Deskripsi Buku"]
        status = book["Status Buku"]

        # Path cover buku
        cover_path = f"../assets/covers/{isbn}.jpg"
        if not os.path.exists(cover_path):
            cover_path = "../assets/covers/default.jpg"

        # Load cover
        img = Image.open(cover_path).resize((150, 200))
        img = ImageTk.PhotoImage(img)

        # Layout
        tk.Button(self, text="← Back", command=self.on_back, bg="lightgray").pack(anchor="w", padx=10, pady=5)

        tk.Label(self, text=book_title, font=("Arial", 16, "bold"), wraplength=300, bg="white").pack(pady=5)
        tk.Label(self, image=img, bg="white").pack()
        self.cover_image = img  # Simpan referensi gambar agar tidak hilang

        # Detail Buku
        details = [
            f"Author: {author}",
            f"Year: {year}",
            f"Category: {category}",
            f"Pages: {pages}",
            f"Status: {status}"
        ]
        for detail in details:
            tk.Label(self, text=detail, font=("Arial", 10), bg="white").pack(pady=2)

        # Deskripsi
        tk.Label(self, text="Description:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=5)
        tk.Label(self, text=description, wraplength=350, justify="left", bg="white").pack(padx=20)

        # Tombol Borrow
        if status.lower() == "available":
            tk.Button(self, text="Borrow", command=lambda: self.on_borrow(book_title), bg="green", fg="white").pack(pady=10)

# Contoh Pemanggilan
if __name__ == "__main__":
    def borrow_book(title):
        print(f"Borrowing: {title}")

    def go_back():
        print("Back to homepage")

    root = tk.Tk()
    root.geometry("400x600")
    book_info = BookInformation(root, "Sample Book", borrow_book, go_back)
    book_info.pack(fill="both", expand=True)
    root.mainloop()
