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