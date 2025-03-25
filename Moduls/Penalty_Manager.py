import json
import time
import os
import locale
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path

class PenaltyManager:
    def __init__(self, loansFile="data/loans.json", penaltiesFile="data/penalties.json", test_mode=False):
        self.loansFile = loansFile
        self.penaltiesFile = penaltiesFile
        self.loans: List[Dict] = []
        self.penalties: List[Dict] = []
        self.dailyPenaltyRate = 5000  # Rp5000 per day
        self.test_mode = test_mode
        self.test_current_date = None
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.loansFile), exist_ok=True)
        os.makedirs(os.path.dirname(self.penaltiesFile), exist_ok=True)
        
        # Set locale for currency formatting
        try:
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except:
                pass
        
        self.loadData()
        self.updatePenalties()
    
    def set_test_date(self, date_str: str) -> None:
        """Set a custom date for testing purposes."""
        if self.test_mode:
            try:
                self.test_current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")
    
    def get_current_date(self) -> datetime.date:
        """Get current date, using test date if in test mode."""
        if self.test_mode and self.test_current_date:
            return self.test_current_date
        return datetime.now().date()
    
    def atomic_write_json(self, file_path: str, data: Any) -> bool:
        """Write data to JSON file atomically to prevent corruption."""
        temp_path = f"{file_path}.tmp"
        backup_path = f"{file_path}.bak"
    
        try:
            # Write to temp file with lock
            with open(temp_path, 'w') as f:
                if os.name == 'posix':  # Unix
                    import fcntl
                    fcntl.flock(f, fcntl.LOCK_EX)
                elif os.name == 'nt':  # Windows
                    import msvcrt
                    msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            
                json.dump(data, f, indent=2)
            
                if os.name == 'posix':
                    fcntl.flock(f, fcntl.LOCK_UN)
        
            # Atomic replace
            if os.path.exists(file_path):
                os.replace(file_path, backup_path)
            os.replace(temp_path, file_path)
        
            if os.path.exists(backup_path):
                os.remove(backup_path)
            return True
        except Exception as e:
            if os.path.exists(backup_path):
                os.replace(backup_path, file_path)
            raise e
    
    def loadData(self) -> None:
        """Load loans and penalties from JSON files with error handling."""
        try:
            # Load loans.json
            if os.path.exists(self.loansFile):
                with open(self.loansFile, "r") as file:
                    self.loans = json.load(file)
            else:
                self.loans = []
                self.atomic_write_json(self.loansFile, self.loans)
            
            # Load penalties.json
            if os.path.exists(self.penaltiesFile):
                with open(self.penaltiesFile, "r") as file:
                    self.penalties = json.load(file)
            else:
                self.penalties = []
                self.atomic_write_json(self.penaltiesFile, self.penalties)
                    
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data in files: {str(e)}")
        except Exception as e:
            raise IOError(f"Error loading data: {str(e)}")
    
    def validate_loan_data(self, loan_data: Dict) -> Tuple[bool, str]:
        """Validate loan data before saving."""
        required_fields = ["username", "isbn", "title", "borrow_date", "return_date", "status", "created_at"]
    
        for field in required_fields:
            if field not in loan_data or not loan_data[field]:
                return False, f"Field '{field}' is required and cannot be empty"
    
        if not str(loan_data["isbn"]).isdigit():
            return False, "ISBN must be a number"
    
        try:
            borrow_date = datetime.strptime(loan_data["borrow_date"], "%Y-%m-%d").date()
            return_date = datetime.strptime(loan_data["return_date"], "%Y-%m-%d").date()
            if return_date < borrow_date:
                return False, "Return date cannot be earlier than borrow date"
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
        return True, "Data is valid"


    def validate_penalty_data(self, penalty_data: Dict) -> Tuple[bool, str]:
        """Validate penalty data before saving."""
        required_fields = ["isbn", "username", "amount", "days_overdue", "status", "created_at"]
        
        # Check required fields
        for field in required_fields:
            if field not in penalty_data:
                return False, f"Missing required field: {field}"
        
        # Validate numeric fields
        try:
            if not isinstance(penalty_data["amount"], (int, float)) or penalty_data["amount"] < 0:
                return False, "Invalid penalty amount"
            if not isinstance(penalty_data["days_overdue"], int) or penalty_data["days_overdue"] < 0:
                return False, "Invalid days overdue"
        except (TypeError, ValueError):
            return False, "Invalid numeric values"
        
        return True, "Data is valid"

    def saveData(self) -> bool:
        """Save loans and penalties to JSON files."""
        try:
            # Validate loans data
            for loan in self.loans:
                isValid, message = self.validate_loan_data(loan)
                if not isValid:
                    print(f"Invalid loan data: {message}")
                    return False

            # Validate penalties data
            for penalty in self.penalties:
                isValid, message = self.validate_penalty_data(penalty)
                if not isValid:
                    print(f"Invalid penalty data: {message}")
                    return False

            # Save loans with proper formatting
            with open(self.loansFile, "w") as file:
                json.dump(self.loans, file, indent=2)
            
            # Save penalties with proper formatting
            with open(self.penaltiesFile, "w") as file:
                json.dump(self.penalties, file, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def delete_loan(self, loan_id: str) -> Tuple[bool, str]:
        """Delete a loan by its ID."""
        try:
            original_length = len(self.loans)
            self.loans = [loan for loan in self.loans if loan.get("id") != loan_id]
            
            if len(self.loans) == original_length:
                return False, "Loan not found"
            
            if self.saveData():
                return True, "Loan deleted successfully"
            return False, "Error saving data"
            
        except Exception as e:
            return False, f"Error deleting loan: {str(e)}"

    def delete_penalty(self, penalty_id: str) -> Tuple[bool, str]:
        """Delete a penalty by its ID."""
        try:
            original_length = len(self.penalties)
            self.penalties = [penalty for penalty in self.penalties if penalty.get("id") != penalty_id]
            
            if len(self.penalties) == original_length:
                return False, "Penalty not found"
            
            if self.saveData():
                return True, "Penalty deleted successfully"
            return False, "Error saving data"
            
        except Exception as e:
            return False, f"Error deleting penalty: {str(e)}"
    
    def borrowBook(self, bookId: str, userId: str = "default_user", durationDays: int = 7) -> Tuple[bool, str]:
        """Record a book borrowing transaction."""
        try:
            # Input validation
            if not bookId or not isinstance(bookId, (str, int)):
                return False, "Invalid book ID"
            
            if not userId or not isinstance(userId, str):
                return False, "Invalid user ID"
                
            if not isinstance(durationDays, int) or durationDays <= 0:
                return False, "Duration must be a positive integer"
            
            # Convert bookId to string for consistency
            bookId = str(bookId)
            
            # Check if book is already borrowed
            for loan in self.loans:
                if str(loan["isbn"]) == bookId and loan["status"] == "active":
                    return False, "Book is already borrowed"
            
            # Check if user has unpaid penalties
            if self.getTotalPenalty(userId) > 0:
                return False, "Cannot borrow books while having unpaid penalties"
            
            # Calculate dates
            current_date = self.get_current_date()
            borrow_date = current_date.strftime("%Y-%m-%d")
            return_date = (current_date + timedelta(days=durationDays)).strftime("%Y-%m-%d")
            
            # Create new loan record
            newLoan = {
                "username": userId,
                "isbn": bookId,
                "title": "",  # This should be filled by the caller
                "borrow_date": borrow_date,
                "return_date": return_date,
                "status": "active",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Validate loan data
            isValid, message = self.validate_loan_data(newLoan)
            if not isValid:
                return False, message
            
            self.loans.append(newLoan)
            self.updatePenalties()  # Update penalties after adding new loan
            if self.saveData():
                return True, "Book borrowed successfully"
            return False, "Error saving loan data"
            
        except Exception as e:
            return False, f"Error processing loan: {str(e)}"
    
    def updatePenalties(self) -> None:
        """Update penalties for all overdue books."""
        try:
            current_date = self.get_current_date()
        
            for loan in self.loans:
                if loan["status"] == "active":
                    due_date = datetime.strptime(loan["return_date"], "%Y-%m-%d").date()
                    if current_date > due_date:
                        days_overdue = (current_date - due_date).days
                        penalty_amount = days_overdue * self.dailyPenaltyRate
                    
                        # Check if penalty already exists
                        existing_penalty = next(
                            (p for p in self.penalties 
                            if p["isbn"] == loan["isbn"] and 
                            p["username"] == loan["username"] and 
                            p["status"] == "active"), 
                            None
                        )
                    
                        if existing_penalty:
                            existing_penalty["amount"] = penalty_amount
                            existing_penalty["days_overdue"] = days_overdue
                            existing_penalty["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            new_penalty = {
                                "isbn": loan["isbn"],
                                "username": loan["username"],
                                "title": loan["title"],
                                "amount": penalty_amount,
                                "days_overdue": days_overdue,
                                "status": "active",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        
                            # Validate penalty data
                            is_valid, message = self.validate_penalty_data(new_penalty)
                            if is_valid:
                                self.penalties.append(new_penalty)
        
            self.saveData()
        
        except Exception as e:
            print(f"Error updating penalties: {e}")
    
    def getBorrowedBooks(self, userId: str = "default_user") -> List[Dict]:
        """Get list of books borrowed by a user."""
        try:
            self.updatePenalties()
            return [loan for loan in self.loans 
                    if loan["username"] == userId and loan["status"] == "active"]
        except Exception as e:
            print(f"Error getting borrowed books: {e}")
            return []
    
    def getOverdueBooks(self, userId: str = "default_user") -> List[Dict]:
        """Get list of overdue books for a user."""
        try:
            self.updatePenalties()
            current_date = self.get_current_date()
            
            overdue_books = []
            for loan in self.loans:
                if (loan["username"] == userId and 
                    loan["status"] == "active"):
                    
                    return_date = datetime.strptime(loan["return_date"], "%Y-%m-%d").date()
                    if current_date > return_date:
                        # Calculate days overdue and fine
                        days_overdue = (current_date - return_date).days
                        fine_amount = days_overdue * self.dailyPenaltyRate
                        
                        # Add fine information to loan record
                        loan_with_fine = loan.copy()
                        loan_with_fine["days_overdue"] = days_overdue
                        loan_with_fine["fine_amount"] = fine_amount
                        
                        overdue_books.append(loan_with_fine)
            
            return overdue_books
            
        except Exception as e:
            print(f"Error getting overdue books: {e}")
            return []
    
    def getTotalPenalty(self, userId: str) -> int:
        """Get total penalty amount for a user."""
        try:
            # Get only active overdue books
            overdueBooks = self.getOverdueBooks(userId)
            
            # Calculate total only if there are overdue books
            if not overdueBooks:
                return 0
                
            return sum(book.get("fine_amount", 0) for book in overdueBooks)
        except Exception as e:
            print(f"Error calculating total penalty: {e}")
            return 0
    
    def formatCurrency(self, amount: int) -> str:
        """Format amount as Indonesian Rupiah."""
        try:
            return locale.currency(amount, grouping=True, symbol=False)
        except:
            return f"{amount:,}".replace(',', '.')
    
    def payPenalty(self, bookId: str, userId: str = None) -> Tuple[bool, str]:
        """Pay penalty for a book."""
        try:
            # Find the active loan
            loan = next(
                (l for l in self.loans 
                 if str(l["isbn"]) == str(bookId) and l["status"] == "active"),
                None
            )
            
            if not loan:
                return False, "No active loan found for this book"
            
            if userId and loan["username"] != userId:
                return False, "This loan belongs to another user"
            
            # Calculate the penalty amount
            days_overdue = self.getDaysOverdue(bookId)
            if days_overdue <= 0:
                return False, "No penalty due for this book"
            
            penalty_amount = days_overdue * self.dailyPenaltyRate
            
            # Update or create penalty record
            penalty = next(
                (p for p in self.penalties 
                 if str(p["isbn"]) == str(bookId) and p["status"] == "active"),
                None
            )
            
            if penalty:
                penalty["status"] = "paid"
                penalty["paid_amount"] = penalty_amount
                penalty["paid_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_penalty = {
                    "isbn": bookId,
                    "username": loan["username"],
                    "amount": penalty_amount,
                    "days_overdue": days_overdue,
                    "status": "paid",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "paid_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "paid_amount": penalty_amount
                }
                self.penalties.append(new_penalty)
            
            # Update loan status to completed
            loan["status"] = "completed"
            loan["actual_return_date"] = datetime.now().strftime("%Y-%m-%d")
            
            if self.saveData():
                return True, "Penalty paid successfully"
            return False, "Error saving penalty payment"
                
        except Exception as e:
            return False, f"Error processing penalty payment: {str(e)}"
    
    def returnBook(self, bookId: str, userId: str = "default_user") -> Tuple[bool, str]:
        """Process book return."""
        try:
            # Find active loan
            loan = next(
                (l for l in self.loans 
                 if str(l["isbn"]) == str(bookId) and 
                 l["username"] == userId and 
                 l["status"] == "active"),
                None
            )
            
            if not loan:
                return False, "No active loan found for this book"
            
            # Check for unpaid penalties
            penalty = next(
                (p for p in self.penalties 
                 if str(p["isbn"]) == str(bookId) and 
                 p["username"] == userId and 
                 p["status"] == "active"),
                None
            )
            
            if penalty:
                return False, "Please pay the penalty before returning the book"
            
            # Update loan status
            currentDate = self.get_current_date()
            loan["status"] = "completed"
            loan["actual_return_date"] = currentDate.strftime("%Y-%m-%d")
            loan["returned_late"] = datetime.strptime(loan["return_date"], "%Y-%m-%d").date() < currentDate
            
            self.updatePenalties()  # Update penalties after return
            if self.saveData():
                return True, "Book returned successfully"
            return False, "Error saving book return"
                
        except Exception as e:
            return False, f"Error processing book return: {str(e)}"
    
    def getDaysRemaining(self, bookId: str) -> int:
        """Get days remaining until due date."""
        try:
            loan = next(
                (l for l in self.loans 
                 if str(l["isbn"]) == str(bookId) and l["status"] == "active"), 
                None
            )
            
            if not loan:
                return 0
            
            due_date = datetime.strptime(loan["return_date"], "%Y-%m-%d").date()
            current_date = self.get_current_date()
            
            if due_date < current_date:
                return 0  # Overdue
            
            return (due_date - current_date).days
            
        except Exception as e:
            print(f"Error calculating days remaining: {e}")
            return 0
    
    def getDaysOverdue(self, bookId: str) -> int:
        """Get days overdue for a book."""
        try:
            loan = next(
                (l for l in self.loans 
                 if str(l["isbn"]) == str(bookId) and l["status"] == "active"), 
                None
            )
            
            if not loan:
                return 0
            
            due_date = datetime.strptime(loan["return_date"], "%Y-%m-%d").date()
            current_date = self.get_current_date()
            
            if current_date <= due_date:
                return 0  # Not overdue
            
            return (current_date - due_date).days
            
        except Exception as e:
            print(f"Error calculating days overdue: {e}")
            return 0
    
    def getBooksApproachingDueDate(self, userId: str = "default_user", daysThreshold: int = 2) -> List[Dict]:
        """Get books that are approaching their due date."""
        try:
            current_date = self.get_current_date()
            threshold_date = current_date + timedelta(days=daysThreshold)
            
            return [loan for loan in self.loans 
                    if loan["username"] == userId 
                    and loan["status"] == "active"
                    and current_date < datetime.strptime(loan["return_date"], "%Y-%m-%d").date() <= threshold_date]
        except Exception as e:
            print(f"Error getting books approaching due date: {e}")
            return []
    
    def getTransactionHistory(self, userId: str = "default_user") -> List[Dict]:
        """Get transaction history for a user."""
        try:
            return [loan for loan in self.loans if loan["username"] == userId]
        except Exception as e:
            print(f"Error getting transaction history: {e}")
            return []