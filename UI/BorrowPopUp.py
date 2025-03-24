import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import datetime, timedelta
import os
import json
import calendar

class BorrowPopUp(ctk.CTkToplevel):
    def __init__(self, parent, controller, book, is_booking=False):
        super().__init__(parent)
        self.title("BOOK-KU - Borrow Book")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Make the popup modal
        self.transient(parent)
        self.grab_set()
        
        self.controller = controller
        self.book = book
        self.is_booking = is_booking
        
        # Get directories from controller
        self.data_dir = self.controller.data_dir
        self.assets_dir = self.controller.assets_dir
        self.cover_dir = os.path.join(self.assets_dir, "covers")
        self.default_cover = os.path.join(self.assets_dir, "IMG.jpg")
        
        # Data files
        self.bookings_file = os.path.join(self.data_dir, "bookings.json")
        self.loans_file = os.path.join(self.data_dir, "loans.json")
        
        # Create files if they don't exist
        for file_path in [self.bookings_file, self.loans_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
        
        # Set dates
        self.today = datetime.now().date()
        self.return_date = self.today + timedelta(days=7)
        
        # If booking, find the first available date
        if self.is_booking:
            self.booking_start_date = self.find_first_available_date()
        
        # Selected date for booking
        self.selected_booking_date = None
        
        # Create the UI
        self.create_ui()
    
    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_text = "Book Reservation" if self.is_booking else "Borrow Book"
        title_label = ctk.CTkLabel(
            self.main_frame,
            text=title_text,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=20)
        
        # Book details
        details_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Book title
        book_title = ctk.CTkLabel(
            details_frame,
            text=self.book.get('Judul', 'Unknown Title'),
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        book_title.pack(pady=10)
        
        # Dates
        dates_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        dates_frame.pack(fill="x", padx=20, pady=10)
        
        # Borrow date
        borrow_label = ctk.CTkLabel(
            dates_frame,
            text=f"Borrow Date: {self.today.strftime('%d %B %Y')}",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="white"
        )
        borrow_label.pack(pady=5)
        
        # Return date
        return_label = ctk.CTkLabel(
            dates_frame,
            text=f"Return By: {self.return_date.strftime('%d %B %Y')}",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#FF6D00"
        )
        return_label.pack(pady=5)
        
        # Note
        note_label = ctk.CTkLabel(
            details_frame,
            text="Please return the book on time to avoid penalties.\nLate fees are Rp5,000 per day.",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA"
        )
        note_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=50)
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="#F44336",
            hover_color="#D32F2F",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            width=100,
            height=35
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Confirm button
        confirm_text = "Confirm Booking" if self.is_booking else "Confirm Borrow"
        confirm_color = "#FF6D00" if self.is_booking else "#4CAF50"
        hover_color = "#E65100" if self.is_booking else "#388E3C"
        
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text=confirm_text,
            command=self.confirm_action,
            fg_color=confirm_color,
            hover_color=hover_color,
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            width=150,
            height=35
        )
        confirm_btn.pack(side="right", padx=10)
    
    def save_loan_record(self):
        """Menyimpan data peminjaman ke loans.json dan datapeminjaman.txt"""
        try:
            # Load existing loans
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
            
            # Create new loan record
            loan_record = {
                "isbn": self.book['ISBN'],
                "title": self.book['Judul'],
                "username": self.controller.current_user.get("username", "unknown"),
                "borrow_date": self.today.strftime("%Y-%m-%d"),
                "return_date": self.return_date.strftime("%Y-%m-%d"),
                "status": "Borrowed" if not self.is_booking else "Booked"
            }
            
            # Add to loans list
            loans.append(loan_record)
            
            # Save back to file
            with open(self.loans_file, 'w') as f:
                json.dump(loans, f, indent=2)
            
            # Save to datapeminjaman.txt
            data_peminjaman_file = os.path.join(self.data_dir, "datapeminjaman.txt")
            with open(data_peminjaman_file, 'a') as f:
                f.write(f"ISBN: {self.book['ISBN']}\n")
                f.write(f"Judul: {self.book['Judul']}\n")
                f.write(f"Peminjam: {self.controller.current_user.get('username', 'unknown')}\n")
                f.write(f"Tanggal Pinjam: {self.today.strftime('%Y-%m-%d')}\n")
                f.write(f"Tanggal Kembali: {self.return_date.strftime('%Y-%m-%d')}\n")
                f.write(f"Status: {'Booked' if self.is_booking else 'Borrowed'}\n")
                f.write("-" * 50 + "\n")
            
            # Update MyBookFrame
            if "MyBookFrame" in self.controller.frames:
                if hasattr(self.controller.frames["MyBookFrame"], "load_current_books"):
                    self.controller.frames["MyBookFrame"].load_current_books()
            
            # Check for overdue books and move to penalties
            self.check_overdue_books()
                
            return True
        except Exception as e:
            print(f"Error saving loan record: {e}")
            return False
    
    def check_overdue_books(self):
        """Memeriksa buku yang terlambat dan memindahkannya ke penalties"""
        try:
            # Load current loans
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
            
            # Load penalties
            penalties_file = os.path.join(self.data_dir, "penalties.json")
            if not os.path.exists(penalties_file):
                with open(penalties_file, 'w') as f:
                    json.dump([], f)
            
            with open(penalties_file, 'r') as f:
                penalties = json.load(f)
            
            current_date = datetime.now().date()
            
            # Check each loan
            for loan in loans[:]:  # Use slice copy to avoid modification during iteration
                return_date = datetime.strptime(loan['return_date'], "%Y-%m-%d").date()
                
                # If book is overdue
                if current_date > return_date and loan['status'] == "Borrowed":
                    # Create penalty record
                    penalty_record = {
                        "isbn": loan['isbn'],
                        "title": loan['title'],
                        "username": loan['username'],
                        "borrow_date": loan['borrow_date'],
                        "return_date": loan['return_date'],
                        "overdue_days": (current_date - return_date).days,
                        "penalty_amount": (current_date - return_date).days * 5000  # Rp5,000 per day
                    }
                    
                    # Add to penalties
                    penalties.append(penalty_record)
                    
                    # Update book status
                    if hasattr(self.controller, 'book_manager'):
                        self.controller.book_manager.UpdateStatus(loan['isbn'], "Overdue")
                    
                    # Remove from loans
                    loans.remove(loan)
            
            # Save updated loans
            with open(self.loans_file, 'w') as f:
                json.dump(loans, f, indent=2)
            
            # Save updated penalties
            with open(penalties_file, 'w') as f:
                json.dump(penalties, f, indent=2)
            
            # Refresh MyBookFrame and PenaltyFrame
            if "MyBookFrame" in self.controller.frames:
                if hasattr(self.controller.frames["MyBookFrame"], "load_current_books"):
                    self.controller.frames["MyBookFrame"].load_current_books()
            
            if "PenaltyFrame" in self.controller.frames:
                if hasattr(self.controller.frames["PenaltyFrame"], "load_penalties"):
                    self.controller.frames["PenaltyFrame"].load_penalties()
                    
        except Exception as e:
            print(f"Error checking overdue books: {e}")
    
    def confirm_action(self):
        """Handle confirm button click"""
        try:
            # Pastikan controller memiliki book_manager
            if not hasattr(self.controller, 'book_manager'):
                print("Controller attributes:", dir(self.controller))
                messagebox.showerror("Error", "Book manager not initialized")
                return

            # Debug info
            print("Book ISBN:", self.book['ISBN'])
            print("Book Status:", self.book.get('Status', 'Unknown'))
            print("Is Booking:", self.is_booking)

            if self.is_booking:
                # Handle booking
                if self.controller.book_manager.UpdateStatus(self.book['ISBN'], "Booked"):
                    # Simpan data booking
                    if self.save_loan_record():
                        messagebox.showinfo("Success", "Book booked successfully!")
                        # Log aksi booking
                        if hasattr(self.controller, 'log_action'):
                            self.controller.log_action(f"Booked book: {self.book['Judul']} (ISBN: {self.book['ISBN']})")
                        # Refresh MyBookFrame
                        if "MyBookFrame" in self.controller.frames:
                            if hasattr(self.controller.frames["MyBookFrame"], "load_current_books"):
                                self.controller.frames["MyBookFrame"].load_current_books()
                    else:
                        messagebox.showerror("Error", "Failed to save booking record")
                else:
                    messagebox.showerror("Error", "Failed to book the book")
            else:
                # Handle borrowing
                if self.controller.book_manager.UpdateStatus(self.book['ISBN'], "Borrowed"):
                    # Simpan data peminjaman
                    if self.save_loan_record():
                        messagebox.showinfo("Success", "Book borrowed successfully!")
                        # Log aksi peminjaman
                        if hasattr(self.controller, 'log_action'):
                            self.controller.log_action(f"Borrowed book: {self.book['Judul']} (ISBN: {self.book['ISBN']})")
                        # Refresh MyBookFrame
                        if "MyBookFrame" in self.controller.frames:
                            if hasattr(self.controller.frames["MyBookFrame"], "load_current_books"):
                                self.controller.frames["MyBookFrame"].load_current_books()
                    else:
                        messagebox.showerror("Error", "Failed to save loan record")
                else:
                    messagebox.showerror("Error", "Failed to borrow the book")
            
            self.destroy()
        except AttributeError as e:
            print("AttributeError detail:", str(e))
            print("Controller attributes:", dir(self.controller))
            messagebox.showerror("Error", f"Book manager not properly initialized: {str(e)}")
        except Exception as e:
            print("Exception detail:", str(e))
            print("Controller attributes:", dir(self.controller))
            messagebox.showerror("Error", f"Failed to {'book' if self.is_booking else 'borrow'} book: {str(e)}")
    
    def find_first_available_date(self):
        """Find the first available date for booking"""
        # Get booked dates
        booked_dates = self.get_booked_dates()
        
        # Start from tomorrow
        first_available = self.today + timedelta(days=1)
        
        # If the book is currently borrowed, we need to check the return date
        # For demo, let's assume it's borrowed for 7 days from today
        if self.book.get('Status', '') == "Borrowed":
            first_available = self.today + timedelta(days=8)
        
        # If the date is already booked, move to the next day
        while first_available in booked_dates:
            first_available += timedelta(days=1)
        
        return first_available
    
    def get_booked_dates(self):
        """Get a list of dates when the book is already booked"""
        booked_dates = []
        
        # Load existing bookings
        try:
            with open(self.bookings_file, 'r') as f:
                bookings = json.load(f)
                
            # Filter bookings for this book
            book_bookings = [
                b for b in bookings 
                if b.get('isbn', '') == self.book.get('ISBN', '') and b.get('status', '') == 'active'
            ]
            
            # Extract booked dates
            for booking in book_bookings:
                booking_date = datetime.strptime(booking.get('booking_date', ''), "%Y-%m-%d").date()
                return_date = datetime.strptime(booking.get('return_date', ''), "%Y-%m-%d").date()
                
                # Add all dates between booking_date and return_date (inclusive)
                current_date = booking_date
                while current_date <= return_date:
                    booked_dates.append(current_date)
                    current_date += timedelta(days=1)
                
        except Exception as e:
            print(f"Error loading bookings: {e}")
            
        return booked_dates
    
    def load_book_cover(self):
        """Load the book cover image"""
        # Default dimensions
        width, height = 180, 270
        
        try:
            # Try to load from controller's book manager
            if hasattr(self.controller, 'loadCover'):
                isbn = self.book.get('ISBN', '')
                cover = self.controller.loadCover(isbn)
                if cover:
                    return cover
            
            # If no cover from controller, try loading from cover_dir
            isbn = self.book.get('ISBN', '')
            cover_path = os.path.join(self.cover_dir, f"{isbn}.jpg")
            if os.path.exists(cover_path):
                img = Image.open(cover_path)
                img = img.resize((width, height))
                return ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
            
            # If still no cover, try default cover
            if os.path.exists(self.default_cover):
                img = Image.open(self.default_cover)
                img = img.resize((width, height))
                return ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
            
        except Exception as e:
            print(f"Error loading cover image: {e}")
        
        # Fallback to a blank cover
        blank_img = Image.new('RGB', (width, height), color='#333333')
        return ctk.CTkImage(light_image=blank_img, dark_image=blank_img, size=(width, height))


