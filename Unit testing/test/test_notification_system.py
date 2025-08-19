import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from notification_system import calculate_fine, is_reservation_expired


@pytest.mark.parametrize("issue_date, return_date, expected_fine", [
   
    ("2023-01-01", "2023-01-14", 0), 
    ("2023-01-01", "2023-01-10", 0),  
   
    ("2023-01-01", "2023-01-15", 5),  
    ("2023-01-01", "2023-01-20", 30), 
    ("2023-01-01", "2023-02-01", 90),  
])
def test_calculate_fine(issue_date, return_date, expected_fine):
    assert calculate_fine(issue_date, return_date) == expected_fine


@pytest.mark.parametrize("reserved_date, collected_date, today, expected", [
    
    ("2023-01-01", None, "2023-01-02", False),  
    ("2023-01-01", "2023-01-02", None, False),  
    
    ("2023-01-01", None, "2023-01-04", True),  
    ("2023-01-01", "2023-01-05", None, True),  
    ("2023-01-01", None, "2023-01-03", True),  
])
def test_is_reservation_expired(reserved_date, collected_date, today, expected):
    if today:
        with patch('notification_system.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime.strptime(today, "%Y-%m-%d")
            mock_datetime.side_effect = datetime
            assert is_reservation_expired(reserved_date) == expected
    else:
        assert is_reservation_expired(reserved_date, collected_date) == expected


@patch('notification_system.mysql.connector.connect')
def test_notification_system(mock_connect):
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
   
    mock_transactions = [
        {'TransactionID': 1, 'UserID': 101, 'BookID': 201, 
         'IssueDate': '2023-01-01', 'ReturnDate': '2023-01-15'},  # 1 day late
        {'TransactionID': 2, 'UserID': 102, 'BookID': 202, 
         'IssueDate': '2023-01-01', 'ReturnDate': '2023-01-10'},  # on time
    ]
    
    
    mock_due_books = [
        {'UserID': 103, 'BookID': 203, 'DueDate': datetime.today().date() + timedelta(days=1)},
        {'UserID': 104, 'BookID': 204, 'DueDate': datetime.today().date()},
    ]
    
    
    mock_reservations = [
        {'ReservationID': 1, 'UserID': 105, 'BookID': 205, 
         'ReservationDate': (datetime.today() - timedelta(days=3)).date()},
        {'ReservationID': 2, 'UserID': 106, 'BookID': 206, 
         'ReservationDate': (datetime.today() - timedelta(days=1)).date()},
    ]
    
   
    def mock_execute(query, params=None):
        if "ReturnDate IS NOT NULL" in query:
            mock_cursor.fetchall.return_value = mock_transactions
        elif "ReturnDate IS NULL" in query:
            mock_cursor.fetchall.return_value = mock_due_books
        elif "FROM reservation" in query:
            mock_cursor.fetchall.return_value = mock_reservations
    
    mock_cursor.execute.side_effect = mock_execute
    
    
    from notification_system import conn
    assert mock_conn.commit.called
    assert mock_cursor.close.called
    assert mock_conn.close.called
    
   
    expected_updates = [
        (5, 1),  
        (0, 2),  
    ]
    
    
    update_calls = [call for call in mock_cursor.execute.call_args_list 
                   if "UPDATE transaction" in call[0][0]]
    for call, expected in zip(update_calls, expected_updates):
        assert call[0][1] == expected
    
   
    notification_calls = [call for call in mock_cursor.execute.call_args_list 
                         if "INSERT INTO notification" in call[0][0]]
    assert len(notification_calls) == 4 