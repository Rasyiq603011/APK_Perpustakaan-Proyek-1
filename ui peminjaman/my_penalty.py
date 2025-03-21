import tkinter as tk
from tkinter import ttk

class MyPenalty(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        # Label Judul
        tk.Label(self, text="My Penalty", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Tabel untuk menampilkan daftar penalti
        columns = ("Judul Buku", "Tgl Seharusnya Kembali", "Hari Terlambat", "Total Penalti")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Tombol Refresh
        tk.Button(self, text="Refresh", command=self.load_penalty, bg="red", fg="white").pack(pady=10)

        # Muat data awal
        self.load_penalty()

    def load_penalty(self):
        """
        Memuat data penalti dari file penalty.txt ke dalam tabel.
        """
        self.tree.delete(*self.tree.get_children())  # Bersihkan tabel

        try:
            with open("../data/penalty.txt", "r") as file:
                for line in file:
                    data = line.strip().split(", ")
                    if len(data) == 4:
                        self.tree.insert("", "end", values=data)
        except FileNotFoundError:
            print("File penalty.txt tidak ditemukan!")

# Contoh pemanggilan
if __name__ == "__main__":
    root = tk.Tk()
    root.title("My Penalty")
    root.geometry("600x400")

    frame = MyPenalty(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()
