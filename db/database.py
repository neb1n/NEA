import sqlite3
from contextlib import contextmanager
from typing import List, Optional, Dict, Any

class Database:
    def __init__(self, db_path: str = "movie_theater.db"):
        self.db_path = db_path #!Setting the path of the database file

    @contextmanager
    def get_connection(self): #!Creating the connection to the database
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    #!The CRUD for movies
    def get_movies(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            return [dict(row) for row in cursor.fetchall()]
    #!Adding movies with input coming from the textboxes
    def add_movie(self, title: str, genre: str, duration: int, showtimes: str, screen: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO movies (title, genre, duration, showtimes, screen)
                VALUES (?, ?, ?, ?, ?)
            """, (title, genre, duration, showtimes, screen))
            conn.commit()
    #!Updating movies based on the information changed but changes all the information as to keep current updates
    def update_movie(self, movie_id: int, title: str, genre: str, duration: int, showtimes: str, screen: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE movies SET title=?, genre=?, duration=?, showtimes=?, screen=?
                WHERE id=?
            """, (title, genre, duration, showtimes, screen, movie_id))
            conn.commit()

    def delete_movie(self, movie_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
            conn.commit()

    #!Reservation CRUD operations
    def add_reservation(self, customer_name: str, customer_email: str, customer_phone: str,
                       movie_title: str, showtime: str, screen: int, seat_numbers: str, total_price: float, date: str): #! Long ahh parse
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservations (customer_name, customer_email, customer_phone,
                                        movie_title, showtime, screen, seat_numbers, total_price, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_name, customer_email, customer_phone, movie_title, showtime, screen, seat_numbers, total_price, date))
            conn.commit()
            return cursor.lastrowid
    #!Gets all reservations from the database and orders them by their timestamp
    def get_reservations(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations ORDER BY timestamp DESC")
            return [dict(row) for row in cursor.fetchall()]
    #!Gets all the reserved seats which can also be used in the seat_map.py
    def get_reserved_seats(self, movie_title: str, showtime: str, screen: int) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT seat_numbers FROM reservations
                WHERE movie_title=? AND showtime=? AND screen=?
            """, (movie_title, showtime, screen))
            
            reserved_seats = []
            for row in cursor.fetchall():
                seats = row['seat_numbers'].split(',')
                reserved_seats.extend([seat.strip() for seat in seats])
            return reserved_seats
    #!Fetches the reservation by the ID as to process a refund
    def get_reservation_by_id(self, reservation_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
        
    #!Fetches the reservation by the ID as to process a refund
    def delete_reservation_by_id(self, reservation_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
            conn.commit()
            return cursor.rowcount > 0
    #!Deletes the reservations when the button is pressed
    def delete_all_reservations(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations")
            conn.commit()
    #!Deletes the reservations when the movie is deleted
    def delete_reservations_by_movie(self, movie_title: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations WHERE movie_title=?", (movie_title,))
            conn.commit()

    #!User management methods
    def add_user(self, username: str, password_hash: str, role: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))
            conn.commit()
    
    def get_users(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]

    def verify_user_credentials(self, username: str, password: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username=? AND password=?
            """, (username, password))
            return cursor.fetchone() is not None
