
class Book:
    def __init__(self, id=None, judul="", penulis="", tahun="", penerbit="", genre="", isbn=""):
        self._id = id
        self._judul = judul
        self._penulis = penulis
        self._tahun = tahun
        self._penerbit = penerbit
        self._genre = genre
        self._isbn = isbn

    
    # Getter untuk ID
    def get_id(self):
        return self._id
    
    # Getter untuk judul
    def get_judul(self):
        return self._judul
    
    # Getter untuk penulis
    def get_penulis(self):
        return self._penulis
    
    # Getter untuk tahun
    def get_tahun(self):
        return self._tahun
    
     # Getter untuk penerbit
    def get_penerbit(self):
        return self._penerbit
    
    # Getter untuk genre
    def get_genre(self):
        return self._genre
    
    # Getter untuk ISBN
    def get_isbn(self):
        return self._isbn
    
    # Setter untuk ID
    def set_id(self, id):
        self._id = id
    
    # Setter untuk judul
    def set_judul(self, judul):
        self._judul = judul
    
    # Setter untuk penulis
    def set_penulis(self, penulis):
        self._penulis = penulis
    
    # Setter untuk tahun
    def set_tahun(self, tahun):
        self._tahun = tahun

    # Setter untuk penerbit
    def set_penerbit(self, penerbit):
        self._penerbit = penerbit

    # Setter untuk genre
    def set_genre(self, genre):
        self._genre = genre

    # Setter untuk ISBN
    def set_isbn(self, isbn):
        self._isbn = isbn
    
    def to_dict(self):
        return {
            "ID": self._id,
            "Judul": self._judul,
            "Penulis": self._penulis,
            "Tahun": self._tahun,
            "Penerbit": self._penerbit,
            "Genre": self._genre,
            "ISBN": self._isbn,
        }
    
    def __str__(self):
        return f"Book(id={self._id}, judul='{self._judul}', penulis='{self._penulis}', tahun='{self._tahun}', penerbit='{self._penerbit}', genre='{self._genre}', isbn='{self._isbn}')"
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            id=data_dict.get("ID", None),
            judul=data_dict.get("Judul", ""),
            penulis=data_dict.get("Penulis", ""),
            tahun=data_dict.get("Tahun", ""),
            penerbit=data_dict.get("Penerbit", ""),
            genre=data_dict.get("Genre", ""),
            isbn=data_dict.get("ISBN", "")           
        )