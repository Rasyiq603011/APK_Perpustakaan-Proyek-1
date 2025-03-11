import os
import pandas as pd
from book_manager.constants import FILE_NAME
from book_manager.models import Book

def buat_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["ID", "Judul", "Penulis", "Tahun", "Penerbit", "Genre", "ISBN"])
        df.to_excel(FILE_NAME, index=False)
        return True
    return False

def read_data():
    try:
        return pd.read_excel(FILE_NAME)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return pd.DataFrame(columns=["ID", "Judul", "Penulis", "Tahun", "Penerbit", "Genre", "ISBN"])

def get_all_books():
    df = read_data()
    books = []
    
    for _, row in df.iterrows():
        book = Book(
            id=row["ID"],
            judul=row["Judul"],
            penulis=row["Penulis"],
            tahun=row["Tahun"],
            penerbit=row["Penerbit"],
            genre=row["Genre"],
            isbn=row["ISBN"]
        )
        books.append(book)
    
    return books

def get_book_by_id(id_buku):
    df = read_data()
    book_row = df[df["ID"] == id_buku]
    
    if not book_row.empty:
        row = book_row.iloc[0]
        return Book(
            id=row["ID"],
            judul=row["Judul"],
            penulis=row["Penulis"],
            tahun=row["Tahun"],
            penerbit=row["Penerbit"],
            genre=row["Genre"],
            isbn=row["ISBN"]
        )
    
    return None

def search_books(keyword):
    keyword = str(keyword).lower()
    all_books = get_all_books()
    result = []
    
    for book in all_books:
        # Cari di semua field
        if (keyword in str(book.get_id()).lower() or
            keyword in book.get_judul().lower() or
            keyword in book.get_penulis().lower() or
            keyword in str(book.get_tahun()).lower()or
            keyword in book.get_penerbit().lower() or
            keyword in book.get_genre().lower() or
            keyword in str(book.get_isbn()).lower()):
            result.append(book)
    
    return result

def add_book(judul, penulis, tahun, penerbit, genre, isbn):
    try:
        df = read_data()
        id_baru = 1 if df.empty else int(df["ID"].max()) + 1
        
        # Buat objek Book baru
        new_book = Book(id_baru, judul, penulis, tahun, penerbit, genre, isbn)
        
        # Tambahkan ke DataFrame
        df = pd.concat([df, pd.DataFrame([new_book.to_dict()])], ignore_index=True)
        df.to_excel(FILE_NAME, index=False)
        
        return new_book
    except Exception as e:
        print(f"Error adding book: {str(e)}")
        return None

def update_book(id_buku, judul, penulis, tahun, penerbit, genre, isbn):
    try:
        df = read_data()
        
        if id_buku in df["ID"].values:
            # Update DataFrame
            df.loc[df["ID"] == id_buku, ["Judul", "Penulis", "Tahun", "Penerbit", "Genre", "ISBN"]] = [judul, penulis, tahun, penerbit, genre, isbn]
            df.to_excel(FILE_NAME, index=False)
            
            # Return updated Book object
            return Book(id_buku, judul, penulis, tahun, penerbit, genre, isbn)
        return None
    except Exception as e:
        print(f"Error updating book: {str(e)}")
        return None

def delete_book(id_buku):
    try:
        df = read_data()
        
        if id_buku in df["ID"].values:
            df = df[df["ID"] != id_buku]
            df.to_excel(FILE_NAME, index=False)
            return True
        return False
    except Exception as e:
        print(f"Error deleting book: {str(e)}")
        return False

def get_books_by_author(penulis):
    penulis = str(penulis).lower()
    return [book for book in get_all_books() if penulis in book.get_penulis().lower()]

def get_books_by_year(tahun):
    tahun = str(tahun)
    return [book for book in get_all_books() if tahun == str(book.get_tahun())]

def get_book_count():
    return len(get_all_books())