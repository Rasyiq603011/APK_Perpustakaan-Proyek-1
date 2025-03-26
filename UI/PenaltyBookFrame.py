import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable, List, Any
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Moduls.Penalty_Manager import PenaltyManager
ctk.deactivate_automatic_dpi_awareness() 
class PenaltyBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        # Initialize PenaltyManager
        try:
            self.penaltyManager = PenaltyManager()
            if hasattr(self.controller, 'test_mode') and self.controller.test_mode:
                self.penaltyManager.test_mode = True
                self.penaltyManager.set_test_date(self.controller.test_date)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize penalty system: {str(e)}")
            return
        
        # Create the layout structure
        self.create_layout()
        
        # Bind window close event
        self.bind('<Destroy>', self.on_destroy)
        
        # Store current tooltip
        self._current_tooltip = None
        
        # Update data when frame is shown
        self.bind('<Visibility>', self.on_frame_shown)
    
    def on_destroy(self, event):
        """Clean up resources when frame is destroyed"""
        try:
            if hasattr(self, '_current_tooltip') and self._current_tooltip:
                self._current_tooltip.destroy()
            if hasattr(self, 'penaltyManager'):
                self.penaltyManager.saveData()
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def create_layout(self):
        """Create the main layout structure"""
        try:
            # Configure layout for the frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=0)  # Header
            self.rowconfigure(1, weight=0)  # Summary panel
            self.rowconfigure(2, weight=1)  # Penalties list
            
            # Create header with back button and title
            self.create_header()
            
            # Create summary panel
            self.create_summary_panel()
            
            # Create penalties list
            self.create_penalties_list()
            
            # Load penalties data
            self.load_penalties()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create layout: {str(e)}")
    
    def create_header(self):
        """Create the header section with back button and title"""
        header_frame = ctk.CTkFrame(self, fg_color="#232323", height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.on_back_click,
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
            text="MY PENALTIES",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=12)
    
    def on_back_click(self):
        """Handle back button click"""
        try:
            if hasattr(self, 'penaltyManager'):
                self.penaltyManager.saveData()
            self.controller.showFrame("HomeFrame")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to navigate back: {str(e)}")
    
    def create_summary_panel(self):
        """Create the summary panel showing total penalties"""
        self.summary_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=15, height=100)
        self.summary_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.summary_frame.grid_propagate(False)
        
        # Two-column layout
        self.summary_frame.columnconfigure(0, weight=1)  # Info column
        self.summary_frame.columnconfigure(1, weight=1)  # Total column
        
        # Left side: Penalties info
        info_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
        self.penalty_count_label = ctk.CTkLabel(
            info_frame,
            text="You have 0 unpaid penalties",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="white"
        )
        self.penalty_count_label.pack(anchor="w", pady=(10, 5))
        
        self.penalty_info_label = ctk.CTkLabel(
            info_frame,
            text="Please pay your penalties to continue borrowing books",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA"
        )
        self.penalty_info_label.pack(anchor="w")
        
        # Right side: Total amount
        total_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        total_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        
        total_text_label = ctk.CTkLabel(
            total_frame,
            text="Total Amount Due:",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#AAAAAA"
        )
        total_text_label.pack(anchor="e", pady=(10, 5))
        
        self.total_amount_label = ctk.CTkLabel(
            total_frame,
            text="Rp 0",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="#F44336"
        )
        self.total_amount_label.pack(anchor="e")
    
    def create_penalties_list(self):
        """Create the scrollable list for penalties"""
        self.list_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#1E1E1E",
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#666666",
            scrollbar_button_hover_color="#888888"
        )
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        self.penalties_list_frame = ctk.CTkFrame(self.list_container, fg_color="transparent")
        self.penalties_list_frame.pack(fill="both", expand=True)
    
    def load_penalties(self):
        """Load and display penalties for the current user"""
        try:
            # Clear existing items
            for widget in self.penalties_list_frame.winfo_children():
                widget.destroy()
            
            # Check if user is logged in
            if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
                self.show_login_required()
                return
            
            username = self.controller.current_user.get("name")
            
            # Load overdue books using PenaltyManager
            overdue_books = self.penaltyManager.getOverdueBooks(username)
            
            # Update summary panel
            self.update_summary(overdue_books)
            
            # Show penalties
            self.show_penalties(overdue_books)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load penalties: {str(e)}")
    
    def show_login_required(self):
        """Show message when user is not logged in"""
        login_frame = ctk.CTkFrame(self.penalties_list_frame, fg_color="#2B2B2B", corner_radius=15)
        login_frame.pack(fill="both", expand=True, padx=20, pady=50)
        
        message_label = ctk.CTkLabel(
            login_frame,
            text="Please login to view your penalties",
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
        
        # Update summary panel
        self.penalty_count_label.configure(text="No penalties available")
        self.penalty_info_label.configure(text="Please login to view your penalties")
        self.total_amount_label.configure(text="Rp 0")
    
    def update_summary(self, penalties: List[Dict]):
        """Update the summary panel with penalties data"""
        try:
            # Count unpaid penalties
            unpaid_count = len(penalties)
            
            # Calculate total amount
            total_amount = 0
            if unpaid_count > 0:
                total_amount = self.penaltyManager.getTotalPenalty(
                    self.controller.current_user.get("username")
                )
            
            # Update labels
            penalty_text = f"You have {unpaid_count} unpaid {'penalty' if unpaid_count == 1 else 'penalties'}"
            self.penalty_count_label.configure(text=penalty_text)
            
            if unpaid_count > 0:
                info_text = "Please pay your penalties to continue borrowing books"
            else:
                info_text = "You're in good standing. Thank you for returning books on time!"
            
            self.penalty_info_label.configure(text=info_text)
            
            # Format amount
            formatted_amount = self.penaltyManager.formatCurrency(total_amount)
            self.total_amount_label.configure(text=f"Rp {formatted_amount}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update summary: {str(e)}")
    
    def show_penalties(self, penalties: List[Dict]):
        """Display all penalties for the user"""
        try:
            if not penalties:
                no_penalties_label = ctk.CTkLabel(
                    self.penalties_list_frame,
                    text="You have no overdue books or unpaid penalties.",
                    font=ctk.CTkFont(family="Arial", size=16),
                    text_color="#AAAAAA"
                )
                no_penalties_label.pack(pady=50)
                return
            
            # Create card for each penalty
            for penalty in penalties:
                self.create_penalty_card(penalty)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display penalties: {str(e)}")
    
    def create_penalty_card(self, penalty: Dict):
        """Create a card for a single penalty"""
        try:
            # Main card container
            card = ctk.CTkFrame(self.penalties_list_frame, fg_color="#2B2B2B", corner_radius=10)
            card.pack(fill="x", pady=10)
            
            # Content area with two columns
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=20, pady=15)
            content_frame.grid_columnconfigure(0, weight=1)  # Left side
            content_frame.grid_columnconfigure(1, weight=0)  # Right side
            
            # Left side content
            left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="nsew")
            
            # Book title and Pay Now button row
            title_row = ctk.CTkFrame(left_frame, fg_color="transparent")
            title_row.pack(fill="x", expand=True)
            title_row.grid_columnconfigure(0, weight=1)
            title_row.grid_columnconfigure(1, weight=0)
            
            # Book title
            title_label = ctk.CTkLabel(
                title_row,
                text=penalty.get('title', 'Unknown Book'),
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white",
                anchor="w"
            )
            title_label.grid(row=0, column=0, sticky="w")
            
            # Pay Now button - Aligned with title
            pay_btn = ctk.CTkButton(
                title_row,
                text="Pay Now",
                command=lambda p=penalty: self.show_payment_popup(p),
                fg_color="#4CAF50",
                hover_color="#388E3C",
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                corner_radius=8,
                width=120,
                height=36
            )
            pay_btn.grid(row=0, column=1, padx=(10, 0))
            
            # Due date and days late
            days_late = penalty.get('days_overdue', 0)
            days_text = f"{days_late} {'day' if days_late == 1 else 'days'}"
            details_text = f"Due: {self.format_date(penalty.get('return_date'))} • Late by: {days_text}"
            
            details_label = ctk.CTkLabel(
                left_frame,
                text=details_text,
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#AAAAAA",
                anchor="w"
            )
            details_label.pack(anchor="w", pady=5)
            
            # Fine amount and UNPAID badge row
            bottom_row = ctk.CTkFrame(left_frame, fg_color="transparent")
            bottom_row.pack(fill="x", expand=True)
            bottom_row.grid_columnconfigure(0, weight=1)
            bottom_row.grid_columnconfigure(1, weight=0)
            
            # Fine amount
            fine_amount = penalty.get('fine_amount', 0)
            formatted_amount = self.penaltyManager.formatCurrency(fine_amount)
            
            amount_label = ctk.CTkLabel(
                bottom_row,
                text=f"Rp {formatted_amount}",
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                text_color="#F44336",
                anchor="w"
            )
            amount_label.grid(row=0, column=0, sticky="w")
            
            # Status badge (UNPAID) - Aligned with amount
            status_frame = ctk.CTkFrame(bottom_row, fg_color="#F44336", corner_radius=4)
            status_frame.grid(row=0, column=1, padx=(10, 0))
            
            status_label = ctk.CTkLabel(
                status_frame,
                text="UNPAID",
                font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
                text_color="white"
            )
            status_label.pack(padx=10, pady=2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create penalty card: {str(e)}")
    
    def show_payment_popup(self, penalty: Dict):
        """Show payment confirmation popup"""
        try:
            # Create popup window
            popup = ctk.CTkToplevel(self)
            popup.title("BOOK-KU - Pay Penalty")
            popup.geometry("400x600")
            popup.resizable(False, False)
            
            # Make the popup modal
            popup.transient(self)
            popup.grab_set()
            
            # Center on parent
            x = self.winfo_x() + (self.winfo_width() - 400) // 2
            y = self.winfo_y() + (self.winfo_height() - 600) // 2
            popup.geometry(f"+{int(x)}+{int(y)}")
            
            # Main container with scrollable content
            main_frame = ctk.CTkScrollableFrame(
                popup,
                fg_color="#232323",
                corner_radius=15,
                scrollbar_fg_color="#333333",
                scrollbar_button_color="#666666"
            )
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Header
            header_label = ctk.CTkLabel(
                main_frame,
                text="Payment",
                font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
                text_color="white"
            )
            header_label.pack(pady=(20, 10))
            
            # Penalty Details section
            details_frame = ctk.CTkFrame(main_frame, fg_color="#2B2B2B", corner_radius=10)
            details_frame.pack(fill="x", padx=20, pady=10)
            
            details_title = ctk.CTkLabel(
                details_frame,
                text="Penalty Details",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white"
            )
            details_title.pack(anchor="w", padx=20, pady=(15, 10))
            
            # Book title
            book_label = ctk.CTkLabel(
                details_frame,
                text=f"Book: {penalty.get('title', 'Unknown')}",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                anchor="w"
            )
            book_label.pack(anchor="w", padx=20, pady=5)
            
            # Days late
            days_late = penalty.get('days_overdue', 0)
            days_text = f"{days_late} {'day' if days_late == 1 else 'days'}"
            days_label = ctk.CTkLabel(
                details_frame,
                text=f"Late by: {days_text}",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                anchor="w"
            )
            days_label.pack(anchor="w", padx=20, pady=5)
            
            # Total amount
            fine_amount = penalty.get('fine_amount', 0)
            formatted_amount = self.penaltyManager.formatCurrency(fine_amount)
            amount_label = ctk.CTkLabel(
                details_frame,
                text=f"Total Amount: Rp {formatted_amount}",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="#F44336",
                anchor="w"
            )
            amount_label.pack(anchor="w", padx=20, pady=(5, 15))
            
            # Payment Method section
            method_frame = ctk.CTkFrame(main_frame, fg_color="#2B2B2B", corner_radius=10)
            method_frame.pack(fill="x", padx=20, pady=10)
            
            method_title = ctk.CTkLabel(
                method_frame,
                text="Payment Method",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                text_color="white"
            )
            method_title.pack(anchor="w", padx=20, pady=(15, 10))
            
            # Payment method selection
            self.payment_method = tk.StringVar(value="bank")
            
            # Bank Transfer option
            bank_radio = ctk.CTkRadioButton(
                method_frame,
                text="Bank Transfer",
                variable=self.payment_method,
                value="bank",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white"
            )
            bank_radio.pack(anchor="w", padx=20, pady=5)
            
            # E-Wallet option
            ewallet_radio = ctk.CTkRadioButton(
                method_frame,
                text="E-Wallet",
                variable=self.payment_method,
                value="ewallet",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white"
            )
            ewallet_radio.pack(anchor="w", padx=20, pady=5)
            
            # Bank Transfer details frame
            self.bank_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
            self.bank_frame.pack(fill="x", padx=20, pady=10)
            
            bank_number_label = ctk.CTkLabel(
                self.bank_frame,
                text="Enter Bank Account Number:",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                anchor="w"
            )
            bank_number_label.pack(anchor="w", pady=(10, 0))
            
            self.bank_number_entry = ctk.CTkEntry(
                self.bank_frame,
                placeholder_text="Enter bank account number",
                font=ctk.CTkFont(family="Arial", size=14),
                height=35,
                width=300
            )
            self.bank_number_entry.pack(anchor="w", pady=(5, 10))
            
            bank_holder = ctk.CTkLabel(
                self.bank_frame,
                text="Account Name: BOOK-KU Library",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#AAAAAA",
                anchor="w"
            )
            bank_holder.pack(anchor="w")
            
            # E-Wallet details frame
            self.ewallet_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
            
            ewallet_number_label = ctk.CTkLabel(
                self.ewallet_frame,
                text="Enter E-Wallet Number:",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="white",
                anchor="w"
            )
            ewallet_number_label.pack(anchor="w", pady=(10, 0))
            
            self.ewallet_number_entry = ctk.CTkEntry(
                self.ewallet_frame,
                placeholder_text="Enter e-wallet number",
                font=ctk.CTkFont(family="Arial", size=14),
                height=35,
                width=300
            )
            self.ewallet_number_entry.pack(anchor="w", pady=(5, 10))
            
            ewallet_holder = ctk.CTkLabel(
                self.ewallet_frame,
                text="Account Name: BOOK-KU Library",
                font=ctk.CTkFont(family="Arial", size=14),
                text_color="#AAAAAA",
                anchor="w"
            )
            ewallet_holder.pack(anchor="w")
            
            # Payment Instructions
            instruction_label = ctk.CTkLabel(
                main_frame,
                text="Please enter your payment details and transfer the exact amount.\nClick 'Pay Now' after completing the transfer.",
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="#AAAAAA",
                justify="center"
            )
            instruction_label.pack(pady=15)
            
            # Pay button
            pay_btn = ctk.CTkButton(
                main_frame,
                text="Pay Now",
                command=lambda: self.validate_and_process_payment(penalty, popup),
                fg_color="#4CAF50",
                hover_color="#388E3C",
                text_color="white",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                corner_radius=8,
                width=360,
                height=45
            )
            pay_btn.pack(pady=(10, 20))
            
            # Bind payment method change
            def update_account_visibility(*args):
                if self.payment_method.get() == "bank":
                    self.bank_frame.pack(fill="x", padx=20, pady=5)
                    self.ewallet_frame.pack_forget()
                else:
                    self.bank_frame.pack_forget()
                    self.ewallet_frame.pack(fill="x", padx=20, pady=5)
            
            self.payment_method.trace_add("write", update_account_visibility)
            update_account_visibility()  # Initial visibility
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show payment popup: {str(e)}")
    
    def validate_and_process_payment(self, penalty: Dict, popup: ctk.CTkToplevel):
        """Validate payment details and process the payment"""
        try:
            # Get the selected payment method and corresponding number
            payment_method = self.payment_method.get()
            transfer_number = ""
            
            if payment_method == "bank":
                transfer_number = self.bank_number_entry.get().strip()
                if not transfer_number:
                    messagebox.showerror("Error", "Please enter your bank account number")
                    return
                if not transfer_number.replace("-", "").isdigit():
                    messagebox.showerror("Error", "Bank account number should contain only digits and hyphens")
                    return
            else:  # e-wallet
                transfer_number = self.ewallet_number_entry.get().strip()
                if not transfer_number:
                    messagebox.showerror("Error", "Please enter your e-wallet number")
                    return
                if not transfer_number.replace("-", "").isdigit():
                    messagebox.showerror("Error", "E-wallet number should contain only digits and hyphens")
                    return
            
            # Add payment details to penalty data
            penalty["payment_method"] = payment_method
            penalty["transfer_number"] = transfer_number
            penalty["payment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Show processing message
            processing = self.show_processing_overlay(popup)
            
            # Process payment after a short delay
            self.after(1000, lambda: self.complete_payment(penalty, popup, processing))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process payment: {str(e)}")
    
    def show_processing_overlay(self, parent: ctk.CTkToplevel) -> ctk.CTkToplevel:
        """Show processing overlay window"""
        processing = ctk.CTkToplevel(parent)
        processing.title("")
        processing.geometry("300x150")
        processing.resizable(False, False)
        processing.transient(parent)
        processing.grab_set()
        
        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() - 300) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        processing.geometry(f"+{int(x)}+{int(y)}")
        
        # Processing message
        frame = ctk.CTkFrame(processing, fg_color="#232323", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            frame,
            text="Processing Payment...",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="white"
        ).pack(pady=(30, 10))
        
        ctk.CTkLabel(
            frame,
            text="Please wait",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA"
        ).pack(pady=(0, 10))
        
        return processing
    
    def complete_payment(self, penalty: Dict, popup: ctk.CTkToplevel, processing: ctk.CTkToplevel):
        """Complete the payment process"""
        try:
            # Close processing window
            if processing:
                processing.destroy()
            
            # Process payment through PenaltyManager
            success, message = self.penaltyManager.payPenalty(
                penalty.get('isbn'),
                self.controller.current_user.get('username')
            )
            
            if success:
                # Show success message
                formatted_amount = self.penaltyManager.formatCurrency(penalty.get('fine_amount', 0))
                messagebox.showinfo(
                    "Payment Successful",
                    f"Your payment of Rp {formatted_amount} has been processed successfully."
                )
                
                # Close popup
                if popup:
                    popup.destroy()
                
                # Refresh penalties list
                self.load_penalties()
            else:
                messagebox.showerror("Error", message or "Failed to process payment")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete payment: {str(e)}")
    
    def return_book(self, penalty: Dict):
        """Process book return after payment"""
        try:
            success, message = self.penaltyManager.returnBook(
                penalty.get('isbn'),
                self.controller.current_user.get('username')
            )
            
            if success:
                # Update book status in database if available
                if hasattr(self.controller, 'updateBookStatus'):
                    self.controller.updateBookStatus(penalty.get('isbn'), "Available")
                
                # Refresh penalties list
                self.load_penalties()
            else:
                messagebox.showerror("Return Failed", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")
    
    def format_date(self, date_str: str) -> str:
        """Format date string for display"""
        if not date_str:
            return "Unknown"
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date.strftime("%d %b %Y")
        except:
            return date_str
    
    def on_frame_shown(self, event):
        """Update data when frame becomes visible"""
        if event.widget == self and self.winfo_viewable():
            self.load_penalties()  


# For testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("Penalties Test")
    
    class MockController:
        def __init__(self):
            self.current_user = {"username": "test_user", "role": "user"}
            self.test_mode = True
            self.test_date = "2025-03-29"
        
        def showFrame(self, frame_name):
            if frame_name in self.frames:
                frame = self.frames[frame_name]

            if frame_name == "PenaltyFrame":
                if hasattr(frame, "load_penalties"):
                    frame.load_penalties()

            frame.tkraise()
        
        def updateBookStatus(self, isbn, status):
            print(f"Would update book {isbn} status to {status}")
            return True
    
    controller = MockController()
    frame = PenaltyBookFrame(root, controller)
    frame.pack(fill="both", expand=True)
    
    root.mainloop()