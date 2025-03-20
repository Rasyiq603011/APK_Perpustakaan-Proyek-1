import tkinter as tk
from MyLibrary.constans import *
from MyLibrary.Moduls.Book_Manager import BookManager
from MyLibrary.UI.DaftarBukuFrame import DataBookFrame
from MyLibrary.UI.DetailsBookFrame import DetailsBookFrame
from MyLibrary.UI.UpdateBookFrame import UpdateBookFrame
from MyLibrary.UI.AddBookFrame import AddBookFrame


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Book-Ku")
        self.root.geometry("1024x768")
        self.currentFrame = None
        self.bookManager = BookManager("D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku.xlsx",'Cover', "img.jpg")
        self.selectedBook = BookManager.getBookByIndeks(self.bookManager, 14)

        self.create_widgets()
    
    def create_widgets(self):
        # Create the container frame
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frameClases = {
            "DetailsBookFrame": DetailsBookFrame,
            # "DaftarBukuFrame": DataBookFrame,
            "UpdateBookFrame": UpdateBookFrame,
            "AddBookFrame": AddBookFrame,
        }

        self.setupFrames()
        self.showFrame("DetailsBookFrame")  # Start with book list

    def setupFrames(self):
        for name, FrameClass in self.frameClases.items():
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def showFrame(self, frame_name):
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            self.currentFrame = frame_name
            
    def show_book_detail(self, book):
        self.selectedBook = book
        self.showFrame("DetailsBookFrame")  # Use correct frame name

if __name__ == "__main__":
    root = tk.Tk()
    App = Application(root)
    root.mainloop()