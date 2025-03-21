import tkinter as tk
from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk
import pandas as pd
import os

class HomePage(tk.Frame):
    def __init__(self, parent, on_book_selected):
        super().__init__(parent)
        self.configure(bg="white")

        self.on_book_selected = on_book_selected  # Callback saat buku diklik

        # Judul halaman
        tk.Label(self, text="Digital Library", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        # Frame utama untuk buku dengan scrolling
        self.canvas = Canvas(self, bg="white", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Load dan tampilkan buku
        self.load_books()

        # Update ukuran frame agar scrolling berfungsi
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def load_books(self):
        """
        Membaca data buku dari data_buku.xlsx dan menampilkan cover + judul buku.
        """
        try:
            df = pd.read_excel("../data/data_buku.xlsx")
        except FileNotFoundError:
            tk.Label(self.scroll_frame, text="Book data not found!", fg="red", font=("Arial", 12)).pack(pady=10)
            return

        row, col = 0, 0
        for _, book in df.iterrows():
            isbn = str(book["ISBN"])
            title = book["Judul Buku"]

            # Path cover buku
            cover_path = f"../assets/covers/{isbn}.jpg"
            if not os.path.exists(cover_path):
                cover_path = "../assets/covers/default.jpg"  # Placeholder jika tidak ada

            # Load gambar cover
            img = Image.open(cover_path).resize((100, 150))
            img = ImageTk.PhotoImage(img)

            # Frame untuk setiap buku
            book_frame = tk.Frame(self.scroll_frame, bg="white", padx=10, pady=10)
            book_frame.grid(row=row, column=col, padx=10, pady=10)

            # Tombol gambar buku
            btn = tk.Button(book_frame, image=img, command=lambda t=title: self.on_book_selected(t), border=0)
            btn.image = img  # Simpan referensi agar gambar tidak hilang
            btn.pack()

            # Label judul buku
            tk.Label(book_frame, text=title, font=("Arial", 10), wraplength=100, bg="white").pack()

            # Grid layout max 3 kolom
            col += 1
            if col >= 3:
                col = 0
                row += 1

# Contoh pemanggilan
if __name__ == "__main__":
    def show_book_info(title):
        print(f"Selected book: {title}")

    root = tk.Tk()
    root.geometry("400x600")
    homepage = HomePage(root, show_book_info)
    homepage.pack(fill="both", expand=True)
    root.mainloop()
