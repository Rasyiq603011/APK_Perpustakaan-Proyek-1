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
        # Convert to string for comparison if needed
        isbn_str = str(isbn)
        # Check if any row's ISBN equals the given ISBN
        return (self.book['ISBN'].astype(str) == isbn_str).any()
        
    def addBook(self, book):
        """Add a new book to the DataFrame"""
        # Convert dictionary to DataFrame
        book_df = pd.DataFrame([book])
        
        # Concatenate with existing DataFrame
        self.book = pd.concat([self.book, book_df], ignore_index=True)
        self.save()
        return True
    
    def save(self):
        try:
            # Try to save directly
            self.book.to_excel(self.file_path, index=False)
            return True
        except PermissionError:
            from tkinter import messagebox
            import os
            import time
            
            # Inform the user
            response = messagebox.askretrycancel(
                "File Access Error",
                f"Tidak dapat menyimpan ke file '{os.path.basename(self.file_path)}'. File mungkin sedang terbuka di program lain atau Anda tidak memiliki izin yang cukup.\n\nTutup program lain yang membuka file ini dan coba lagi."
            )
            
            if response:  # User wants to retry
                try:
                    # Wait briefly then try again
                    time.sleep(1)
                    self.book.to_excel(self.file_path, index=False)
                    return True
                except Exception as e:
                    # If still fails, try saving to a backup location
                    backup_path = self.file_path.replace(".xlsx", f"_backup_{int(time.time())}.xlsx")
                    try:
                        self.book.to_excel(backup_path, index=False)
                        messagebox.showinfo(
                            "Berhasil Disimpan ke Backup",
                            f"Data berhasil disimpan ke file backup:\n{os.path.basename(backup_path)}"
                        )
                        return True
                    except Exception as backup_error:
                        messagebox.showerror(
                            "Gagal Menyimpan Data",
                            f"Tidak dapat menyimpan data ke file asli maupun backup.\nError: {str(backup_error)}"
                        )
                        return False
            return False
        except Exception as e:
            # Handle other errors
            from tkinter import messagebox
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan saat menyimpan data:\n{str(e)}"
            )
            return False
    
    def UpdateBook(self, bookUpdate):
        # Find the index of the book to update
        mask = self.book['ISBN'].astype(str) == str(bookUpdate['ISBN'])
        if not mask.any():
            # print(f"Book with ISBN {bookUpdate['ISBN']} not found")
            return False
            
        # Get the index where the ISBN matches
        idx = mask.idxmax()
        
        # Update all fields for the book at this index
        for column in self.book.columns:
            if column in bookUpdate:
                self.book.at[idx, column] = bookUpdate[column]
        
        # Save the updated DataFrame
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
        """Load book cover image as CTkImage"""
        import customtkinter as ctk
        
        size = (100, 150)
        
        # Check if book image exists
        img_path = os.path.join(self.coverDir, f"{isbn}.jpeg")
        if not os.path.exists(img_path) or not isbn:
            # Use default image if not found
            img_path = self.defaultImage
                
        try:
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Create blank image on error
            blank_img = Image.new('RGB', size, color='lightgray')
            return ctk.CTkImage(light_image=blank_img, dark_image=blank_img, size=size)

    

if __name__ == '__main__':
    book = BookManager("D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku_2.xlsx")
    print(book.book[0].get('Penulis', 'Tidak Tersedia'))

    
    