"""
Contoh penggunaan model Book dan utility functions
"""

from book_manager.utils import *

def demo_book_getters():
    """
    Demonstrasi penggunaan getter pada objek Book
    """
    print("=== DEMONSTRASI PENGGUNAAN GETTER PADA OBJEK BOOK ===")
    
    # Tambah buku baru untuk demo
    book = add_book("Python Programming", "John Smith", "2022", "Tech Books", "Programming", "1234567890")
    
    if book:
        # Gunakan getter untuk mengakses nilai-nilai buku
        print(f"Info Buku:")
        print(f"ID       : {book.get_id()}")
        print(f"Judul    : {book.get_judul()}")
        print(f"Penulis  : {book.get_penulis()}")
        print(f"Tahun    : {book.get_tahun()}")
        print(f"Penerbit : {book.get_penerbit()}")
        print(f"Genre    : {book.get_genre()}")
        print(f"ISBN     : {book.get_isbn()}")
        
        # Menggunakan string representation
        print(f"\nString representation:")
        print(str(book))
        
        # Mengubah data menggunakan setter
        print("\nMengubah judul buku...")
        book.set_judul("Advanced Python Programming")
        
        # Update buku di database
        update_book(book.get_id(), book.get_judul(), book.get_penulis(), book.get_tahun(), book.get_penerbit(), book.get_genre(), book.get_isbn())
        
        # Verifikasi perubahan
        updated_book = get_book_by_id(book.get_id())
        print(f"Judul setelah diubah: {updated_book.get_judul()}")
    else:
        print("Gagal menambahkan buku demo")

def demo_search():
    """
    Demonstrasi penggunaan fungsi pencarian
    """
    print("\n=== DEMONSTRASI PENCARIAN BUKU ===")
    
    # Tambah beberapa buku untuk demo
    add_book("Java Programming", "Mark Johnson", "2020", "Tech Books", "Programming", "0987654321")
    add_book("Database Design", "Susan Lee", "2021", "Tech Books", "Database", "2345678901")
    add_book("Web Development", "Mark Wilson", "2022", "Tech Books", "Web Development", "3456789012")
    
    # 1. Cari buku berdasarkan keyword
    print("\n1. Mencari buku dengan keyword 'Programming':")
    result = search_books("Programming")
    print(f"Ditemukan {len(result)} buku:")
    for book in result:
        print(f"- {book.get_judul()} oleh {book.get_penulis()}")
    
    # 2. Cari buku berdasarkan penulis
    print("\n2. Mencari buku dengan penulis 'Mark':")
    result = get_books_by_author("Mark")
    print(f"Ditemukan {len(result)} buku:")
    for book in result:
        print(f"- {book.get_judul()} ({book.get_tahun()})")
    
    # 3. Cari buku berdasarkan tahun
    print("\n3. Mencari buku dengan tahun terbit '2022':")
    result = get_books_by_year("2022")
    print(f"Ditemukan {len(result)} buku:")
    for book in result:
        print(f"- {book.get_judul()} oleh {book.get_penulis()}")

def show_all_books():
    """
    Menampilkan semua buku
    """
    print("\n=== DAFTAR SEMUA BUKU ===")
    books = get_all_books()
    
    if not books:
        print("Tidak ada buku dalam database")
        return
        
    print(f"Jumlah total buku: {get_book_count()}")
    
    for book in books:
        print(f"ID: {book.get_id()}")
        print(f"Judul    : {book.get_judul()}")
        print(f"Penulis  : {book.get_penulis()}")
        print(f"Tahun    : {book.get_tahun()}")
        print(f"Penerbit : {book.get_penerbit()}")
        print(f"Genre    : {book.get_genre()}")
        print(f"ISBN     : {book.get_isbn()}")
        print("-" * 30)

if __name__ == "__main__":
    print("Demonstrasi penggunaan Model Book dan Utility Functions")
    print("======================================================")
    
    # Demo penggunaan getter
    demo_book_getters()
    
    # Demo pencarian
    demo_search()
    
    # Tampilkan semua buku
    show_all_books()
    
    print("\nDemo selesai!")