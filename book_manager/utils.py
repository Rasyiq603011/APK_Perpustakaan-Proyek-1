import os
import pandas as pd
from book_manager.constants import FILE_NAME

def buat_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Judul", "Penulis", "Tahun", "Penerbit", "Genre","ISBN"])
        df.to_excel(FILE_NAME, index=False)
        return True
    return False

def read_data():
    try:
        return pd.read_excel(FILE_NAME)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return pd.DataFrame(columns=["ID", "Judul", "Penulis", "Tahun", "Penerbit", "Genre","ISBN"])

def add_book(judul, penulis, tahun, penerbit, genre, isbn):
    try:
        df = read_data()
        id_baru = 1 if df.empty else int(df["ID"].max()) + 1
        
        df = pd.concat([df, pd.DataFrame({
            "ID": [id_baru], 
            "Judul": [judul], 
            "Penulis": [penulis], 
            "Tahun": [tahun],
            "Penerbit": [penerbit],
            "Genre": [genre],
            "ISBN": [isbn]
        })], ignore_index=True)
        
        df.to_excel(FILE_NAME, index=False)
        return True
    except Exception as e:
        print(f"Error adding book: {str(e)}")
        return False

def update_book(id_buku, judul, penulis, tahun, penerbit, genre, isbn):
    try:
        df = read_data()
        
        if id_buku in df["ID"].values:
            df.loc[df["ID"] == id_buku, ["Judul", "Penulis", "Tahun","Penerbit", "Genre","ISBN"]] = [judul, penulis, tahun, penerbit, genre, isbn]  
            df.to_excel(FILE_NAME, index=False)
            return True
        return False
    except Exception as e:
        print(f"Error updating book: {str(e)}")
        return False

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