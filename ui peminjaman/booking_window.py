import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # ✅ Import Kalender

class BookingWindow(tk.Toplevel):
    def __init__(self, parent, book_title, book_status, image_path):
        super().__init__(parent)
        self.title("BOOK-KU!")
        self.geometry("350x500")
        self.configure(bg="#f5f5dc")

        self.book_title = book_title
        self.book_status = book_status
        self.image_path = image_path

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

        # 🔹 INPUT TANGGAL PEMINJAMAN
        tk.Label(content_frame, text="📅 Pilih Tanggal Peminjaman:", font=("Arial", 11), bg="#dce3c5").pack(pady=2)

        self.borrow_date_entry = DateEntry(content_frame, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.borrow_date_entry.pack(pady=5)

        # 🔹 TANGGAL PENGEMBALIAN OTOMATIS
        self.return_date_label = tk.Label(content_frame, text="🚀 Tanggal Maksimal Pengembalian: -", font=("Arial", 11, "bold"), bg="#dce3c5", fg="red")
        self.return_date_label.pack(pady=2)

        # Update tanggal pengembalian otomatis ketika user memilih tanggal peminjaman
        self.borrow_date_entry.bind("<<DateEntrySelected>>", self.update_return_date)

        # 🔹 TOMBOL BOOKING
        borrow_btn = tk.Button(content_frame, text="BOOKING", font=("Arial", 12, "bold"), bg="orange", fg="white", width=15, command=self.confirm_booking)
        borrow_btn.pack(pady=15)

    def update_return_date(self, event):
        """Update tanggal pengembalian otomatis berdasarkan tanggal peminjaman + 7 hari"""
        borrow_date = datetime.strptime(self.borrow_date_entry.get(), "%Y-%m-%d")
        return_date = borrow_date + timedelta(days=7)
        self.return_date_label.config(text=f"🚀 Tanggal Maksimal Pengembalian: {return_date.strftime('%Y-%m-%d')}")

    def confirm_booking(self):
        borrow_date = self.borrow_date_entry.get()
        return_date = (datetime.strptime(borrow_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")

        if self.book_status.lower() == "dipinjam":
            messagebox.showwarning("Maaf", "Buku ini sedang dipinjam!")
        else:
            messagebox.showinfo("Sukses", f"Anda telah membooking '{self.book_title}'!\n\n📅 Tanggal Pinjam: {borrow_date}\n🚀 Tanggal Kembali: {return_date}")
            self.destroy()

# Contoh pemanggilan
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    booking_win = BookingWindow(root, "Harry Potter", "Tersedia", "/mnt/data/image.png")
    booking_win.mainloop()
