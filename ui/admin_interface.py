import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.movie_service import MovieService
from services.reservation_service import ReservationService
import csv

class AdminInterface:
    def __init__(self, parent, auth_service, logout_callback=None):
        self.parent = parent
        self.auth_service = auth_service
        self.logout_callback = logout_callback
        self.movie_service = MovieService()
        self.reservation_service = ReservationService()
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and user info
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Admin Panel", font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        user_info = self.auth_service.get_current_user()
        user_label = ttk.Label(header_frame, text=f"Welcome, {user_info['username']}")
        user_label.pack(side=tk.RIGHT)

        # --- Add Logout Button ---
        if self.logout_callback:
            logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout_callback)
            logout_btn.pack(side=tk.RIGHT, padx=(0, 10))
        # --- End Logout Button ---

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Movie Management Tab
        self.movie_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.movie_frame, text="Movie Management")
        self.setup_movie_tab()
        
        # Reports Tab
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports")
        self.setup_reports_tab()
        
        # Reservations Tab
        self.reservations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reservations_frame, text="Reservations")
        self.setup_reservations_tab()
    
    def setup_movie_tab(self):
        # Movie list frame
        list_frame = ttk.LabelFrame(self.movie_frame, text="Movies", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Movie treeview
        columns = ('ID', 'Title', 'Genre', 'Duration', 'Showtimes', 'Screen')
        self.movie_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.movie_tree.heading(col, text=col)
            self.movie_tree.column(col, width=100)
        
        self.movie_tree.pack(fill=tk.BOTH, expand=True)
        
        # Movie form frame
        form_frame = ttk.LabelFrame(self.movie_frame, text="Add/Edit Movie", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.X)
        
        ttk.Label(fields_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.title_entry = ttk.Entry(fields_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(fields_frame, text="Genre:").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.genre_entry = ttk.Entry(fields_frame, width=15)
        self.genre_entry.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(fields_frame, text="Duration (min):").grid(row=0, column=4, sticky="w", padx=(0, 5))
        self.duration_entry = ttk.Entry(fields_frame, width=10)
        self.duration_entry.grid(row=0, column=5)
        
        ttk.Label(fields_frame, text="Showtimes:").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(10, 0))
        self.showtimes_entry = ttk.Entry(fields_frame, width=30)
        self.showtimes_entry.grid(row=1, column=1, columnspan=2, padx=(0, 10), pady=(10, 0))
        
        ttk.Label(fields_frame, text="Screen:").grid(row=1, column=3, sticky="w", padx=(0, 5), pady=(10, 0))
        self.screen_var = tk.StringVar()
        self.screen_combo = ttk.Combobox(fields_frame, textvariable=self.screen_var, values=[1, 2, 3, 4], width=8)
        self.screen_combo.grid(row=1, column=4, pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Movie", command=self.add_movie).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Update Movie", command=self.update_movie).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Movie", command=self.delete_movie).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Form", command=self.clear_movie_form).pack(side=tk.LEFT)
        
        # Bind tree selection
        self.movie_tree.bind('<<TreeviewSelect>>', self.on_movie_select)
    
    def setup_reports_tab(self):
        # Stats frame
        stats_frame = ttk.LabelFrame(self.reports_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=10, width=80)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.reports_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Refresh Stats", command=self.refresh_stats).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT)
    
    def setup_reservations_tab(self):
        # Reservations list
        list_frame = ttk.LabelFrame(self.reservations_frame, text="All Reservations", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Reservations treeview
        columns = ('ID', 'Customer', 'Movie', 'Showtime', 'Screen', 'Seats', 'Price', 'Date')
        self.reservations_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.reservations_tree.heading(col, text=col)
            self.reservations_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.reservations_tree.yview)
        self.reservations_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reservations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh and Remove All Bookings buttons
        button_frame = ttk.Frame(self.reservations_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Refresh", command=self.load_reservations).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Remove All Bookings", command=self.remove_all_bookings).pack(side=tk.LEFT)

    def remove_all_bookings(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm", "Are you sure you want to remove all bookings? This cannot be undone."):
            self.reservation_service.db.delete_all_reservations()
            self.load_reservations()
            messagebox.showinfo("Success", "All bookings have been removed.")

    def load_data(self):
        self.load_movies()
        self.load_reservations()
        self.refresh_stats()
    
    def load_movies(self):
        for item in self.movie_tree.get_children():
            self.movie_tree.delete(item)
        
        movies = self.movie_service.get_all_movies()
        for movie in movies:
            self.movie_tree.insert('', 'end', values=(
                movie['id'], movie['title'], movie['genre'], 
                movie['duration'], movie['showtimes'], movie['screen']
            ))
    
    def load_reservations(self):
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        reservations = self.reservation_service.get_all_reservations()
        for reservation in reservations:
            self.reservations_tree.insert('', 'end', values=(
                reservation['id'], reservation['customer_name'], 
                reservation['movie_title'], reservation['showtime'],
                reservation['screen'], reservation['seat_numbers'],
                f"${reservation['total_price']:.2f}", reservation['timestamp']
            ))
    
    def on_movie_select(self, event):
        selection = self.movie_tree.selection()
        if not selection:
            return
        
        item = self.movie_tree.item(selection[0])
        values = item['values']
        
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])
        
        self.genre_entry.delete(0, tk.END)
        self.genre_entry.insert(0, values[2])
        
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, values[3])
        
        self.showtimes_entry.delete(0, tk.END)
        self.showtimes_entry.insert(0, values[4])
        
        self.screen_var.set(values[5])
    
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        duration = self.duration_entry.get().strip()
        showtimes = self.showtimes_entry.get().strip()
        screen = self.screen_var.get()
        
        if not all([title, genre, duration, showtimes, screen]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            duration = int(duration)
            screen = int(screen)
            showtimes_list = [time.strip() for time in showtimes.split(',')]
            
            self.movie_service.add_movie(title, genre, duration, showtimes_list, screen)
            self.load_movies()
            self.clear_movie_form()
            messagebox.showinfo("Success", "Movie added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid duration and screen numbers")
    
    def update_movie(self):
        selection = self.movie_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a movie to update")
            return
        
        item = self.movie_tree.item(selection[0])
        movie_id = item['values'][0]
        
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        duration = self.duration_entry.get().strip()
        showtimes = self.showtimes_entry.get().strip()
        screen = self.screen_var.get()
        
        if not all([title, genre, duration, showtimes, screen]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            duration = int(duration)
            screen = int(screen)
            showtimes_list = [time.strip() for time in showtimes.split(',')]
            
            self.movie_service.update_movie(movie_id, title, genre, duration, showtimes_list, screen)
            self.load_movies()
            self.clear_movie_form()
            messagebox.showinfo("Success", "Movie updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid duration and screen numbers")
    
    def delete_movie(self):
        selection = self.movie_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a movie to delete")
            return
        
        item = self.movie_tree.item(selection[0])
        movie_id = item['values'][0]
        movie_title = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{movie_title}'?"):
            self.movie_service.delete_movie(movie_id)
            self.load_movies()
            self.clear_movie_form()
            messagebox.showinfo("Success", "Movie deleted successfully")
    
    def clear_movie_form(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.showtimes_entry.delete(0, tk.END)
        self.screen_var.set('')
    
    def refresh_stats(self):
        stats = self.reservation_service.get_reservation_stats()
        
        self.stats_text.delete(1.0, tk.END)
        
        report = "NUTWARK REPORT\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Total Reservations: {stats['total_reservations']}\n"
        report += f"Total Revenue: ${stats['total_revenue']:.2f}\n\n"
        
        report += "Screen Occupancy:\n"
        report += "-" * 20 + "\n"
        for screen, count in stats['screen_stats'].items():
            report += f"Screen {screen}: {count} reservations\n"
        
        report += "\nDetailed Reservations:\n"
        report += "-" * 30 + "\n"
        
        reservations = self.reservation_service.get_all_reservations()
        for reservation in reservations:
            report += f"ID: {reservation['id']} | "
            report += f"{reservation['customer_name']} | "
            report += f"{reservation['movie_title']} | "
            report += f"{reservation['showtime']} | "
            report += f"Screen {reservation['screen']} | "
            report += f"Seats: {reservation['seat_numbers']} | "
            report += f"${reservation['total_price']:.2f}\n"
        
        self.stats_text.insert(1.0, report)
    
    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                reservations = self.reservation_service.get_all_reservations()
                
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['id', 'customer_name', 'customer_email', 'customer_phone',
                                'movie_title', 'showtime', 'screen', 'seat_numbers', 
                                'total_price', 'timestamp']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for reservation in reservations:
                        writer.writerow(reservation)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")