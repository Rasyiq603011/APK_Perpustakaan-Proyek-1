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
from constans import COLOR_DARK, COLOR_LIGHT, FONTS, TEXT_SIZES, SPACING, BORDER_RADIUS

ctk.deactivate_automatic_dpi_awareness()

class BaseFrame(ctk.CTkFrame):
    """Base frame class for theme management"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.load_theme_settings()
        
    def load_theme_settings(self):
        """Initialize theme settings from controller"""
        self.is_dark_mode = getattr(self.controller, 'is_dark_mode', True)
        self.color = COLOR_DARK if self.is_dark_mode else COLOR_LIGHT
        self.fonts = FONTS
        self.text_sizes = {k: int(v.replace("px", "")) for k, v in TEXT_SIZES.items()}
        self.spacing = {k: int(v.replace("px", "")) for k, v in SPACING.items()}
        self.border_radius = int(BORDER_RADIUS.replace("px", ""))
        
    def get_font(self, font_type="body", size="md", weight="normal"):
        """Helper method for consistent font styling"""
        return ctk.CTkFont(
            family=self.fonts[font_type],
            size=self.text_sizes[size],
            weight=weight
        )
        
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.is_dark_mode = not self.is_dark_mode
        self.color = COLOR_DARK if self.is_dark_mode else COLOR_LIGHT
        self.update_theme()
        
    def update_theme(self):
        """To be implemented by child classes"""
        pass


class PenaltyBookFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.configure(fg_color=self.color["surface"], corner_radius=0)
        
        # Initialize PenaltyManager
        try:
            self.penaltyManager = PenaltyManager()
            if hasattr(self.controller, 'test_mode') and self.controller.test_mode:
                self.penaltyManager.test_mode = True
                self.penaltyManager.set_test_date(self.controller.test_date)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize penalty system: {str(e)}")
            return
        
        self._current_tooltip = None
        self.create_layout()
        self.bind('<Destroy>', self.on_destroy)
        self.bind('<Visibility>', self.on_frame_shown)
    
    def create_layout(self):
        """Create the main layout structure"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Summary panel
        self.grid_rowconfigure(2, weight=1)  # Penalties list
        
        self.create_header()
        self.create_summary_panel()
        self.create_penalties_list()
        self.load_penalties()
    
    def create_header(self):
        """Create header with back button and title"""
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=self.color["primary"],
            height=60,
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_propagate(False)
        
        back_btn = ctk.CTkButton(
            self.header_frame,
            text="← Back",
            command=self.on_back_click,
            fg_color=self.color["primaryVariant"],
            hover_color=self.color["hover"]["primary"],
            text_color=self.color["primaryText"],
            font=self.get_font("body", "md", "bold"),
            corner_radius=self.border_radius,
            width=100,
            height=36
        )
        back_btn.pack(side="left", padx=self.spacing["lg"], pady=self.spacing["md"])
        
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="MY PENALTIES",
            font=self.get_font("heading", "xl", "bold"),
            text_color=self.color["primaryText"]
        )
        title_label.pack(side="left", padx=self.spacing["lg"], pady=self.spacing["md"])
    
    def create_summary_panel(self):
        """Create summary panel showing total penalties"""
        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color=self.color["surface"],
            corner_radius=self.border_radius,
            height=100,
            border_color=self.color["border"],
            border_width=1
        )
        self.summary_frame.grid(row=1, column=0, sticky="ew", 
                              padx=self.spacing["lg"], 
                              pady=(self.spacing["lg"], self.spacing["md"]))
        self.summary_frame.grid_propagate(False)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        
        # Info column
        info_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=self.spacing["lg"], pady=self.spacing["md"])
        
        self.penalty_count_label = ctk.CTkLabel(
            info_frame,
            text="You have 0 unpaid penalties",
            font=self.get_font("body", "lg", "bold"),
            text_color=self.color["primaryText"]
        )
        self.penalty_count_label.pack(anchor="w", pady=(self.spacing["md"], self.spacing["sm"]))
        
        self.penalty_info_label = ctk.CTkLabel(
            info_frame,
            text="Please pay your penalties to continue borrowing books",
            font=self.get_font("body", "sm"),
            text_color=self.color["secondaryText"]
        )
        self.penalty_info_label.pack(anchor="w")
        
        # Total column
        total_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        total_frame.grid(row=0, column=1, sticky="nsew", padx=self.spacing["lg"], pady=self.spacing["md"])
        
        ctk.CTkLabel(
            total_frame,
            text="Total Amount Due:",
            font=self.get_font("body", "md"),
            text_color=self.color["secondaryText"]
        ).pack(anchor="e", pady=(self.spacing["md"], self.spacing["sm"]))
        
        self.total_amount_label = ctk.CTkLabel(
            total_frame,
            text="Rp 0",
            font=self.get_font("body", "lg", "bold"),
            text_color=self.color["error"]
        )
        self.total_amount_label.pack(anchor="e")
    
    def create_penalties_list(self):
        """Create scrollable list for penalties"""
        self.list_container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.color["surface"],
            scrollbar_fg_color=self.color["border"],
            scrollbar_button_color=self.color["secondaryText"],
            scrollbar_button_hover_color=self.color["primaryText"],
            corner_radius=self.border_radius
        )
        self.list_container.grid(row=2, column=0, sticky="nsew", 
                               padx=self.spacing["lg"], 
                               pady=(self.spacing["md"], self.spacing["lg"]))
        
        self.penalties_list_frame = ctk.CTkFrame(self.list_container, fg_color="transparent")
        self.penalties_list_frame.pack(fill="both", expand=True)
    
    def load_penalties(self):
        """Load and display penalties for current user"""
        for widget in self.penalties_list_frame.winfo_children():
            widget.destroy()
        
        if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
            self.show_login_required()
            return
        
        username = self.controller.current_user.get("username")
        overdue_books = self.penaltyManager.getOverdueBooks(username)
        self.update_summary(overdue_books)
        self.show_penalties(overdue_books)
    
    def show_login_required(self):
        """Show message when user is not logged in"""
        login_frame = ctk.CTkFrame(
            self.penalties_list_frame, 
            fg_color=self.color["inputField"], 
            corner_radius=self.border_radius
        )
        login_frame.pack(fill="both", expand=True, 
                        padx=self.spacing["lg"], 
                        pady=self.spacing["xl"])
        
        ctk.CTkLabel(
            login_frame,
            text="Please login to view your penalties",
            font=self.get_font("heading", "lg", "bold"),
            text_color=self.color["primaryText"]
        ).pack(pady=(self.spacing["xl"], self.spacing["md"]))
        
        ctk.CTkButton(
            login_frame,
            text="Login",
            command=lambda: self.controller.showFrame("LoginFrame"),
            fg_color=self.color["primary"],
            hover_color=self.color["hover"]["primary"],
            text_color=self.color["primaryText"],
            font=self.get_font("body", "md", "bold"),
            corner_radius=self.border_radius,
            width=120,
            height=36
        ).pack(pady=(0, self.spacing["xl"]))
        
        self.penalty_count_label.configure(text="No penalties available")
        self.penalty_info_label.configure(text="Please login to view your penalties")
        self.total_amount_label.configure(text="Rp 0")
    
    def update_summary(self, penalties: List[Dict]):
        """Update summary panel with penalties data"""
        unpaid_count = len(penalties)
        total_amount = self.penaltyManager.getTotalPenalty(
            self.controller.current_user.get("username")
        ) if unpaid_count > 0 else 0
        
        penalty_text = f"You have {unpaid_count} unpaid {'penalty' if unpaid_count == 1 else 'penalties'}"
        self.penalty_count_label.configure(text=penalty_text)
        
        info_text = ("Please pay your penalties to continue borrowing books" if unpaid_count > 0
                    else "You're in good standing. Thank you for returning books on time!")
        self.penalty_info_label.configure(text=info_text)
        
        formatted_amount = self.penaltyManager.formatCurrency(total_amount)
        self.total_amount_label.configure(text=f"Rp {formatted_amount}")
    
    def show_penalties(self, penalties: List[Dict]):
        """Display all penalties for the user"""
        if not penalties:
            ctk.CTkLabel(
                self.penalties_list_frame,
                text="You have no overdue books or unpaid penalties.",
                font=self.get_font("body", "md"),
                text_color=self.color["secondaryText"]
            ).pack(pady=self.spacing["xl"])
            return
        
        for penalty in penalties:
            self.create_penalty_card(penalty)
    
    def create_penalty_card(self, penalty: Dict):
        """Create a card for a single penalty"""
        card = ctk.CTkFrame(
            self.penalties_list_frame,
            fg_color=self.color["inputField"],
            corner_radius=self.border_radius,
            border_color=self.color["border"],
            border_width=1
        )
        card.pack(fill="x", pady=self.spacing["sm"])
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, 
                          padx=self.spacing["lg"], 
                          pady=self.spacing["md"])
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        
        # Left side content
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title row
        title_row = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_row.pack(fill="x", expand=True)
        title_row.grid_columnconfigure(0, weight=1)
        title_row.grid_columnconfigure(1, weight=0)
        
        ctk.CTkLabel(
            title_row,
            text=penalty.get('title', 'Unknown Book'),
            font=self.get_font("body", "md", "bold"),
            text_color=self.color["primaryText"],
            anchor="w"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkButton(
            title_row,
            text="Pay Now",
            command=lambda p=penalty: self.show_payment_popup(p),
            fg_color=self.color["success"],
            hover_color=self.color["hover"]["primary"],
            text_color=self.color["primaryText"],
            font=self.get_font("body", "sm", "bold"),
            corner_radius=self.border_radius,
            width=120,
            height=36
        ).grid(row=0, column=1, padx=(self.spacing["md"], 0))
        
        # Due date
        days_late = penalty.get('days_overdue', 0)
        days_text = f"{days_late} {'day' if days_late == 1 else 'days'}"
        details_text = f"Due: {self.format_date(penalty.get('return_date'))} • Late by: {days_text}"
        
        ctk.CTkLabel(
            left_frame,
            text=details_text,
            font=self.get_font("body", "sm"),
            text_color=self.color["secondaryText"],
            anchor="w"
        ).pack(anchor="w", pady=self.spacing["sm"])
        
        # Bottom row
        bottom_row = ctk.CTkFrame(left_frame, fg_color="transparent")
        bottom_row.pack(fill="x", expand=True)
        bottom_row.grid_columnconfigure(0, weight=1)
        bottom_row.grid_columnconfigure(1, weight=0)
        
        # Fine amount
        fine_amount = penalty.get('fine_amount', 0)
        formatted_amount = self.penaltyManager.formatCurrency(fine_amount)
        
        ctk.CTkLabel(
            bottom_row,
            text=f"Rp {formatted_amount}",
            font=self.get_font("body", "md", "bold"),
            text_color=self.color["error"],
            anchor="w"
        ).grid(row=0, column=0, sticky="w")
        
        # Status badge
        status_frame = ctk.CTkFrame(
            bottom_row,
            fg_color=self.color["error"],
            corner_radius=self.border_radius
        )
        status_frame.grid(row=0, column=1, padx=(self.spacing["md"], 0))
        
        ctk.CTkLabel(
            status_frame,
            text="UNPAID",
            font=self.get_font("body", "sm", "bold"),
            text_color=self.color["primaryText"]
        ).pack(padx=self.spacing["md"], pady=2)
    
    def show_payment_popup(self, penalty: Dict):
        """Show payment confirmation popup with theme support"""
        popup = ctk.CTkToplevel(self)
        popup.title("BOOK-KU - Pay Penalty")
        popup.geometry("400x600")
        popup.resizable(False, False)
        popup.configure(fg_color=self.color["surface"])
        popup.transient(self)
        popup.grab_set()
        
        # Center on parent
        x = self.winfo_x() + (self.winfo_width() - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 600) // 2
        popup.geometry(f"+{int(x)}+{int(y)}")
        
        # Main container
        main_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color=self.color["surface"],
            corner_radius=self.border_radius,
            scrollbar_fg_color=self.color["border"],
            scrollbar_button_color=self.color["secondaryText"]
        )
        main_frame.pack(fill="both", expand=True, 
                       padx=self.spacing["md"], 
                       pady=self.spacing["md"])
        
        # Header
        ctk.CTkLabel(
            main_frame,
            text="Payment",
            font=self.get_font("heading", "xl", "bold"),
            text_color=self.color["primaryText"]
        ).pack(pady=(self.spacing["lg"], self.spacing["md"]))
        
        # Penalty Details section
        details_frame = ctk.CTkFrame(
            main_frame, 
            fg_color=self.color["inputField"], 
            corner_radius=self.border_radius
        )
        details_frame.pack(fill="x", padx=self.spacing["lg"], pady=self.spacing["md"])
        
        ctk.CTkLabel(
            details_frame,
            text="Penalty Details",
            font=self.get_font("body", "lg", "bold"),
            text_color=self.color["primaryText"]
        ).pack(anchor="w", padx=self.spacing["lg"], pady=(self.spacing["lg"], self.spacing["sm"]))
        
        # Book title
        ctk.CTkLabel(
            details_frame,
            text=f"Book: {penalty.get('title', 'Unknown')}",
            font=self.get_font("body", "md"),
            text_color=self.color["primaryText"],
            anchor="w"
        ).pack(anchor="w", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        # Days late
        days_late = penalty.get('days_overdue', 0)
        days_text = f"{days_late} {'day' if days_late == 1 else 'days'}"
        ctk.CTkLabel(
            details_frame,
            text=f"Late by: {days_text}",
            font=self.get_font("body", "md"),
            text_color=self.color["primaryText"],
            anchor="w"
        ).pack(anchor="w", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        # Total amount
        fine_amount = penalty.get('fine_amount', 0)
        formatted_amount = self.penaltyManager.formatCurrency(fine_amount)
        ctk.CTkLabel(
            details_frame,
            text=f"Total Amount: Rp {formatted_amount}",
            font=self.get_font("body", "md", "bold"),
            text_color=self.color["error"],
            anchor="w"
        ).pack(anchor="w", padx=self.spacing["lg"], pady=(self.spacing["sm"], self.spacing["lg"]))
        
        # Payment Method section
        method_frame = ctk.CTkFrame(
            main_frame, 
            fg_color=self.color["inputField"], 
            corner_radius=self.border_radius
        )
        method_frame.pack(fill="x", padx=self.spacing["lg"], pady=self.spacing["md"])
        
        ctk.CTkLabel(
            method_frame,
            text="Payment Method",
            font=self.get_font("body", "lg", "bold"),
            text_color=self.color["primaryText"]
        ).pack(anchor="w", padx=self.spacing["lg"], pady=(self.spacing["lg"], self.spacing["sm"]))
        
        # Payment method selection
        self.payment_method = tk.StringVar(value="bank")
        
        # Bank Transfer option
        bank_radio = ctk.CTkRadioButton(
            method_frame,
            text="Bank Transfer",
            variable=self.payment_method,
            value="bank",
            font=self.get_font("body", "md"),
            text_color=self.color["primaryText"]
        )
        bank_radio.pack(anchor="w", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        # E-Wallet option
        ewallet_radio = ctk.CTkRadioButton(
            method_frame,
            text="E-Wallet",
            variable=self.payment_method,
            value="ewallet",
            font=self.get_font("body", "md"),
            text_color=self.color["primaryText"]
        )
        ewallet_radio.pack(anchor="w", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        # Bank Transfer details frame
        self.bank_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        self.bank_frame.pack(fill="x", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        ctk.CTkLabel(
            self.bank_frame,
            text="Enter Bank Account Number:",
            font=self.get_font("body", "sm"),
            text_color=self.color["primaryText"],
            anchor="w"
        ).pack(anchor="w", pady=(self.spacing["sm"], 0))
        
        self.bank_number_entry = ctk.CTkEntry(
            self.bank_frame,
            placeholder_text="Enter bank account number",
            font=self.get_font("body", "md"),
            fg_color=self.color["surface"],
            border_color=self.color["border"],
            text_color=self.color["primaryText"],
            corner_radius=self.border_radius,
            height=35,
            width=300
        )
        self.bank_number_entry.pack(anchor="w", pady=(self.spacing["xs"], self.spacing["sm"]))
        
        ctk.CTkLabel(
            self.bank_frame,
            text="Account Name: BOOK-KU Library",
            font=self.get_font("body", "sm"),
            text_color=self.color["secondaryText"],
            anchor="w"
        ).pack(anchor="w")
        
        # E-Wallet details frame
        self.ewallet_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.ewallet_frame,
            text="Enter E-Wallet Number:",
            font=self.get_font("body", "sm"),
            text_color=self.color["primaryText"],
            anchor="w"
        ).pack(anchor="w", pady=(self.spacing["sm"], 0))
        
        self.ewallet_number_entry = ctk.CTkEntry(
            self.ewallet_frame,
            placeholder_text="Enter e-wallet number",
            font=self.get_font("body", "md"),
            fg_color=self.color["surface"],
            border_color=self.color["border"],
            text_color=self.color["primaryText"],
            corner_radius=self.border_radius,
            height=35,
            width=300
        )
        self.ewallet_number_entry.pack(anchor="w", pady=(self.spacing["xs"], self.spacing["sm"]))
        
        ctk.CTkLabel(
            self.ewallet_frame,
            text="Account Name: BOOK-KU Library",
            font=self.get_font("body", "sm"),
            text_color=self.color["secondaryText"],
            anchor="w"
        ).pack(anchor="w")
        
        # Payment Instructions
        ctk.CTkLabel(
            main_frame,
            text="Please enter your payment details and transfer the exact amount.\nClick 'Pay Now' after completing the transfer.",
            font=self.get_font("body", "sm"),
            text_color=self.color["secondaryText"],
            justify="center"
        ).pack(pady=self.spacing["lg"])
        
        # Pay button
        pay_btn = ctk.CTkButton(
            main_frame,
            text="Pay Now",
            command=lambda: self.validate_and_process_payment(penalty, popup),
            fg_color=self.color["success"],
            hover_color=self.color["hover"]["primary"],
            text_color=self.color["primaryText"],
            font=self.get_font("body", "md", "bold"),
            corner_radius=self.border_radius,
            width=360,
            height=45
        )
        pay_btn.pack(pady=(self.spacing["md"], self.spacing["lg"]))
        
        # Bind payment method change
        def update_account_visibility(*args):
            if self.payment_method.get() == "bank":
                self.bank_frame.pack(fill="x", padx=self.spacing["lg"], pady=self.spacing["sm"])
                self.ewallet_frame.pack_forget()
            else:
                self.bank_frame.pack_forget()
                self.ewallet_frame.pack(fill="x", padx=self.spacing["lg"], pady=self.spacing["sm"])
        
        self.payment_method.trace_add("write", update_account_visibility)
        update_account_visibility()  # Initial visibility
    
    def validate_and_process_payment(self, penalty: Dict, popup: ctk.CTkToplevel):
        """Validate payment details and process the payment"""
        try:
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
            
            penalty["payment_method"] = payment_method
            penalty["transfer_number"] = transfer_number
            penalty["payment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            processing = self.show_processing_overlay(popup)
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
        processing.configure(fg_color=self.color["surface"])
        
        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() - 300) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        processing.geometry(f"+{int(x)}+{int(y)}")
        
        # Processing message
        frame = ctk.CTkFrame(
            processing, 
            fg_color=self.color["inputField"], 
            corner_radius=self.border_radius
        )
        frame.pack(fill="both", expand=True, padx=self.spacing["md"], pady=self.spacing["md"])
        
        ctk.CTkLabel(
            frame,
            text="Processing Payment...",
            font=self.get_font("body", "lg", "bold"),
            text_color=self.color["primaryText"]
        ).pack(pady=(self.spacing["xl"], self.spacing["sm"]))
        
        ctk.CTkLabel(
            frame,
            text="Please wait",
            font=self.get_font("body", "md"),
            text_color=self.color["secondaryText"]
        ).pack(pady=(0, self.spacing["xl"]))
        
        return processing
    
    def complete_payment(self, penalty: Dict, popup: ctk.CTkToplevel, processing: ctk.CTkToplevel):
        """Complete the payment process"""
        try:
            if processing:
                processing.destroy()
            
            success, message = self.penaltyManager.payPenalty(
                penalty.get('isbn'),
                self.controller.current_user.get('username')
            )
            
            if success:
                formatted_amount = self.penaltyManager.formatCurrency(penalty.get('fine_amount', 0))
                messagebox.showinfo(
                    "Payment Successful",
                    f"Your payment of Rp {formatted_amount} has been processed successfully."
                )
                
                if popup:
                    popup.destroy()
                
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
                if hasattr(self.controller, 'updateBookStatus'):
                    self.controller.updateBookStatus(penalty.get('isbn'), "Available")
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
    
    def on_back_click(self):
        """Handle back button click"""
        try:
            self.penaltyManager.saveData()
            self.controller.showFrame("HomeFrame")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to navigate back: {str(e)}")
    
    def on_destroy(self, event):
        """Clean up resources when frame is destroyed"""
        try:
            if hasattr(self, '_current_tooltip') and self._current_tooltip:
                self._current_tooltip.destroy()
            if hasattr(self, 'penaltyManager'):
                self.penaltyManager.saveData()
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def on_frame_shown(self, event):
        """Update data when frame becomes visible"""
        if event.widget == self and self.winfo_viewable():
            self.load_penalties()
    
    def update_theme(self):
        """Update all UI elements with current theme colors"""
        self.configure(fg_color=self.color["surface"])
        self.header_frame.configure(fg_color=self.color["primary"])
        self.summary_frame.configure(
            fg_color=self.color["surface"],
            border_color=self.color["border"]
        )
        self.list_container.configure(
            fg_color=self.color["surface"],
            scrollbar_fg_color=self.color["border"],
            scrollbar_button_color=self.color["secondaryText"],
            scrollbar_button_hover_color=self.color["primaryText"]
        )
        self.load_penalties()


# For testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("Penalties Test")
    
    class MockController:
        def __init__(self):
            self.current_user = {"username": "test_user", "name": "Test User", "role": "user"}
            self.test_mode = True
            self.test_date = "2025-03-29"
            self.is_dark_mode = True
        
        def showFrame(self, frame_name):
            print(f"Showing frame: {frame_name}")
        
        def updateBookStatus(self, isbn, status):
            print(f"Would update book {isbn} status to {status}")
            return True
    
    controller = MockController()
    frame = PenaltyBookFrame(root, controller)
    frame.pack(fill="both", expand=True)
    
    # Add theme toggle button for testing
    def toggle_theme():
        controller.is_dark_mode = not controller.is_dark_mode
        frame.toggle_theme()
    
    ctk.CTkButton(
        root,
        text="Toggle Theme",
        command=toggle_theme,
        fg_color="#6200EA",
        hover_color="#3700B3",
        text_color="white"
    ).pack(pady=10)
    
    root.mainloop()
