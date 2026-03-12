import tkinter as tk
from tkinter import ttk, messagebox
from services.movie_service import MovieService
from services.reservation_service import ReservationService
from ui.seat_map import SeatMap
from ui.landing_page import LandingPage
from ui.theme import Colors
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
        self.current_page = None

        self.setup_ui()
        self.show_landing_page()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def clear_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_landing_page(self):
        self.clear_page()
        self.current_page = LandingPage(
            self.main_frame, 
            self.show_reservation_page,
            self.admin_login_callback
        )

    def show_reservation_page(self, movie):
        self.clear_page()
        self.selected_movie = movie
        self.selected_screen = movie['screen']
        
        # Create reservation frame with theme background
        style = ttk.Style()
        style.configure("Reservation.TFrame", background=Colors.BACKGROUND)
        style.configure("Reservation.TLabelframe", background=Colors.BACKGROUND, foreground=Colors.TEXT)
        res_frame = ttk.Frame(self.main_frame, style="Reservation.TFrame")
        res_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        res_frame.configure()
        
        # Back button (subtle style consistent with theme)
        back_btn = tk.Button(res_frame, text="← Back to Movies", bg=Colors.CARD_BG, fg=Colors.TEXT,
                             activebackground=Colors.ACCENT_HOVER, activeforeground=Colors.CTA_FG,
                             relief="groove", bd=1, cursor="hand2", command=self.show_landing_page)
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # Title
        title_label = tk.Label(res_frame, text=f"Reserve: {movie['title']}", 
                               font=("Segoe UI", 20, "bold"), bg=Colors.BACKGROUND, fg=Colors.TEXT)
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Showtime selection
        showtime_frame = ttk.LabelFrame(res_frame, text="Select Showtime", padding="16", style="Reservation.TLabelframe")
        showtime_frame.pack(fill=tk.X, pady=(0, 15))

        self.showtime_var = tk.StringVar()
        showtimes = self.selected_movie['showtimes'].split(',')
        self.showtime_combo = ttk.Combobox(showtime_frame, textvariable=self.showtime_var, 
                                          values=showtimes, state="readonly")
        self.showtime_combo.pack(fill=tk.X)
        self.showtime_combo.bind('<<ComboboxSelected>>', self.on_showtime_selected)

        # Seat selection container (will hold the seat map)
        seat_frame = ttk.LabelFrame(res_frame, text="Select Seats", padding="16", style="Reservation.TLabelframe")
        seat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        # give seat_frame a soft bg to match theme
        try:
            seat_frame.configure(style="Reservation.TLabelframe")
        except Exception:
            pass
        self.seat_container = seat_frame

        # Customer details
        details_frame = ttk.LabelFrame(res_frame, text="Customer Details", padding="16", style="Reservation.TLabelframe")
        details_frame.pack(fill=tk.X, pady=(0, 15))

        # Labels/Entries — ensure readable text color & consistent spacing
        lbl_opts = {"bg": Colors.BACKGROUND, "fg": Colors.TEXT, "font": ("Segoe UI", 10)}
        ttk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(details_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(details_frame, text="Email:").grid(row=0, column=2, sticky="w", pady=5)
        self.email_entry = ttk.Entry(details_frame, width=25)
        self.email_entry.grid(row=0, column=3, pady=5)

        ttk.Label(details_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=5)
        self.phone_entry = ttk.Entry(details_frame, width=25)
        self.phone_entry.grid(row=1, column=1, pady=5)

        ttk.Label(details_frame, text="Date (DD-MM-YYYY):").grid(row=1, column=2, sticky="w", pady=5)
        self.date_entry = ttk.Entry(details_frame, width=25)
        self.date_entry.grid(row=1, column=3, pady=5)

        # Reserve button — styled to match theme
        self.reserve_btn = tk.Button(details_frame, text="Complete Reservation", bg=Colors.ACCENT, fg=Colors.CTA_FG,
                                     activebackground=Colors.ACCENT_HOVER, activeforeground=Colors.CTA_FG,
                                     relief="flat", cursor="hand2", command=self.make_reservation)
        self.reserve_btn.grid(row=2, column=2, columnspan=2, pady=15, sticky="ew")

    def on_showtime_selected(self, event):
        self.selected_showtime = self.showtime_var.get()
        self.load_seat_map()

    def load_seat_map(self):
        # Clear previous seat map
        for widget in self.seat_container.winfo_children():
            widget.destroy()

        # Create new seat map
        self.seat_map = SeatMap(self.seat_container, lambda s: None)
        
        # Get reserved seats for this specific showtime/screen/movie
        reserved_seats = self.reservation_service.get_reserved_seats(
            self.selected_movie['title'], self.selected_showtime, self.selected_screen
        )
        
        # Set reserved seats in the seat map
        if reserved_seats:
            self.seat_map.set_reserved_seats(reserved_seats)
        
        # Force update to ensure colours are applied
        self.seat_map.update_seat_colours()

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
        return re.match(pattern, phone) is not None

    def make_reservation(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        date = self.date_entry.get().strip()

        if not all([name, email, phone, self.selected_showtime, self.seat_map]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        selected_seats = self.seat_map.get_selected_seats()
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        # Validate email and phone
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Please enter a valid phone number")
            return

        total_price = self.reservation_service.calculate_total_price(selected_seats)

        if messagebox.askyesno("Confirm", f"Total: ${total_price:.2f}. Proceed?"):
            success = self.reservation_service.make_reservation(
                name, email, phone, self.selected_movie['title'],
                self.selected_showtime, self.selected_screen, selected_seats, date
            )
            if success:
                messagebox.showinfo("Success", "Reservation complete!")
                self.show_landing_page()
            else:
                messagebox.showerror("Error", "Reservation failed")