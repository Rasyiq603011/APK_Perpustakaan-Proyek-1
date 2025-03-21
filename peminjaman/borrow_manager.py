import datetime

def borrow_book(book_title, books, peminjaman_file):
    """
    Meminjam buku jika tersedia dan menyimpannya ke file TXT.
    """
    for book in books:
        if book["Judul"] == book_title:
            if book.get("tersedia", True):  # Default: tersedia jika tidak ada atribut
                book["tersedia"] = False  # Update status
                borrow_date = datetime.date.today()
                return_date = borrow_date + datetime.timedelta(days=7)

                # Simpan ke file
                with open(peminjaman_file, "a") as file:
                    file.write(f"{book_title}, {borrow_date}, {return_date}\n")

                return f"Buku '{book_title}' berhasil dipinjam sampai {return_date}."
            else:
                return f"Buku '{book_title}' sedang dipinjam. Silakan booking."
    return "Buku tidak ditemukan."

def book_book(book_title, books, booking_date, peminjaman_file):
    """
    Booking buku jika sedang dipinjam.
    """
    for book in books:
        if book["Judul"] == book_title:
            if not book.get("tersedia", True):  # Cek jika sedang dipinjam
                borrow_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d").date()
                return_date = borrow_date + datetime.timedelta(days=7)

                # Simpan ke file
                with open(peminjaman_file, "a") as file:
                    file.write(f"{book_title}, {borrow_date}, {return_date}\n")

                return f"Buku '{book_title}' berhasil dibooking. Bisa diambil mulai {borrow_date}."
            else:
                return f"Buku '{book_title}' tersedia, silakan pinjam langsung."
    return "Buku tidak ditemukan."

# Contoh pemanggilan
if __name__ == "__main__":
    sample_books = [
        {"Judul": "Python Basics", "tersedia": True},
        {"Judul": "Machine Learning", "tersedia": False},
    ]

    print(borrow_book("Python Basics", sample_books, "../data/peminjaman.txt"))
    print(book_book("Machine Learning", sample_books, "2025-03-25", "../data/peminjaman.txt"))