# For testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("200x100")
    root.title("Parent Window")
    
    class MockController:
        def __init__(self):
            self.current_user = {"username": "test_user", "role": "user"}
        
        def update_book_status(self, isbn, status):
            print(f"Would update book status to: {isbn}, {status}")
        
        def create_booking_record(self, booking_data):
            print(f"Would create booking record: {booking_data}")
        
        def create_loan_record(self, loan_data):
            print(f"Would create loan record: {loan_data}")
        
        def loadCover(self, isbn):
            return None
    
    controller = MockController()
    
    # Sample book
    import pandas as pd
    sample_book = pd.Series({
        'Judul': 'The Great Gatsby',
        'Penulis': 'F. Scott Fitzgerald',
        'Penerbit': 'Scribner',
        'Tahun': '1925',
        'Kategori': 'Classic Literature',
        'ISBN': '9780743273565',
        'Halaman': '180',
        'Status': 'Available',
        'Deskripsi': 'The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald.'
    })
    
    def open_borrow():
        BorrowPopUp(root, controller, sample_book, is_booking=False)
    
    def open_booking():
        # Change status to Borrowed for booking test
        book_copy = sample_book.copy()
        book_copy['Status'] = 'Borrowed'
        BorrowPopUp(root, controller, book_copy, is_booking=True)
    
    btn1 = ctk.CTkButton(root, text="Test Borrow", command=open_borrow)
    btn1.pack(pady=5)
    
    btn2 = ctk.CTkButton(root, text="Test Booking", command=open_booking)
    btn2.pack(pady=5)
    
    root.mainloop()