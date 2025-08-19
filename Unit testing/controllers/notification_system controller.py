from datetime import datetime, timedelta
from model import LMSModel
from typing import Optional

class NotificationController:
    FINE_PER_DAY: float = 5.0
    BORROW_PERIOD_DAYS: int = 14
    RESERVATION_EXPIRY_DAYS: int = 2
    
    def __init__(self, model: LMSModel):
        self.model = model
        
    def calculate_fine(self, issue_date, return_date) -> float:
        """Calculate fine for overdue book"""
        try:
            issue_date = datetime.strptime(str(issue_date), "%Y-%m-%d").date()
            return_date = datetime.strptime(str(return_date), "%Y-%m-%d").date()
            allowed_return_date = issue_date + timedelta(days=self.BORROW_PERIOD_DAYS)
            
            if return_date > allowed_return_date:
                overdue_days = (return_date - allowed_return_date).days
                return overdue_days * self.FINE_PER_DAY
            return 0.0
        except (ValueError, TypeError) as err:
            raise ValueError(f"Invalid date format: {err}")
        
    def is_reservation_expired(self, reserved_date, collected_date: Optional[str] = None) -> bool:
        """Check if reservation has expired"""
        try:
            reserved_date = datetime.strptime(str(reserved_date), "%Y-%m-%d").date()
            expiry_date = reserved_date + timedelta(days=self.RESERVATION_EXPIRY_DAYS)
            
            if collected_date:
                collected_date = datetime.strptime(str(collected_date), "%Y-%m-%d").date()
                return collected_date > expiry_date
            return datetime.today().date() > expiry_date
        except (ValueError, TypeError) as err:
            raise ValueError(f"Invalid date format: {err}")
        
    def process_all_notifications(self) -> None:
        """Process all notifications (fines, due dates, reservations)"""
        
        transactions = self.model.get_completed_transactions()
        for tx in transactions:
            fine = self.calculate_fine(tx['IssueDate'], tx['ReturnDate'])
            self.model.update_fine(tx['TransactionID'], fine)
            
            if fine > 0:
                message = f"You have an unpaid fine of BDT {fine} for book (ID {tx['BookID']})."
                self.model.create_notification(tx['UserID'], message)
        
       
        pending_books = self.model.get_pending_transactions()
        for book in pending_books:
            due_date = book['DueDate']
            if 0 <= (due_date - datetime.today().date()).days <= 2:
                message = f"Reminder: Your book (ID {book['BookID']}) is due on {due_date}."
                self.model.create_notification(book['UserID'], message)
        
        
        reservations = self.model.get_all_reservations()
        for res in reservations:
            if self.is_reservation_expired(res['ReservationDate']):
                message = f"Your reservation for book (ID {res['BookID']}) has expired."
                self.model.create_notification(res['UserID'], message)
        
        self.model.commit()