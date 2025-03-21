import pandas as pd
import numpy as np
import os
from PIL import Image, ImageTk

class BookManager:
    def __init__(self, file_path, CoverDir, defaultImage):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.book = pd.read_excel(file_path)
        else:
            self.book = pd.DataFrame(columns=['Judul', 'Penulis', 'Penerbit', 'Tahun','Kategori', 'ISBN', 'Halaman', 'Deskripsi','Status'])

        self.coverDir = CoverDir
        self.defaultImage = defaultImage


    def getBook(self):
        return self.book
    
    def getCoverImage(self, ISBN):
        if ISBN in self.book['ISBN'].values:
            cover_path = os.path.join(self.coverDir, f"{ISBN}.jpg")
            if os.path.exists(cover_path):
                return ImageTk.PhotoImage(Image.open(cover_path))
            else:
                return ImageTk.PhotoImage(Image.open(self.defaultImage))
        else:
            return ImageTk.PhotoImage(Image.open(self.defaultImage))
        
    def getBookByIndeks(self, index):
        if index < len(self.book):
            return self.book.iloc[index]
        else:
            return None
    
    def ISBNValidator(self,isbn):
        if not isbn.isdigit() or len(isbn) < 10:
            return False
    
    def TahunValidator(self, tahun):
        # Validate year is a number
        if tahun < 1000 or tahun > 3000:
            return False
        
    def PageValidator(self,page):       
        if page < 0:
            return False
        
    def ISBNexists(self, isbn):
        return isbn in self.book['ISBN']
    
    def addBook(self,book):
        self.book = self.book.append(book, ignore_index=True)
        self.save()
        return True
    
    def save(self):
        self.book.to_excel(self.file_path, index=False)
        return True
    
    def UpdateBook(self, bookUpdate):
        self.book.loc[self.book['ISBN'] == bookUpdate['ISBN'], :] = bookUpdate
        self.save()
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
    
    def FilterByKategori(self, Kategori = None, Tahun = None, Status = None):
        conditions = []

        if Kategori is not None:
            conditions.append(np.isin(self.book['Kategori'], Kategori if isinstance(Kategori, list) else [Kategori]))

        if Tahun is not None:
            conditions.append(np.isin(self.book['Tahun'], Tahun if isinstance(Tahun, list) else [Tahun]))

        if Status is not None:
            conditions.append(np.isin(self.book['Status'], Status if isinstance(Status, list) else [Status]))

        if conditions:
            return self.book[np.logical_and.reduce(conditions)]
        else:
            return self.book #Jika kategori tidak ada yang dipilih
        
    def UpdateStatus(self, Status):
        self.book.loc[self.book['ISBN'] == book['ISBN'], 'Status'] = book['Status']
        return True
    
    def getBookCount(self):
        return len(self.book)
    
    def daftarPenulis(self):
        return self.book.drop_duplicates(subset='Penulis')['Penulis'].tolist()
    
    def daftarKategori(self):
        return self.book['Kategori'].unique().tolist()
    
    def daftarPenerbit(self):
        return self.book['Penerbit'].unique().tolist()
    
    def LoadCover(self, isbn):
        size = (100, 150)
        
        # Check if book image exists
        img_path = os.path.join(self.coverDir, f"{isbn}.jpeg")
        if not os.path.exists(img_path) or not isbn:
            # Use default image if not found
            img_path = self.defaultImage
            
        try:
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Create blank image on error
            blank_img = Image.new('RGB', size, color='lightgray')
            return ImageTk.PhotoImage(blank_img)
    

if __name__ == '__main__':
    book = BookManager("D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku_2.xlsx")
    print(book.book[0].get('Penulis', 'Tidak Tersedia'))

    
    