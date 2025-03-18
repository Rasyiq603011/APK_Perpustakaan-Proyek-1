import tkinter as tk
import MyLibrary as L


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Book-Ku")
        self.root.geometry("400x300")

        self.create_widgets()
        self.currentFrame = None
        self.selectedBook = None

        self.container = tk.Container

        self.frames = {}

        self.frameClases = {
            #"Frame": Frame,
            "DetailsBookFrame": L.DetailsBookFrame,
            "DaftarBukuFrame": L.DataBookFrame
        }

        self.setupFrames()

        self.showFrame("isi frame awal")

        self.bookManager = L.BookManager("D:\\Project 1\\Tubes Semester 1\\Asset\\data_buku.xlsx")

    def create_widgets(self):
        pass

    def setupFrames(self):
        for name, FrameClass in self.frameClases.items():
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def showFrame(self, frame_name):
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            self.current_frame = frame_name
            

    def show_book_detail(self, book):
        self.selectedBook = book
        self.showFrame("detail")
