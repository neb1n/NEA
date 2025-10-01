from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

#!Model for the reservations
@dataclass
class Reservation:
    id: Optional[int] = None
    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""
    movie_title: str = ""
    showtime: str = ""
    screen: int = 1
    seat_numbers: List[str] = None
    date: str = ""  
    timestamp: Optional[datetime] = None
    total_price: float = 0.0
    
    def __post_init__(self):
        if self.seat_numbers is None:
            self.seat_numbers = []
        if self.timestamp is None:
            self.timestamp = datetime.now()