from model import LibraryModel
from view import LibraryView

class LibraryController:
    def __init__(self):
        self.model = LibraryModel()
        self.view = LibraryView()

    def calculate_fine(self):
        try:
            issue_date = self.view.get_user_input("Enter issue date (YYYY-MM-DD): ")
            return_date = self.view.get_user_input("Enter return date (YYYY-MM-DD): ")
            fine = self.model.calculate_fine(issue_date, return_date)
            self.view.display_fine(fine)
        except ValueError as e:
            self.view.display_error(str(e))

    def check_reservation(self):
        try:
            reserved_date = self.view.get_user_input("Enter reservation date (YYYY-MM-DD): ")
            collected_date = self.view.get_user_input("Enter collection date (leave empty if not collected): ")
            
            expired = self.model.is_reservation_expired(
                reserved_date, 
                collected_date if collected_date else None
            )
            
            self.view.display_reservation_status(expired)
        except ValueError as e:
            self.view.display_error(str(e))

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_user_input("Enter your choice: ")
            
            if choice == "1":
                self.calculate_fine()
            elif choice == "2":
                self.check_reservation()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                self.view.display_error("Invalid choice. Please try again.")