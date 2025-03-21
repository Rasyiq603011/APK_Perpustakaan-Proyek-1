import pandas as pd

def load_books(filepath):
    """
    Membaca file Excel dan mengembalikan daftar buku dalam bentuk dictionary.
    """
    try:
        df = pd.read_excel(filepath)
        books = df.to_dict(orient="records")  # Konversi ke list of dictionaries
        return books
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")
        return []

# Contoh pemanggilan
if __name__ == "__main__":
    books = load_books("../data/data_buku.xlsx")
    for book in books[:5]:  # Menampilkan 5 buku pertama
        print(book)
