import sqlite3
import os
from db.database import Database

def init_database():
    db = Database()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        #!Create tables on other systems with not fully functional databases
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration INTEGER NOT NULL,
                showtimes TEXT NOT NULL,
                screen INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                movie_title TEXT NOT NULL,
                showtime TEXT NOT NULL,
                screen INTEGER NOT NULL,
                seat_numbers TEXT NOT NULL,
                total_price REAL NOT NULL,
                date TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'admin'
            )
        """)
        
        conn.commit()
    
    #!Make the receipt directory if it does not exist
    os.makedirs("receipts", exist_ok=True)

def add_sample_data(db: Database):
    #!Check if data already exists
    movies = db.get_movies()
    if movies:
        return
    
    # Admin user/ Manager user
    db.add_user("admin", "admin123", "admin")
    db.add_user("manager", "manager123", "manager")

