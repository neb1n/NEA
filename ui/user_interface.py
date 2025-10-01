import tkinter as tk
from tkinter import ttk, messagebox
from services.movie_service import MovieService
from services.reservation_service import ReservationService
from ui.seat_map import SeatMap
import re

class UserInterface:
    def __init__(self, parent, admin_login_callback=None):
        self.parent = parent
        self.movie_service = MovieService()
        self.reservation_service = ReservationService()
        self.admin_login_callback = admin_login_callback

        self.selected_movie = None
        self.selected_showtime = None
        self.selected_screen = None
        self.seat_map = None

        self.setup_styles()
        self.setup_ui()
        self.load_movies()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Main.TFrame", background="#f5f6fa")
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), background="#f5f6fa", foreground="#273c75")
        style.configure("Section.TLabelframe", font=("Segoe UI", 14, "bold"), background="#f5f6fa", foreground="#353b48")
        style.configure("TButton", font=("Segoe UI", 12), padding=8)
        style.configure("TLabel", font=("Segoe UI", 12), background="#f5f6fa")
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("TCombobox", font=("Segoe UI", 12))

    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Top bar with title and admin login button
        top_bar = ttk.Frame(self.main_frame, style="Main.TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(top_bar, text="🎬 Movie Reservation System", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=(0, 20))

        if self.admin_login_callback:
            admin_btn = ttk.Button(top_bar, text="Admin Login", command=self.admin_login_callback, style="TButton")
            admin_btn.pack(side=tk.RIGHT, padx=(0, 10))
            admin_btn.bind("<Enter>", lambda e: admin_btn.config(cursor="hand2"))

        # Movie selection frame
        movie_frame = ttk.LabelFrame(self.main_frame, text="Select Movie", style="Section.TLabelframe", padding="16")
        movie_frame.pack(fill=tk.X, pady=(0, 15))

        self.movie_listbox = tk.Listbox(movie_frame, height=5, font=("Segoe UI", 12), bg="#fff", bd=0, highlightthickness=1, relief="flat")
        self.movie_listbox.pack(fill=tk.X)
        self.movie_listbox.bind('<<ListboxSelect>>', self.on_movie_selected)

        # Showtime selection frame
        showtime_frame = ttk.LabelFrame(self.main_frame, text="Select Showtime", style="Section.TLabelframe", padding="16")
        showtime_frame.pack(fill=tk.X, pady=(0, 15))

        self.showtime_var = tk.StringVar()
        self.showtime_combo = ttk.Combobox(showtime_frame, textvariable=self.showtime_var, state="readonly", style="TCombobox")
        self.showtime_combo.pack(fill=tk.X)
        self.showtime_combo.bind('<<ComboboxSelected>>', self.on_showtime_selected)

        # Seat selection frame
        seat_frame = ttk.LabelFrame(self.main_frame, text="Select Seats", style="Section.TLabelframe", padding="16")
        seat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.seat_container = seat_frame

        # Customer details frame
        details_frame = ttk.LabelFrame(self.main_frame, text="Customer Details", style="Section.TLabelframe", padding="16")
        details_frame.pack(fill=tk.X, pady=(0, 15))

        form_frame = ttk.Frame(details_frame, style="Main.TFrame")
        form_frame.pack(fill=tk.X)

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.name_entry = ttk.Entry(form_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=(0, 20), pady=5)

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=(0, 5), pady=5)
        self.email_entry = ttk.Entry(form_frame, width=25)
        self.email_entry.grid(row=0, column=3, pady=5)

        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=5)
        self.phone_entry = ttk.Entry(form_frame, width=25)
        self.phone_entry.grid(row=1, column=1, pady=5)

        # Date
        ttk.Label(form_frame, text="Date (DD-MM-YYYY):").grid(row=2, column=0, sticky="w", padx=(0, 5), pady=5)
        self.date_entry = ttk.Entry(form_frame, width=25)
        self.date_entry.grid(row=2, column=1, padx=(0, 20), pady=5)

        # Selected seats display
        ttk.Label(form_frame, text="Selected Seats:").grid(row=1, column=2, sticky="w", padx=(0, 5), pady=5)
        self.selected_seats_label = ttk.Label(form_frame, text="None", foreground="#0097e6")
        self.selected_seats_label.grid(row=1, column=3, pady=5)

        # Reserve button
        self.reserve_btn = ttk.Button(form_frame, text="Make Reservation", command=self.make_reservation, style="TButton")
        self.reserve_btn.grid(row=2, column=2, columnspan=2, pady=(15, 0), sticky="ew")

    def load_movies(self):
        movies = self.movie_service.get_all_movies()
        self.movie_listbox.delete(0, tk.END)

        for movie in movies:
            display_text = f"{movie['title']} ({movie['genre']}) - {movie['duration']} min - Screen {movie['screen']}"
            self.movie_listbox.insert(tk.END, display_text)

    def on_movie_selected(self, event):
        selection = self.movie_listbox.curselection()
        if not selection:
            return

        movie_index = selection[0]
        movies = self.movie_service.get_all_movies()

        if movie_index < len(movies):
            self.selected_movie = movies[movie_index]
            self.selected_screen = self.selected_movie['screen']

            # Load showtimes
            showtimes = self.selected_movie['showtimes'].split(',')
            self.showtime_combo['values'] = showtimes
            self.showtime_combo.set('')

            # Clear seat selection
            self.clear_seat_selection()

    def on_showtime_selected(self, event):
        self.selected_showtime = self.showtime_var.get()
        self.load_seat_map()

    def load_seat_map(self):
        if not self.selected_movie or not self.selected_showtime:
            return

        # Clear existing seat map
        for widget in self.seat_container.winfo_children():
            widget.destroy()

        # Create new seat map
        self.seat_map = SeatMap(self.seat_container, self.on_seat_selected)

        # Load reserved seats
        reserved_seats = self.reservation_service.get_reserved_seats(
            self.selected_movie['title'], self.selected_showtime, self.selected_screen
        )
        self.seat_map.set_reserved_seats(reserved_seats)

    def on_seat_selected(self, seat_id):
        selected_seats = self.seat_map.get_selected_seats()
        if selected_seats:
            self.selected_seats_label.config(text=', '.join(selected_seats))
        else:
            self.selected_seats_label.config(text="None")

    def clear_seat_selection(self):
        if self.seat_map:
            self.seat_map.clear_selection()
        self.selected_seats_label.config(text="None")

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
        return re.match(pattern, phone) is not None

    def make_reservation(self):
        # Validate inputs
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        date = self.date_entry.get().strip()

        if not name or not email or not phone:
            messagebox.showerror("Error", "Please fill in all customer details")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Please enter a valid phone number")
            return

        if not self.selected_movie or not self.selected_showtime:
            messagebox.showerror("Error", "Please select a movie and showtime")
            return

        selected_seats = self.seat_map.get_selected_seats()
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        # Calculate total price for confirmation
        total_price = self.reservation_service.calculate_total_price(selected_seats)

        # Confirm reservation
        message = f"Reservation Summary:\n\n"
        message += f"Movie: {self.selected_movie['title']}\n"
        message += f"Showtime: {self.selected_showtime}\n"
        message += f"Screen: {self.selected_screen}\n"
        message += f"Seats: {', '.join(selected_seats)}\n"
        message += f"Total Price: ${total_price:.2f}\n\n"
        message += "Confirm reservation?"

        if messagebox.askyesno("Confirm Reservation", message):
            success = self.reservation_service.make_reservation(
                name, email, phone, self.selected_movie['title'],
                self.selected_showtime, self.selected_screen, selected_seats, date
            )
            if success:
                messagebox.showinfo("Success", "Reservation completed!")
                self.reset_form()
            else:
                messagebox.showerror("Error", "Reservation failed. Please try again.")

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.movie_listbox.selection_clear(0, tk.END)
        self.showtime_combo.set('')
        self.selected_seats_label.config(text="None")
        self.clear_seat_selection()
        self.selected_movie = None
        self.selected_showtime = None
        self.selected_screen = None