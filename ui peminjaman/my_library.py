import tkinter as tk
from tkinter import messagebox
import os

class MyLibraryWindow(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("My Library")
        self.geometry("500x400")
        self.configure(bg="white")

        # Label judul
        tk.Label(self, text="My Library", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Frame untuk daftar buku
        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Load daftar buku dari file
        self.load_books()
    
    def load_books(self):
        """Membaca data peminjaman dari file dan menampilkannya"""
        file_path = "../data/peminjaman.txt"
        if not os.path.exists(file_path):
            tk.Label(self.list_frame, text="No borrowed or booked books.", font=("Arial", 12), bg="white").pack()
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        if not lines:
            tk.Label(self.list_frame, text="No borrowed or booked books.", font=("Arial", 12), bg="white").pack()
            return

        for line in lines:
            data = line.strip().split(", ")
            if len(data) == 3:
                book_title, borrow_date, return_date = data
                self.add_book_entry(book_title, borrow_date, return_date)
    
    def add_book_entry(self, title, borrow_date, return_date):
        """Menampilkan buku dalam daftar My Library"""
        frame = tk.Frame(self.list_frame, bg="lightgray", padx=10, pady=5)
        frame.pack(pady=5, fill=tk.X)

        tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg="lightgray").pack(anchor="w")
        tk.Label(frame, text=f"Borrowed: {borrow_date} - Return by: {return_date}", font=("Arial", 10), bg="lightgray").pack(anchor="w")

        return_button = tk.Button(frame, text="Return", bg="red", fg="white", command=lambda: self.return_book(title, frame))
        return_button.pack(anchor="e", padx=10)

    def return_book(self, title, frame):
        """Menghapus buku yang dikembalikan dari file dan UI"""
        file_path = "../data/peminjaman.txt"
        with open(file_path, "r") as file:
            lines = file.readlines()

        with open(file_path, "w") as file:
            for line in lines:
                if not line.startswith(title):
                    file.write(line)
        
        frame.destroy()
        messagebox.showinfo("Success", f"You have returned '{title}'.")

# Contoh pemanggilan
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window utama

    my_library = MyLibraryWindow(root)
    my_library.mainloop()
