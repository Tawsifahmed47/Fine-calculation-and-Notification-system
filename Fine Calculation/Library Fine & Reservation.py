from datetime import datetime, timedelta

FINE_PER_DAY = 5 
BORROW_PERIOD_DAYS = 14
RESERVATION_EXPIRY_DAYS = 2

def calculate_fine(issue_date_str, return_date_str):
    """
    Calculates fine for overdue books.

    :param issue_date_str: str in 'YYYY-MM-DD'
    :param return_date_str: str in 'YYYY-MM-DD'
    :return: int fine amount
    """
    issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d").date()
    return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
    
    allowed_return_date = issue_date + timedelta(days=BORROW_PERIOD_DAYS)

    if return_date > allowed_return_date:
        overdue_days = (return_date - allowed_return_date).days
        fine = overdue_days * FINE_PER_DAY
        return fine
    else:
        return 0


def is_reservation_expired(reserved_date_str, collected_date_str=None):
    """
    Checks if reservation is still valid or expired.

    :param reserved_date_str: str in 'YYYY-MM-DD'
    :param collected_date_str: str in 'YYYY-MM-DD' or None
    :return: bool (True if expired, False if still valid)
    """
    reserved_date = datetime.strptime(reserved_date_str, "%Y-%m-%d").date()
    expiry_date = reserved_date + timedelta(days=RESERVATION_EXPIRY_DAYS)

    if collected_date_str:
        collected_date = datetime.strptime(collected_date_str, "%Y-%m-%d").date()
        return collected_date > expiry_date
    else:
        
        today = datetime.today().date()
        return today > expiry_date





# Fine Calculation
issue_date = "2025-07-01"
return_date = "2025-07-20"
fine = calculate_fine(issue_date, return_date)
print(f"Fine: BDT {fine}")

# Reservation Expiry Check
reserved_date = "2025-08-05"
collected_date = "2025-08-08"
expired = is_reservation_expired(reserved_date, collected_date)
print("Reservation Expired:", "Yes" if expired else "No")
