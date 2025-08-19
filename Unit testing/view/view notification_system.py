class NotificationView:
    @staticmethod
    def display_success(message: str) -> None:
        print(f"SUCCESS: {message}")
        
    @staticmethod
    def display_error(error: str) -> None:
        print(f"ERROR: {error}")