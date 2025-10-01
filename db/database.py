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

    def add_movie(self, title: str, genre: str, duration: int, showtimes: str, screen: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO movies (title, genre, duration, showtimes, screen)
                VALUES (?, ?, ?, ?, ?)
            """, (title, genre, duration, showtimes, screen))
            conn.commit()

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

    def get_reservations(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations ORDER BY timestamp DESC")
            return [dict(row) for row in cursor.fetchall()]

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

    def delete_all_reservations(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations")
            conn.commit()

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

    def delete_user(self, user_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()

    def find_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def verify_user_credentials(self, username: str, password: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username=? AND password=?
            """, (username, password))
            return cursor.fetchone() is not None

    def change_user_password(self, username: str, new_password: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password=? WHERE username=?
            """, (new_password, username))
            conn.commit()