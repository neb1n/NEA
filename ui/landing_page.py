import tkinter as tk
from tkinter import ttk
from services.movie_service import MovieService
from ui.theme import Colors

class LandingPage:
    def __init__(self, parent, on_reserve_click, admin_login_callback=None):
        self.parent = parent
        self.movie_service = MovieService()
        self.on_reserve_click = on_reserve_click
        self.admin_login_callback = admin_login_callback
        
        self.setup_styles()
        self.setup_ui()
        self.load_featured_movies()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Landing.TFrame", background=Colors.BACKGROUND)
        style.configure("Landing.TLabel", font=("Segoe UI", 12), background=Colors.BACKGROUND, foreground=Colors.TEXT)
        style.configure("Hero.TLabel", font=("Segoe UI", 28, "bold"), background=Colors.HEADER_BG, foreground=Colors.ACCENT)
        style.configure("MovieCard.TFrame", background=Colors.CARD_BG, relief="raised", borderwidth=1)
        style.configure("MovieTitle.TLabel", font=("Segoe UI", 12, "bold"), background=Colors.CARD_BG, foreground=Colors.TEXT)
        style.configure("MovieInfo.TLabel", font=("Segoe UI", 10), background=Colors.CARD_BG, foreground=Colors.MUTED)
        style.configure("ReserveBtn.TButton", font=("Segoe UI", 11, "bold"), foreground=Colors.CTA_FG, background=Colors.ACCENT)
    
    def setup_ui(self):
        # Main frame with soft background
        self.main_frame = ttk.Frame(self.parent, style="Landing.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header bar container
        header_frame = ttk.Frame(self.main_frame, style="Landing.TFrame")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        header_bg = tk.Frame(header_frame, bg=Colors.HEADER_BG, height=100)
        header_bg.pack(fill=tk.X, padx=0)
        header_bg.pack_propagate(False)

        # Centered title using place; admin button stays at the right
        title_label = tk.Label(header_bg, text="🎬 NUTWARK Cinema", font=("Segoe UI", 28, "bold"),
                               bg=Colors.HEADER_BG, fg=Colors.ACCENT)
        # center the label in the header band
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Admin button: styled tk.Button with hover effect (more sophisticated)
        if self.admin_login_callback:
            admin_btn = tk.Button(
                header_bg,
                text="🔒 Admin",
                font=("Segoe UI", 10, "bold"),
                bg=Colors.CARD_BG,
                fg=Colors.TEXT,
                activebackground=Colors.ACCENT_HOVER,
                activeforeground=Colors.CTA_FG,
                relief="groove",
                bd=1,
                cursor="hand2",
                command=self.admin_login_callback
            )
            # place on the right side
            admin_btn.pack(side=tk.RIGHT, padx=24, pady=20)

            # subtle hover effect
            def on_enter(e):
                try:
                    admin_btn.config(bg=Colors.ACCENT_HOVER, fg=Colors.CTA_FG)
                except Exception:
                    pass
            def on_leave(e):
                try:
                    admin_btn.config(bg=Colors.CARD_BG, fg=Colors.TEXT)
                except Exception:
                    pass
            admin_btn.bind("<Enter>", on_enter)
            admin_btn.bind("<Leave>", on_leave)
        
        # Tagline (soft muted)
        tagline = tk.Label(self.main_frame, text="NOW SHOWING - Book Your Experience Today", 
                          font=("Segoe UI", 14), bg=Colors.BACKGROUND, fg=Colors.MUTED)
        tagline.pack(pady=(20, 10))
        
        # Scrollable movies container
        canvas_frame = ttk.Frame(self.main_frame, style="Landing.TFrame")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(canvas_frame, bg=Colors.BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Landing.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.movies_container = scrollable_frame
    
    def load_featured_movies(self):
        movies = self.movie_service.get_all_movies()
        
        if not movies:
            no_movies_label = tk.Label(self.movies_container, text="No movies available", 
                                       font=("Segoe UI", 14), bg=Colors.BACKGROUND, fg=Colors.MUTED)
            no_movies_label.pack(pady=40)
            return
        
        # Create grid of movie cards (3 columns)
        for idx, movie in enumerate(movies):
            row = idx // 3
            col = idx % 3
            self.create_movie_card(self.movies_container, movie, row, col)
    
    def create_movie_card(self, parent, movie, row, col):
        # Movie card frame
        card_frame = tk.Frame(parent, bg=Colors.CARD_BG, relief="raised", borderwidth=1, height=300, width=250)
        card_frame.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        card_frame.pack_propagate(False)
        
        # Movie poster placeholder
        poster_frame = tk.Frame(card_frame, bg=Colors.HEADER_BG, height=180)
        poster_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        poster_frame.pack_propagate(False)
        
        # Use emoji or text as placeholder
        poster_label = tk.Label(poster_frame, text="🎭", font=("Segoe UI", 60), 
                               bg=Colors.HEADER_BG, fg=Colors.ACCENT)
        poster_label.pack(expand=True)
        
        # Movie title
        title_label = tk.Label(card_frame, text=movie['title'], font=("Segoe UI", 11, "bold"),
                              bg=Colors.CARD_BG, fg=Colors.TEXT, wraplength=230, justify="center")
        title_label.pack(padx=10, pady=(10, 5))
        
        # Genre & Duration
        info_text = f"{movie['genre']} • {movie['duration']} min"
        info_label = tk.Label(card_frame, text=info_text, font=("Segoe UI", 9),
                             bg=Colors.CARD_BG, fg=Colors.MUTED)
        info_label.pack(padx=10, pady=2)
        
        # Screen info
        screen_label = tk.Label(card_frame, text=f"Screen {movie['screen']}", font=("Segoe UI", 9),
                               bg=Colors.CARD_BG, fg=Colors.ACCENT)
        screen_label.pack(padx=10, pady=(2, 8))
        
        # Make the whole card act as a clickable button (card = button)
        # set a pointer cursor for affordance
        try:
            card_frame.config(cursor="hand2")
        except Exception:
            pass

        # Hover effect: show a subtle highlight around the card
        def _on_enter(e):
            try:
                card_frame.config(highlightbackground=Colors.ACCENT_HOVER, highlightthickness=2)
            except Exception:
                pass

        def _on_leave(e):
            try:
                card_frame.config(highlightthickness=0)
            except Exception:
                pass

        def _on_click(e, m=movie):
            try:
                self.on_reserve_click(m)
            except Exception:
                pass

        # Bind the frame and its main children so clicks anywhere register
        widgets_to_bind = [card_frame, poster_frame, poster_label, title_label, info_label, screen_label]
        for w in widgets_to_bind:
            try:
                w.bind("<Enter>", _on_enter)
                w.bind("<Leave>", _on_leave)
                w.bind("<Button-1>", _on_click)
                w.config(cursor="hand2")
            except Exception:
                pass