import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta

class BorrowWindow(tk.Toplevel):
    def __init__(self, parent, book_title, book_status, image_path, on_borrow):
        super().__init__(parent)
        self.title("Borrow Book")
        self.geometry("350x500")
        self.configure(bg="#f5f5dc")  # Warna latar belakang

        self.book_title = book_title
        self.book_status = book_status
        self.on_borrow = on_borrow

        # 🔹 HEADER
        header = tk.Frame(self, bg="#3b4f6d", height=50)
        header.pack(fill="x")

        back_btn = tk.Button(header, text="←", font=("Arial", 14, "bold"), bg="#3b4f6d", fg="white", borderwidth=0, command=self.destroy)
        back_btn.pack(side="left", padx=10, pady=5)

        tk.Label(header, text="📖 BOOK-KU!", font=("Arial", 16, "bold"), bg="#3b4f6d", fg="white").pack(pady=5)

        # 🔹 FRAME KONTEN UTAMA
        content_frame = tk.Frame(self, bg="#dce3c5", bd=2, relief="ridge")
        content_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # 🔹 GAMBAR BUKU
        try:
            img = Image.open(image_path)
            img = img.resize((120, 180), Image.Resampling.LANCZOS)
            self.book_img = ImageTk.PhotoImage(img)

            img_label = tk.Label(content_frame, image=self.book_img, bg="#dce3c5")
            img_label.pack(pady=10)
        except Exception as e:
            print("Error loading image:", e)

        # 🔹 INFORMASI BUKU
        tk.Label(content_frame, text=f"📚 Judul: {self.book_title}", font=("Arial", 12, "bold"), bg="#dce3c5").pack(pady=2)
        tk.Label(content_frame, text=f"📌 Status: {self.book_status}", font=("Arial", 12), bg="#dce3c5").pack(pady=2)

        self.borrow_date = datetime.today().strftime("%Y-%m-%d")
        self.return_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")

        tk.Label(content_frame, text=f"📅 Tanggal Peminjaman: {self.borrow_date}", font=("Arial", 11), bg="#dce3c5").pack(pady=2)
        tk.Label(content_frame, text=f"🚀 Kembali Sebelum: {self.return_date}", font=("Arial", 11, "bold"), bg="#dce3c5", fg="red").pack(pady=2)

        # 🔹 TOMBOL BORROW
        borrow_btn = tk.Button(content_frame, text="BORROW", font=("Arial", 12, "bold"), bg="green", fg="white", width=15, command=self.confirm_borrow)
        borrow_btn.pack(pady=15)

    def confirm_borrow(self):
        if self.book_status == "Tersedia":
            with open("../data/peminjaman.txt", "a") as file:
                file.write(f"{self.book_title}, {self.borrow_date}, {self.return_date}\n")

            self.on_borrow(self.book_title)  # Callback update status
            messagebox.showinfo("Sukses", f"Anda telah meminjam '{self.book_title}'!")
            self.destroy()
        else:
            messagebox.showwarning("Maaf", "Buku ini sedang dipinjam!")

# Contoh pemanggilan
if __name__ == "__main__":
    def update_status(title):
        print(f"Status buku {title} diperbarui!")

    root = tk.Tk()
    root.withdraw()

    borrow_win = BorrowWindow(root, "Harry Potter", "Tersedia", "harry_potter.jpg", update_status)
    borrow_win.mainloop()
