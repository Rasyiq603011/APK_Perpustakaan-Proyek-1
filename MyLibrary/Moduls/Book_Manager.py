import pandas as pd
import numpy as np
import os

class BookManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.book = pd.read_excel(file_path)
        else:
            self.book = pd.DataFrame(columns=['Judul', 'Penulis', 'Penerbit', 'Tahun','Kategori', 'ISBN', 'Halaman', 'Deskripsi','Status'])

    def getBook(self):
        return self.book
    
    def ISBNValidator(self,ISBN):
        if len(ISBN) != 13:
            return False
        return True
    def addBook(self, Judul, Penulis,Penerbit,Tahun, ISBN,Halaman,Status):
        if ISBN in self.book['ISBN'].values | self.ISBNValidator(ISBN):
            return False
        
        buku_baru = {
            'Judul': Judul,
            'Penulis': Penulis,
            'Penerbit': Penerbit,
            'Tahun': Tahun,
            'ISBN': ISBN,
            'Halaman': Halaman,
            'Status': Status,
        }
        self.book = self.book.append(buku_baru, ignore_index=True)
        return True
    
    def save(self):
        self.book.to_excel(self.file_path, index=False)
        return True
    
    def searchBook(self, keyword):
        return self.book[self.book['Judul'].str.contains(keyword) | 
                         self.book['Penulis'].str.contains(keyword) |
                         self.book['Penerbit'].str.contains(keyword) |
                         self.book['Tahun'].str.contains(keyword) |
                         self.book['ISBN'].str.contains(keyword) |
                         self.book['Deskripsi'].str.contains(keyword) |
                         self.book['Kategori'].str.contains(keyword) |
                         self.book['Status'].str.contains(keyword)]
    
    def deleteBook(self, ISBN):
        self.book = self.book[self.book['ISBN']!= ISBN]
        return True
    
    
    def getBookCount(self):
        return len(self.book)
    
    def daftarPenulis(self):
        return self.book.drop_duplicates(subset='Penulis')['Penulis'].tolist()
    
    def daftarKategori(self):
        return self.book['Kategori'].unique().tolist()
    
    def daftarPenerbit(self):
        return self.book['Penerbit'].unique().tolist()
    

if __name__ == '__main__':
    book = BookManager("D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku_2.xlsx")
    print(book.daftarKategori())
    
    