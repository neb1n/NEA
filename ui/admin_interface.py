import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.movie_service import MovieService
from services.reservation_service import ReservationService
import csv
from ui.theme import Colors

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
        style = ttk.Style()
        style.configure("Admin.TFrame", background=Colors.BACKGROUND)
        # Main frame
        self.main_frame = ttk.Frame(self.parent, style="Admin.TFrame")
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
        # Layout: left = movies & showtimes, right = report text
        container = ttk.Frame(self.reports_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.LabelFrame(container, text="Movies / Viewings", padding="6")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        right_frame = ttk.LabelFrame(container, text="Report", padding="6")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Movie treeview on left
        columns = ('ID', 'Title', 'Screen')
        self.movie_tree_reports = ttk.Treeview(left_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.movie_tree_reports.heading(col, text=col)
            self.movie_tree_reports.column(col, width=120)
        self.movie_tree_reports.pack(fill=tk.Y, expand=True)
        self.movie_tree_reports.bind('<<TreeviewSelect>>', self.on_reports_movie_select)

        # Showtimes selector and buttons
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, pady=(8, 0))

        ttk.Label(controls_frame, text="Showtime:").grid(row=0, column=0, sticky='w')
        self.showtime_var = tk.StringVar()
        self.showtime_combo = ttk.Combobox(controls_frame, textvariable=self.showtime_var, values=[], width=20)
        self.showtime_combo.grid(row=0, column=1, padx=(6, 0))

        ttk.Button(controls_frame, text="View Movie Report", command=self.view_movie_report).grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky='ew')
        ttk.Button(controls_frame, text="View Viewing Report", command=self.view_viewing_report).grid(row=2, column=0, columnspan=2, pady=(6, 0), sticky='ew')

        # Right: text area for report details
        self.stats_text = tk.Text(right_frame, height=20)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Footer buttons
        footer_frame = ttk.Frame(self.reports_frame)
        footer_frame.pack(pady=10)

        ttk.Button(footer_frame, text="Refresh Stats", command=self.refresh_stats).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(footer_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT)
    
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
        ttk.Button(button_frame, text="Process Refund", command=self.process_refund).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Remove All Bookings", command=self.remove_all_bookings).pack(side=tk.LEFT)

    def remove_all_bookings(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm", "Are you sure you want to remove all bookings? This cannot be undone."):
            self.reservation_service.db.delete_all_reservations()
            self.load_reservations()
            messagebox.showinfo("Success", "All bookings have been removed.")

    def process_refund(self):
        selection = self.reservations_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a reservation to refund.")
            return

        item = self.reservations_tree.item(selection[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror("Error", "Could not determine selected reservation.")
            return

        try:
            reservation_id = int(values[0])
        except Exception:
            messagebox.showerror("Error", "Invalid reservation ID selected.")
            return

        confirm = messagebox.askyesno("Confirm Refund", f"Are you sure you want to process a refund and delete reservation ID {reservation_id}? This cannot be undone.")
        if not confirm:
            return

        success = self.reservation_service.delete_reservation(reservation_id)
        if success:
            messagebox.showinfo("Success", "Reservation refunded and deleted.")
            self.load_reservations()
            self.refresh_stats()
        else:
            messagebox.showerror("Error", "Failed to delete reservation. It may have already been removed.")

    def load_data(self):
        self.load_movies()
        self.load_reservations()
        self.refresh_stats()
        # Also populate the reports movies list
        try:
            self.load_reports_movies()
        except Exception:
            pass
    
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

        if not title:
            messagebox.showerror("Error", "Title is required.")
            return

        try:
            duration_val = int(duration)
        except Exception:
            messagebox.showerror("Error", "Duration must be an integer (minutes).")
            return

        try:
            screen_val = int(screen)
        except Exception:
            messagebox.showerror("Error", "Please select a valid screen.")
            return

        showtimes_list = [s.strip() for s in showtimes.split(',')] if showtimes else []

        try:
            self.movie_service.add_movie(title, genre, duration_val, showtimes_list, screen_val)
            messagebox.showinfo("Success", f"Movie '{title}' added.")
            self.clear_movie_form()
            self.load_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add movie: {e}")

    def update_movie(self):
        selection = self.movie_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a movie to update.")
            return

        item = self.movie_tree.item(selection[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror("Error", "Could not determine selected movie.")
            return

        try:
            movie_id = int(values[0])
        except Exception:
            messagebox.showerror("Error", "Invalid movie ID selected.")
            return

        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        try:
            duration_val = int(self.duration_entry.get().strip())
        except Exception:
            messagebox.showerror("Error", "Duration must be an integer (minutes).")
            return

        showtimes = self.showtimes_entry.get().strip()
        showtimes_list = [s.strip() for s in showtimes.split(',')] if showtimes else []

        try:
            screen_val = int(self.screen_var.get())
        except Exception:
            messagebox.showerror("Error", "Please select a valid screen.")
            return

        try:
            self.movie_service.update_movie(movie_id, title, genre, duration_val, showtimes_list, screen_val)
            messagebox.showinfo("Success", f"Movie '{title}' updated.")
            self.clear_movie_form()
            self.load_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update movie: {e}")

    def delete_movie(self):
        selection = self.movie_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a movie to delete.")
            return

        item = self.movie_tree.item(selection[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror("Error", "Could not determine selected movie.")
            return

        try:
            movie_id = int(values[0])
            movie_title = values[1]
        except Exception:
            messagebox.showerror("Error", "Invalid movie selection.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{movie_title}'? This will also remove related reservations.")
        if not confirm:
            return

        try:
            self.movie_service.delete_movie(movie_id)
            messagebox.showinfo("Success", f"Movie '{movie_title}' deleted.")
            self.clear_movie_form()
            self.load_movies()
            self.load_reservations()
            self.refresh_stats()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete movie: {e}")

    def clear_movie_form(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.showtimes_entry.delete(0, tk.END)
        self.screen_var.set('')

    def refresh_stats(self):
        try:
            stats = self.reservation_service.get_reservation_stats()
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert(tk.END, f"Total Reservations: {stats['total_reservations']}\n")
            self.stats_text.insert(tk.END, f"Total Revenue: ${stats['total_revenue']:.2f}\n\n")
            self.stats_text.insert(tk.END, "Screen Occupancy:\n")
            for screen, count in stats['screen_stats'].items():
                self.stats_text.insert(tk.END, f"  Screen {screen}: {count} bookings\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh stats: {e}")

    def export_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
            if not file_path:
                return

            movies = self.movie_service.get_all_movies()
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Title', 'Genre', 'Duration', 'Showtimes', 'Screen'])
                for m in movies:
                    writer.writerow([m.get('id'), m.get('title'), m.get('genre'), m.get('duration'), m.get('showtimes'), m.get('screen')])

            messagebox.showinfo('Exported', f'Movie list exported to {file_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export CSV: {e}')
   
    # --- Reports helpers ---
    def load_reports_movies(self):
        # populate the left movie tree in reports tab
        for item in getattr(self, 'movie_tree_reports').get_children():
            self.movie_tree_reports.delete(item)

        movies = self.movie_service.get_all_movies()
        for movie in movies:
            self.movie_tree_reports.insert('', 'end', values=(movie.get('id'), movie.get('title'), movie.get('screen')))

    def on_reports_movie_select(self, event):
        selection = self.movie_tree_reports.selection()
        if not selection:
            return

        item = self.movie_tree_reports.item(selection[0])
        values = item.get('values', [])
        if not values:
            return

        movie_title = values[1]
        # populate showtimes combo
        showtimes = self.movie_service.get_showtimes_for_movie(movie_title)
        self.showtime_combo['values'] = showtimes
        if showtimes:
            self.showtime_var.set(showtimes[0])
        else:
            self.showtime_var.set('')

    def view_movie_report(self):
        selection = self.movie_tree_reports.selection()
        if not selection:
            messagebox.showerror('Error', 'Please select a movie to view report.')
            return

        item = self.movie_tree_reports.item(selection[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror('Error', 'Could not determine selected movie.')
            return

        movie_title = values[1]
        try:
            report = self.reservation_service.get_movie_report(movie_title)
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert(tk.END, f"Report for '{movie_title}'\n")
            self.stats_text.insert(tk.END, f"Total Reservations: {report['total_reservations']}\n")
            self.stats_text.insert(tk.END, f"Total Revenue: ${report['total_revenue']:.2f}\n\n")
            self.stats_text.insert(tk.END, "Showtime Breakdown:\n")
            if report['showtime_stats']:
                for st, sdata in report['showtime_stats'].items():
                    self.stats_text.insert(tk.END, f"  {st}: {sdata['count']} bookings, ${sdata['revenue']:.2f}\n")
            else:
                self.stats_text.insert(tk.END, "  No bookings for this movie.\n")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to get movie report: {e}')

    def view_viewing_report(self):
        selection = self.movie_tree_reports.selection()
        if not selection:
            messagebox.showerror('Error', 'Please select a movie and showtime to view viewing report.')
            return

        item = self.movie_tree_reports.item(selection[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror('Error', 'Could not determine selected movie.')
            return

        movie_title = values[1]
        screen = values[2]
        showtime = self.showtime_var.get()
        if not showtime:
            messagebox.showerror('Error', 'Please select a showtime.')
            return

        try:
            report = self.reservation_service.get_viewing_report(movie_title, showtime, int(screen))
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert(tk.END, f"Viewing Report for '{movie_title}' — {showtime} (Screen {screen})\n")
            self.stats_text.insert(tk.END, f"Total Reservations: {report['total_reservations']}\n")
            self.stats_text.insert(tk.END, f"Total Revenue: ${report['total_revenue']:.2f}\n\n")
            self.stats_text.insert(tk.END, "Seats Booked:\n")
            if report['seats']:
                self.stats_text.insert(tk.END, ', '.join(report['seats']) + '\n')
            else:
                self.stats_text.insert(tk.END, '  No seats booked for this viewing.\n')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to get viewing report: {e}')
   