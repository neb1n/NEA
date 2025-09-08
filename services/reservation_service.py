from db.database import Database
from services.email_service import EmailService
from typing import List, Dict, Any
import os
from datetime import datetime

class ReservationService:
    def __init__(self):
        #!Reservation service (Need to change the prices to be more variable)
        self.db = Database()
        self.email_service = EmailService()
        self.regular_price = 12.0
        self.premium_price = 18.0
        self.premium_seats = ['C4', 'C5', 'C6', 'C7', 'D4', 'D5', 'D6', 'D7', 'E4', 'E5', 'E6', 'E7']
    
    #!Checks for already reserved seats
    def get_reserved_seats(self, movie_title: str, showtime: str, screen: int) -> List[str]:
        return self.db.get_reserved_seats(movie_title, showtime, screen)
    
    #!Calculates the total price of the reservation
    def calculate_total_price(self, seat_numbers: List[str]) -> float:
        total = 0.0
        for seat in seat_numbers:
            if seat in self.premium_seats:
                total += self.premium_price
            else:
                total += self.regular_price
        return total
    
    #!Makes the reservation
    def make_reservation(self, customer_name: str, customer_email: str, customer_phone: str,
                        movie_title: str, showtime: str, screen: int, seat_numbers: List[str], date: str) -> bool:
        try:
            #!Check if seats are available
            reserved_seats = self.get_reserved_seats(movie_title, showtime, screen)
            for seat in seat_numbers:
                if seat in reserved_seats:
                    raise Exception(f"Seat {seat} is already reserved")
            
            #!Calculate total price
            total_price = self.calculate_total_price(seat_numbers)
            
            #!Make reservation
            seat_numbers_str = ','.join(seat_numbers)
            reservation_id = self.db.add_reservation(
                customer_name, customer_email, customer_phone,
                movie_title, showtime, screen, seat_numbers_str, total_price, date
            )
            
            #!Generate receipt
            receipt_data = {
                'reservation_id': reservation_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'movie_title': movie_title,
                'showtime': showtime,
                'screen': screen,
                'seat_numbers': seat_numbers_str,
                'total_price': total_price,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'date': date
            }
            
            self.generate_receipt(receipt_data)
            
            #!Send confirmation email (Rememeber still need to fix)
            self.email_service.send_confirmation_email(customer_email, receipt_data)
            
            return True
            
        except Exception as e:
            print(f"Error making reservation: {e}")
            return False
    
    #!Creation of the receipt
    def generate_receipt(self, receipt_data: Dict[str, Any]):
        receipt_filename = f"receipts/receipt_{receipt_data['reservation_id']}_{receipt_data['timestamp'].replace(':', '-').replace(' ', '_')}.txt"
        
        with open(receipt_filename, 'w') as f:
            f.write("=" * 50 + "\n") #!Aesthetic
            f.write("NUTWARK RECEIPT\n")
            f.write("=" * 50 + "\n\n") #!Aesthetic
            f.write(f"Reservation ID: {receipt_data['reservation_id']}\n") #!ID
            f.write(f"Date: {receipt_data['timestamp']}\n\n") #!Date
            f.write(f"Customer: {receipt_data['customer_name']}\n") #!Name
            f.write(f"Email: {receipt_data['customer_email']}\n") #!Email
            f.write(f"Phone: {receipt_data['customer_phone']}\n\n") #!Phone
            f.write(f"Movie: {receipt_data['movie_title']}\n") #!Title
            f.write(f"Showtime: {receipt_data['showtime']}\n") #!Showtime
            f.write(f"Screen: {receipt_data['screen']}\n") #!Screen
            f.write(f"Seats: {receipt_data['seat_numbers']}\n\n") #!Seats
            f.write(f"Total Price: ${receipt_data['total_price']:.2f}\n") #!Total price
            f.write("\n" + "=" * 50 + "\n") #!Aesthetic
            f.write("Thank you for choosing our theater!\n")
            f.write("=" * 50 + "\n") #!Aesthetic
    
    def get_all_reservations(self) -> List[Dict[str, Any]]:
        #!Fetches all reservations from the database
        return self.db.get_reservations()
    
    def get_reservation_stats(self) -> Dict[str, Any]:
        #!Calculates reservation stats
        reservations = self.get_all_reservations()
        
        total_reservations = len(reservations)
        total_revenue = sum(r['total_price'] for r in reservations)
        
        #!Occupants of the screen
        screen_stats = {}
        for screen in range(1, 5):
            screen_reservations = [r for r in reservations if r['screen'] == screen]
            screen_stats[screen] = len(screen_reservations)
        
        return {
            'total_reservations': total_reservations,
            'total_revenue': total_revenue,
            'screen_stats': screen_stats
        }