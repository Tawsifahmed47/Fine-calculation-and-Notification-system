class LibraryView:
    @staticmethod
    def display_fine(amount):
        if amount > 0:
            print(f"\nFine due: BDT {amount}")
        else:
            print("\nNo fine due. Thank you for returning on time!")

    @staticmethod
    def display_reservation_status(expired):
        if expired:
            print("Reservation status: EXPIRED")
        else:
            print("Reservation status: ACTIVE")

    @staticmethod
    def display_error(message):
        print(f"Error: {message}")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt).strip()

    @staticmethod
    def display_menu():
        print("\nLibrary System Menu:")
        print("1. Calculate Fine")
        print("2. Check Reservation Status")
        print("3. Exit")