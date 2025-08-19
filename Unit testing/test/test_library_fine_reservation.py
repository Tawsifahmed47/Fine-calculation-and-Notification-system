import pytest
from datetime import datetime, timedelta
from library import calculate_fine, is_reservation_expired

class TestCalculateFine:
    def test_no_fine_for_early_return(self):
        issue_date = "2025-01-01"
        return_date = "2025-01-10"  
        assert calculate_fine(issue_date, return_date) == 0

    def test_no_fine_for_on_time_return(self):
        issue_date = "2025-01-01"
        return_date = "2025-01-15"  
        assert calculate_fine(issue_date, return_date) == 0

    def test_fine_for_late_return(self):
        issue_date = "2025-01-01"
        return_date = "2025-01-20"  
        assert calculate_fine(issue_date, return_date) == 25 

    def test_fine_for_much_later_return(self):
        issue_date = "2025-01-01"
        return_date = "2025-02-15"  
        assert calculate_fine(issue_date, return_date) == 155  

    def test_invalid_date_format(self):
        with pytest.raises(ValueError):
            calculate_fine("01-01-2025", "2025-01-15")  

class TestIsReservationExpired:
    def test_not_expired_without_collection(self):
        reserved_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        assert is_reservation_expired(reserved_date) == False

    def test_expired_without_collection(self):
        reserved_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        assert is_reservation_expired(reserved_date) == True

    def test_not_expired_with_collection(self):
        reserved_date = "2025-01-01"
        collected_date = "2025-01-02"  
        assert is_reservation_expired(reserved_date, collected_date) == False

    def test_expired_with_collection(self):
        reserved_date = "2025-01-01"
        collected_date = "2025-01-04"  
        assert is_reservation_expired(reserved_date, collected_date) == True

    def test_invalid_date_format(self):
        with pytest.raises(ValueError):
            is_reservation_expired("01-01-2025")  