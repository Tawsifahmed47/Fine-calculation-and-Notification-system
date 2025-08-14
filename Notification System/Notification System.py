import mysql.connector
from datetime import datetime, timedelta


FINE_PER_DAY = 5
BORROW_PERIOD_DAYS = 14
RESERVATION_EXPIRY_DAYS = 2


def calculate_fine(issue_date, return_date):
    issue_date = datetime.strptime(str(issue_date), "%Y-%m-%d").date()
    return_date = datetime.strptime(str(return_date), "%Y-%m-%d").date()
    allowed_return_date = issue_date + timedelta(days=BORROW_PERIOD_DAYS)

    if return_date > allowed_return_date:
        overdue_days = (return_date - allowed_return_date).days
        return overdue_days * FINE_PER_DAY
    else:
        return 0


def is_reservation_expired(reserved_date, collected_date=None):
    reserved_date = datetime.strptime(str(reserved_date), "%Y-%m-%d").date()
    expiry_date = reserved_date + timedelta(days=RESERVATION_EXPIRY_DAYS)

    if collected_date:
        collected_date = datetime.strptime(str(collected_date), "%Y-%m-%d").date()
        return collected_date > expiry_date
    else:
        return datetime.today().date() > expiry_date


conn = mysql.connector.connect(
    host="localhost",      
    user="your_username",  
    password="your_password",  
    database="lms"
)
cursor = conn.cursor(dictionary=True)


cursor.execute("""
    SELECT TransactionID, UserID, BookID, IssueDate, ReturnDate 
    FROM transaction 
    WHERE ReturnDate IS NOT NULL
""")
transactions = cursor.fetchall()

for tx in transactions:
    fine = calculate_fine(tx['IssueDate'], tx['ReturnDate'])
    cursor.execute("UPDATE transaction SET Fine = %s WHERE TransactionID = %s", (fine, tx['TransactionID']))

    if fine > 0:
        message = f"You have an unpaid fine of BDT {fine} for book (ID {tx['BookID']})."
        cursor.execute("INSERT INTO notification (UserID, Message) VALUES (%s, %s)", (tx['UserID'], message))


cursor.execute("""
    SELECT UserID, BookID, DueDate 
    FROM transaction 
    WHERE ReturnDate IS NULL
""")
due_books = cursor.fetchall()

for dbk in due_books:
    due_date = dbk['DueDate']
    if 0 <= (due_date - datetime.today().date()).days <= 2:
        message = f"Reminder: Your book (ID {dbk['BookID']}) is due on {due_date}."
        cursor.execute("INSERT INTO notification (UserID, Message) VALUES (%s, %s)", (dbk['UserID'], message))


cursor.execute("SELECT ReservationID, UserID, BookID, ReservationDate FROM reservation")
reservations = cursor.fetchall()

for res in reservations:
    if is_reservation_expired(res['ReservationDate']):
        message = f"Your reservation for book (ID {res['BookID']}) has expired."
        cursor.execute("INSERT INTO notification (UserID, Message) VALUES (%s, %s)", (res['UserID'], message))


# Commit and Close
conn.commit()
cursor.close()
conn.close()

print("Fines updated & notifications sent successfully.")
