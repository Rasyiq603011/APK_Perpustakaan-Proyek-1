import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import json
from datetime import datetime, timedelta

class MyBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        # Data directory for loans and bookings
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.loans_file = os.path.join(self.data_dir, "loans.json")
        self.bookings_file = os.path.join(self.data_dir, "bookings.json")
        
        # Create the layout structure
        self.create_layout()
    
    def create_layout(self):
        # Configure layout for the frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Header
        self.rowconfigure(1, weight=0)  # Tab selector
        self.rowconfigure(2, weight=1)  # Book list
        
        # Create header with back button and title
        self.create_header()
        
        # Create tab selector for "Current" and "History"
        self.create_tab_selector()
        
        # Create book list area
        self.create_book_list()
        
        # Load initial data
        self.load_current_books()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#232323", height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)  # Fixed height
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=lambda: self.controller.showFrame("HomeFrame"),
            fg_color="#6200EA",
            hover_color="#5000D0",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=10,
            width=100,
            height=36
        )
        back_btn.pack(side="left", padx=20, pady=12)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="MY BOOKS",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=12)
    
    def create_tab_selector(self):
        tab_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(20, 10))
        tab_frame.grid_propagate(False)  # Fixed height
        
        # Create a frame for the tabs
        tabs_container = ctk.CTkFrame(tab_frame, fg_color="transparent")
        tabs_container.pack(fill="y", pady=5)
        
        # Current Books tab
        self.current_tab_btn = ctk.CTkButton(
            tabs_container,
            text="Current Books",
            command=self.load_current_books,
            fg_color="#6200EA",  # Selected state
            hover_color="#5000D0",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=8,
            width=150,
            height=36
        )
        self.current_tab_btn.pack(side="left", padx=10)
        
        # History tab
        self.history_tab_btn = ctk.CTkButton(
            tabs_container,
            text="Borrowing History",
            command=self.load_history,
            fg_color="#333333",  # Unselected state
            hover_color="#444444",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=8,
            width=150,
            height=36
        )
        self.history_tab_btn.pack(side="left", padx=10)
    
    def create_book_list(self):
        # Container for book list
        self.list_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#1E1E1E",
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#666666"
        )
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        # This will be filled when loading books
        self.book_list_frame = ctk.CTkFrame(self.list_container, fg_color="transparent")
        self.book_list_frame.pack(fill="both", expand=True)
    
    def load_current_books(self):
        """Load currently borrowed and booked books"""
        # Update tab button states
        self.current_tab_btn.configure(fg_color="#6200EA", font=ctk.CTkFont(family="Arial", size=14, weight="bold"))
        self.history_tab_btn.configure(fg_color="#333333", font=ctk.CTkFont(family="Arial", size=14))
        
        # Clear existing items
        for widget in self.book_list_frame.winfo_children():
            widget.destroy()
        
        # Check if user is logged in
        if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
            self.show_login_required()
            return
        
        username = self.controller.current_user.get("username")
        
        # Load active loans
        active_loans = self.get_active_loans(username)
        
        # Load active bookings
        active_bookings = self.get_active_bookings(username)
        
        # If no books found
        if not active_loans and not active_bookings:
            no_books_label = ctk.CTkLabel(
                self.book_list_frame,
                text="You currently have no borrowed or booked books.",
                font=ctk.CTkFont(family="Arial", size=16),
                text_color="#AAAAAA"
            )
            no_books_label.pack(pady=50)
            return
        
        # Show borrowed books section if any
        if active_loans:
            self.show_book_section(active_loans, "Currently Borrowed Books", "#4CAF50")
        
        # Show booked books section if any
        if active_bookings:
            self.show_book_section(active_bookings, "Booked Books", "#FF6D00")
    
    def load_history(self):
        """Load borrowing history"""
        # Update tab button states
        self.current_tab_btn.configure(fg_color="#333333", font=ctk.CTkFont(family="Arial", size=14))
        self.history_tab_btn.configure(fg_color="#6200EA", font=ctk.CTkFont(family="Arial", size=14, weight="bold"))
        
        # Clear existing items
        for widget in self.book_list_frame.winfo_children():
            widget.destroy()
        
        # Check if user is logged in
        if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
            self.show_login_required()
            return
        
        username = self.controller.current_user.get("username")
        
        # Load completed loans
        completed_loans = self.get_completed_loans(username)
        
        # If no history found
        if not completed_loans:
            no_history_label = ctk.CTkLabel(
                self.book_list_frame,
                text="You don't have any borrowing history yet.",
                font=ctk.CTkFont(family="Arial", size=16),
                text_color="#AAAAAA"
            )
            no_history_label.pack(pady=50)
            return
        
        # Show history
        self.show_book_section(completed_loans, "Borrowing History", "#666666")
    
    def show_login_required(self):
        """Show message when not logged in"""
        login_frame = ctk.CTkFrame(self.book_list_frame, fg_color="#2B2B2B", corner_radius=15)
        login_frame.pack(fill="both", expand=True, padx=20, pady=50)
        
        message_label = ctk.CTkLabel(
            login_frame,
            text="Please login to view your books",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white"
        )
        message_label.pack(pady=(30, 15))
        
        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            command=lambda: self.controller.showFrame("LoginFrame"),
            fg_color="#6200EA",
            hover_color="#5000D0",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            corner_radius=8,
            width=120,
            height=36
        )
        login_btn.pack(pady=(0, 30))
    
    def show_book_section(self, books, section_title, title_color):
        """Display a section of books with a title"""
        # Section title
        section_frame = ctk.CTkFrame(self.book_list_frame, fg_color="transparent")
        section_frame.pack(fill="x", pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            section_frame,
            text=section_title,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=title_color
        )
        title_label.pack(anchor="w")
        
        # Books list
        for book in books:
            self.create_book_card(book)
    
    def create_book_card(self, book):
        """Create a card for a single book"""
        # Main card container
        card = ctk.CTkFrame(self.book_list_frame, fg_color="#2B2B2B", corner_radius=10, height=120)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)  # Fixed height
        
        # Grid configuration
        card.columnconfigure(1, weight=1)  # Title column expands
        
        try:
            # Book cover (left side)
            cover_frame = ctk.CTkFrame(card, fg_color="transparent", width=80, height=120)
            cover_frame.grid(row=0, column=0, padx=10, pady=10)
            cover_frame.grid_propagate(False)
            
            # Try to load cover image
            cover_image = self.load_book_cover(book.get('isbn', ''))
            if cover_image:
                cover_label = ctk.CTkLabel(cover_frame, image=cover_image, text="")
                cover_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Book details (middle)
            details_frame = ctk.CTkFrame(card, fg_color="transparent")
            details_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            
            # Title
            title_label = ctk.CTkLabel(
                details_frame,
                text=book.get('title', 'Unknown Title'),
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white",
                anchor="w"
            )
            title_label.pack(anchor="w")
            
            # Status and dates
            status_text = f"Status: {book.get('status', 'Unknown')}"
            dates_text = f"From: {self.format_date(book.get('borrow_date'))} - Until: {self.format_date(book.get('return_date'))}"
            
            status_label = ctk.CTkLabel(
                details_frame,
                text=status_text,
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#AAAAAA",
                anchor="w"
            )
            status_label.pack(anchor="w", pady=(5, 0))
            
            dates_label = ctk.CTkLabel(
                details_frame,
                text=dates_text,
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#AAAAAA",
                anchor="w"
            )
            dates_label.pack(anchor="w", pady=(2, 0))
            
            # Buttons frame (right side)
            buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
            buttons_frame.grid(row=0, column=2, padx=10, pady=10)
            
            # Different buttons based on status
            if book.get('status') == 'Borrowed':
                return_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Return Book",
                    command=lambda b=book: self.return_book(b),
                    fg_color="#4CAF50",
                    hover_color="#388E3C",
                    text_color="white",
                    font=ctk.CTkFont(family="Arial", size=12),
                    width=100,
                    height=32
                )
                return_btn.pack(pady=2)
            
            elif book.get('status') == 'Booked':
                cancel_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Cancel Booking",
                    command=lambda b=book: self.cancel_booking(b),
                    fg_color="#F44336",
                    hover_color="#D32F2F",
                    text_color="white",
                    font=ctk.CTkFont(family="Arial", size=12),
                    width=100,
                    height=32
                )
                cancel_btn.pack(pady=2)
            
            # Details button
            details_btn = ctk.CTkButton(
                buttons_frame,
                text="Details",
                command=lambda b=book: self.show_book_details(b),
                fg_color="#666666",
                hover_color="#777777",
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=12),
                width=100,
                height=32
            )
            details_btn.pack(pady=2)
            
        except Exception as e:
            print(f"Error creating book card: {e}")
            error_label = ctk.CTkLabel(
                card,
                text="Error loading book details",
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#FF0000"
            )
            error_label.pack(pady=10)
    
    def get_active_loans(self, username):
        """Get currently borrowed books for the user"""
        try:
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
            
            # Filter active loans for current user
            active_loans = []
            for loan in loans:
                if (loan.get('username') == username and 
                    loan.get('status') == 'Borrowed' and
                    datetime.strptime(loan.get('return_date', ''), "%Y-%m-%d").date() >= datetime.now().date()):
                    active_loans.append(loan)
            
            return active_loans
        except Exception as e:
            print(f"Error loading active loans: {e}")
            return []
    
    def get_active_bookings(self, username):
        """Get currently booked books for the user"""
        try:
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
            
            # Filter active bookings for current user
            active_bookings = []
            for loan in loans:
                if (loan.get('username') == username and 
                    loan.get('status') == 'Booked' and
                    datetime.strptime(loan.get('return_date', ''), "%Y-%m-%d").date() >= datetime.now().date()):
                    active_bookings.append(loan)
            
            return active_bookings
        except Exception as e:
            print(f"Error loading active bookings: {e}")
            return []
    
    def get_completed_loans(self, username):
        """Get all completed loans for the user"""
        try:
            if os.path.exists(self.loans_file):
                with open(self.loans_file, 'r') as f:
                    loans = json.load(f)
                
                # Filter completed loans for this user
                return [
                    loan for loan in loans 
                    if loan.get('username') == username and loan.get('status') == 'completed'
                ]
        except Exception as e:
            print(f"Error loading loans: {e}")
        
        return []
    
    def load_book_cover(self, isbn):
        """Load book cover image"""
        width, height = 90, 120  # Smaller size for the card
        
        try:
            # Try to load from controller
            if hasattr(self.controller, 'loadCover'):
                cover = self.controller.loadCover(isbn)
                if cover:
                    return cover
        except Exception as e:
            print(f"Error loading cover: {e}")
        
        # Fallback to blank cover
        blank_img = Image.new('RGB', (width, height), color='#333333')
        return ctk.CTkImage(light_image=blank_img, dark_image=blank_img, size=(width, height))
    
    def format_date(self, date_str):
        """Format date string for display"""
        if not date_str or date_str == 'Unknown':
            return "Unknown"
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date.strftime("%d %b %Y")
        except:
            return date_str
    
    def show_book_details(self, book):
        """Show book details by ISBN"""
        if hasattr(self.controller, 'showBookByISBN'):
            self.controller.showBookByISBN(book.get('isbn', ''))
    
    def return_book(self, book):
        """Handle returning a borrowed book"""
        # Show return confirmation message
        from tkinter import messagebox
        result = messagebox.askyesno(
            "Return Book",
            f"Are you sure you want to return '{book.get('title')}'?"
        )
        
        if not result:
            return
        
        # Update loan status in file
        try:
            with open(self.loans_file, 'r') as f:
                loans = json.load(f)
            
            # Find and update the loan
            for loan in loans:
                if (loan.get('username') == self.controller.current_user.get('username') and 
                    loan.get('isbn') == book.get('isbn') and 
                    loan.get('status') == 'active'):
                    
                    loan['status'] = 'completed'
                    loan['actual_return_date'] = datetime.now().strftime("%Y-%m-%d")
                    
                    # Check if returned late
                    return_date = datetime.strptime(loan.get('return_date', ''), "%Y-%m-%d").date()
                    if datetime.now().date() > return_date:
                        loan['returned_late'] = True
                        # Calculate penalty days
                        days_late = (datetime.now().date() - return_date).days
                        loan['days_late'] = days_late
                        loan['penalty_amount'] = days_late * 5000  # Rp 5,000 per day
                        
                        # Add penalty record
                        self.add_penalty_record(loan)
                    else:
                        loan['returned_late'] = False
            
            # Save updated loans
            with open(self.loans_file, 'w') as f:
                json.dump(loans, f, indent=2)
            
            # Update book status in database
            if hasattr(self.controller, 'updateBookStatus'):
                self.controller.updateBookStatus(book.get('isbn', ''), "Available")
            
            messagebox.showinfo("Success", f"Book '{book.get('title')}' has been returned successfully.")
            
            # Refresh the list
            self.load_current_books()
            
        except Exception as e:
            print(f"Error returning book: {e}")
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")
    
    def add_penalty_record(self, loan):
        """Add a penalty record for late return"""
        penalty_file = os.path.join(self.data_dir, "penalties.json")
        
        try:
            # Load existing penalties
            penalties = []
            if os.path.exists(penalty_file):
                with open(penalty_file, 'r') as f:
                    penalties = json.load(f)
            
            # Add new penalty
            penalties.append({
                "username": loan.get('username', ''),
                "isbn": loan.get('isbn', ''),
                "title": loan.get('title', ''),
                "return_date": loan.get('return_date', ''),
                "actual_return_date": loan.get('actual_return_date', ''),
                "days_late": loan.get('days_late', 0),
                "amount": loan.get('penalty_amount', 0),
                "status": "unpaid",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Save penalties
            with open(penalty_file, 'w') as f:
                json.dump(penalties, f, indent=2)
                
        except Exception as e:
            print(f"Error adding penalty record: {e}")
    
    def cancel_booking(self, book):
        """Handle canceling a booking"""
        # Show cancellation confirmation message
        from tkinter import messagebox
        result = messagebox.askyesno(
            "Cancel Booking",
            f"Are you sure you want to cancel your booking for '{book.get('title')}'?"
        )
        
        if not result:
            return
        
        # Update booking status in file
        try:
            with open(self.bookings_file, 'r') as f:
                bookings = json.load(f)
            
            # Find and update the booking
            for booking in bookings:
                if (booking.get('username') == self.controller.current_user.get('username') and 
                    booking.get('isbn') == book.get('isbn') and 
                    booking.get('status') == 'active'):
                    
                    booking['status'] = 'canceled'
                    booking['canceled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save updated bookings
            with open(self.bookings_file, 'w') as f:
                json.dump(bookings, f, indent=2)
            
            # Update book status in database
            if hasattr(self.controller, 'updateBookStatus'):
                self.controller.updateBookStatus(book.get('isbn', ''), "Available")
            
            messagebox.showinfo("Success", f"Booking for '{book.get('title')}' has been canceled successfully.")
            
            # Refresh the list
            self.load_current_books()
            
        except Exception as e:
            print(f"Error canceling booking: {e}")
            messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")
    
    def read_book(self, book):
        """Simulate reading a book"""
        from tkinter import messagebox
        messagebox.showinfo("Read Book", f"Opening '{book.get('title')}' for reading...")
    
    def borrow_again(self, book):
        """Attempt to borrow a book again"""
        if hasattr(self.controller, 'showBookByISBN'):
            self.controller.showBookByISBN(book.get('isbn', ''))


# For testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("My Books Test")
    
    class MockController:
        def __init__(self):
            self.current_user = {"username": "test_user", "role": "user"}
        
        def showFrame(self, frame_name):
            print(f"Would show frame: {frame_name}")
        
        def showBookDetail(self, book):
            print(f"Would show details for book: {book.get('title')}")
        
        def showBookByISBN(self, isbn):
            print(f"Would show details for book with ISBN: {isbn}")
        
        def updateBookStatus(self, isbn, status):
            print(f"Would update book {isbn} status to {status}")
            return True
    
    controller = MockController()
    frame = MyBookFrame(root, controller)
    frame.pack(fill="both", expand=True)
    
    root.mainloop()