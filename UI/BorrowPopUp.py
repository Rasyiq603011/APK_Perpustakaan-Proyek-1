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
        self.geometry("600x380")
        self.resizable(False, False)
        self.minsize(600, 380)
        
        # Center the window
        self.center_window()
        
        # Make the popup modal
        self.transient(parent)
        self.grab_set()
        
        self.controller = controller
        self.book = book
        self.is_booking = is_booking
        
        # Get database from controller
        self.db = self.controller.db if hasattr(self.controller, 'db') else None
        
        # Calendar constants
        self.months = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        
        # Get cover dir from controller or use default
        self.cover_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "covers")
        self.default_cover = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default_cover.jpg")
        
        # Data dir for booking records
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
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
        
        # Lift window to top
        self.lift()
        self.focus_force()
    
    def center_window(self):
        """Center the window on the screen"""
        # Update window size
        self.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - 600) // 2  # 600 is window width
        y = (screen_height - 380) // 2  # 380 is window height
        
        # Set position
        self.geometry(f"600x380+{x}+{y}")
    
    def create_ui(self):
        """Create the main UI layout"""
        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.main_frame.pack(fill="both", expand=True)

        # Create header
        self.create_header()

        # Create content based on mode
        if self.is_booking:
            self.create_booking_layout()
        else:
            self.create_borrow_layout()
    
    def create_header(self):
        """Create the header section of the UI"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B", height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)

        title_text = "Book Reservation" if self.is_booking else "Borrow Book"
        header_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
    
    def create_borrow_layout(self):
        """Create layout for direct borrowing"""
        content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            height=600
        )
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Two columns layout
        content_frame.columnconfigure(0, weight=1)  # Info column
        content_frame.columnconfigure(1, weight=1)  # Cover column
        
        # Book information
        info_frame = ctk.CTkFrame(content_frame, fg_color="#2B2B2B", corner_radius=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=10)
        
        book_title = self.book.get('Judul', 'Unknown Title')
        title_label = ctk.CTkLabel(
            info_frame,
            text=book_title,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white",
            wraplength=250
        )
        title_label.pack(padx=20, pady=(20, 10))
        
        # Borrow details
        details_frame = ctk.CTkFrame(info_frame, fg_color="#333333", corner_radius=8)
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Status
        status_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#AAAAAA",
            anchor="w",
            width=120
        )
        status_label.pack(side="left")
        
        status_value = ctk.CTkLabel(
            status_frame,
            text="Available",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#4CAF50",
            anchor="w"
        )
        status_value.pack(side="left", fill="x", expand=True)
        
        # Borrow date
        borrow_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        borrow_frame.pack(fill="x", padx=10, pady=5)
        
        borrow_label = ctk.CTkLabel(
            borrow_frame,
            text="Borrow Date:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#AAAAAA",
            anchor="w",
            width=120
        )
        borrow_label.pack(side="left")
        
        borrow_value = ctk.CTkLabel(
            borrow_frame,
            text=self.today.strftime("%d %B %Y"),
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="white",
            anchor="w"
        )
        borrow_value.pack(side="left", fill="x", expand=True)
        
        # Return date
        return_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        return_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        return_label = ctk.CTkLabel(
            return_frame,
            text="Return By:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#AAAAAA",
            anchor="w",
            width=120
        )
        return_label.pack(side="left")
        
        return_value = ctk.CTkLabel(
            return_frame,
            text=self.return_date.strftime("%d %B %Y"),
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#FF6D00",
            anchor="w"
        )
        return_value.pack(side="left", fill="x", expand=True)

        # Confirm button below return date with green color
        self.confirm_btn = ctk.CTkButton(
            details_frame,  # Changed from content_frame to details_frame
            text="Confirm Borrow",
            command=self.confirm_action,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            corner_radius=8,
            width=200,
            height=45
        )
        self.confirm_btn.pack(pady=(0, 10))  # Added padding at bottom

        # Warning text
        warning_text = "Please return the book on time to avoid penalties. Late fees are Rp5,000 per day."
        warning_label = ctk.CTkLabel(
            info_frame,
            text=warning_text,
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA",
            wraplength=250
        )
        warning_label.pack(padx=20, pady=(0, 20))
        
        # Book cover
        cover_frame = ctk.CTkFrame(content_frame, fg_color="#2B2B2B", corner_radius=10)
        cover_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=10)
        
        cover_img = self.load_book_cover()
        cover_label = ctk.CTkLabel(cover_frame, image=cover_img, text="")
        cover_label.image = cover_img  # Keep reference
        cover_label.pack(padx=20, pady=20)
    
    def create_booking_layout(self):
        """Create layout for booking"""
        # Create main content frame with scrollbar
        content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            height=600
        )
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Book information
        info_frame = ctk.CTkFrame(content_frame, fg_color="#2B2B2B", corner_radius=10)
        info_frame.pack(fill="x", padx=0, pady=(0, 5))
        
        book_title = self.book.get('Judul', 'Unknown Title')
        title_label = ctk.CTkLabel(
            info_frame,
            text=book_title,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white",
            wraplength=500
        )
        title_label.pack(padx=20, pady=(10, 5))
        
        # Current status and availability info
        status_frame = ctk.CTkFrame(info_frame, fg_color="#333333", corner_radius=8)
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Current Status
        current_status = self.book.get('Status', 'Unknown')
        status_label = ctk.CTkLabel(
            status_frame,
            text=f"Current Status: {current_status}",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#FF6D00",
            anchor="w"
        )
        status_label.pack(padx=20, pady=(5, 3))
        
        # Next availability message
        next_available = self.booking_start_date.strftime("%d %B %Y")
        avail_text = f"This book will be available starting from {next_available}"
        avail_label = ctk.CTkLabel(
            status_frame,
            text=avail_text,
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="white",
            wraplength=500,
            justify="left"
        )
        avail_label.pack(padx=20, pady=(0, 5))
        
        # Calendar section
        calendar_frame = ctk.CTkFrame(content_frame, fg_color="#2B2B2B", corner_radius=10)
        calendar_frame.pack(fill="x", padx=0, pady=5)
        
        # Month and Year selection in one row
        month_year_frame = ctk.CTkFrame(calendar_frame, fg_color="#333333", corner_radius=8)
        month_year_frame.pack(fill="x", padx=20, pady=5)
        
        # Month dropdown
        current_month = self.booking_start_date.month - 1
        self.month_var = ctk.StringVar(value=self.months[current_month])
        month_dropdown = ctk.CTkOptionMenu(
            month_year_frame,
            values=self.months,
            variable=self.month_var,
            command=self.update_calendar,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            button_color="#6200EA",
            button_hover_color="#5000D0",
            width=120
        )
        month_dropdown.pack(side="left", padx=10, pady=5)
        
        # Year dropdown
        current_year = self.booking_start_date.year
        years = [str(current_year + i) for i in range(3)]
        self.year_var = ctk.StringVar(value=str(current_year))
        year_dropdown = ctk.CTkOptionMenu(
            month_year_frame,
            values=years,
            variable=self.year_var,
            command=self.update_calendar,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#1E1E1E",
            button_color="#6200EA",
            button_hover_color="#5000D0",
            width=100
        )
        year_dropdown.pack(side="left", padx=10, pady=5)
        
        # Calendar grid
        self.calendar_grid = ctk.CTkFrame(calendar_frame, fg_color="#333333", corner_radius=8)
        self.calendar_grid.pack(padx=20, pady=5)
        
        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            day_label = ctk.CTkLabel(
                self.calendar_grid,
                text=day,
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#AAAAAA"
            )
            day_label.grid(row=0, column=i, padx=3, pady=3)
        
        # Initialize calendar
        self.update_calendar()
        
        # Selected date info
        self.selected_date_label = ctk.CTkLabel(
            calendar_frame,
            text="Please select a date to continue",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#AAAAAA"
        )
        self.selected_date_label.pack(pady=(10, 3))
        
        # Return date info
        self.return_date_label = ctk.CTkLabel(
            calendar_frame,
            text="",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#FF6D00"
        )
        self.return_date_label.pack(pady=(0, 5))

        # Confirm button below calendar
        self.confirm_btn = ctk.CTkButton(
            calendar_frame,
            text="Confirm Booking",
            command=self.confirm_action,
            fg_color="#FF6D00",
            hover_color="#E65100",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            corner_radius=8,
            width=200,
            height=45,
            state="disabled"  # Initially disabled until date is selected
        )
        self.confirm_btn.pack(pady=(0, 10))
    
    def update_calendar(self, *args):
        """Update calendar grid based on selected month and year"""
        # Clear existing calendar buttons
        for widget in self.calendar_grid.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:  # Preserve day headers
                widget.destroy()
        
        # Get selected month and year
        month = self.months.index(self.month_var.get()) + 1
        year = int(self.year_var.get())
        
        # Get first day of month and number of days
        first_day = datetime(year, month, 1)
        num_days = calendar.monthrange(year, month)[1]
        
        # Calculate first day of week (0 = Monday, 6 = Sunday)
        first_weekday = first_day.weekday()
        
        # Create calendar buttons
        day = 1
        for week in range(6):  # Maximum 6 weeks
            if day > num_days:
                break
            for weekday in range(7):
                if week == 0 and weekday < first_weekday:
                    continue
                if day > num_days:
                    break
                    
                # Create date object for this button
                current_date = datetime(year, month, day).date()
                
                # Check if date is valid (after booking_start_date)
                is_valid = current_date >= self.booking_start_date
                
                date_btn = ctk.CTkButton(
                    self.calendar_grid,
                    text=str(day),
                    command=lambda d=current_date: self.select_date(d) if is_valid else None,
                    fg_color="#1E1E1E" if is_valid else "#333333",
                    hover_color="#6200EA" if is_valid else "#333333",
                    text_color="white" if is_valid else "#666666",
                    font=ctk.CTkFont(family="Arial", size=16),
                    width=60,
                    height=60,
                    state="normal" if is_valid else "disabled",
                    corner_radius=5
                )
                date_btn.grid(row=week+1, column=weekday, padx=4, pady=4)
                day += 1
    
    def select_date(self, date):
        """Handle date selection for booking"""
        self.selected_booking_date = date
        self.return_date = date + timedelta(days=7)
        
        # Update labels
        self.selected_date_label.configure(
            text=f"Selected date: {date.strftime('%d %B %Y')}",
            text_color="white"
        )
        self.return_date_label.configure(
            text=f"Return by: {self.return_date.strftime('%d %B %Y')}"
        )
        
        # Enable confirm button and update its appearance
        self.confirm_btn.configure(
            state="normal",
            fg_color="#FF6D00",
            hover_color="#E65100"
        )
    
    def confirm_action(self):
        """Handle the confirm button action (borrow or book)"""
        if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
            messagebox.showinfo("Login Required", "Please login first.")
            self.destroy()
            if hasattr(self.controller, 'showFrame'):
                self.controller.showFrame("LoginFrame")
            return
            
        username = self.controller.current_user.get('username')
        
        try:
            if self.is_booking:
                # Handle booking
                if not self.selected_booking_date:
                    messagebox.showerror("Error", "Please select a booking date.")
                    return
                    
                # Add booking record
                self.add_booking_record(username)
                new_status = "Booked"
                action_text = "booked"
                date_text = f"\n\nYou can pick it up on {self.selected_booking_date.strftime('%d %B %Y')}."
            else:
                # Handle direct borrowing
                self.add_loan_record(username)
                new_status = "Borrowed"
                action_text = "borrowed"
                date_text = ""
            
            # Update book status in database
            if hasattr(self.controller, 'updateBookStatus'):
                success = self.controller.updateBookStatus(self.book.get('ISBN', ''), new_status)
                
                if success:
                    # Show success message
                    message = f"You have successfully {action_text} '{self.book.get('Judul', 'this book')}'.{date_text}"
                    message += f"\nPlease return by {self.return_date.strftime('%d %B %Y')}."
                    messagebox.showinfo("Success", message)
                    
                    # Close popup
                    self.destroy()
                    
                    # Refresh book details page if available
                    if hasattr(self.controller, 'refreshBookDetails'):
                        self.controller.refreshBookDetails()
                else:
                    messagebox.showerror("Error", "Failed to update book status. Please try again.")
            else:
                messagebox.showinfo("Success", f"Book has been {action_text}: {self.book.get('Judul', 'Unknown')}")
                self.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def add_booking_record(self, username):
        """Add a booking record to bookings.json"""
        booking_date = self.selected_booking_date.strftime("%Y-%m-%d")
        return_date = self.return_date.strftime("%Y-%m-%d")
        
        try:
            with open(self.bookings_file, 'r') as f:
                bookings = json.load(f)
        except:
            bookings = []
        
        # Add new booking
        bookings.append({
            "username": username,
            "isbn": self.book.get('ISBN', ''),
            "title": self.book.get('Judul', 'Unknown Title'),
            "booking_date": booking_date,
            "return_date": return_date,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        with open(self.bookings_file, 'w') as f:
            json.dump(bookings, f, indent=2)
    
    def add_loan_record(self, username):
        """Add a loan record to loans.json"""
        borrow_date = self.today.strftime("%Y-%m-%d")
        return_date = self.return_date.strftime("%Y-%m-%d")
        
        try:
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
        except:
            loans = []
        
        # Add new loan
        loans.append({
            "username": username,
            "isbn": self.book.get('ISBN', ''),
            "title": self.book.get('Judul', 'Unknown Title'),
            "borrow_date": borrow_date,
            "return_date": return_date,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        with open(self.loans_file, 'w') as f:
            json.dump(loans, f, indent=2)
    
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
        
        def borrowBook(self, book):
            print(f"Would update book status to: {book['Status']}")
            return True
        
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