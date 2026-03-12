import tkinter as tk
from tkinter import ttk
from typing import List, Callable
from ui.theme import Colors

class SeatMap:
    def __init__(self, parent, on_seat_selected: Callable[[str], None]):
        self.parent = parent
        self.on_seat_selected = on_seat_selected
        self.seat_buttons = {}
        self.selected_seats = []
        self.reserved_seats = []
        self.premium_seats = ['C4', 'C5', 'C6', 'C7', 'D4', 'D5', 'D6', 'D7', 'E4', 'E5', 'E6', 'E7']
        
        self.setup_ui()
        # update after widgets are created but as soon as possible
        self.parent.after_idle(self.update_seat_colours)
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(pady=10)
        
        # Screen indicator
        screen_frame = ttk.Frame(self.main_frame)
        screen_frame.pack(pady=(0, 20))
        
        screen_label = ttk.Label(screen_frame, text="SCREEN", font=("Arial", 14, "bold"))
        screen_label.pack()
        
        # Create a canvas for the screen
        screen_canvas = tk.Canvas(screen_frame, width=400, height=20, bg=Colors.CARD_BG, highlightthickness=0)
        screen_canvas.pack()
        screen_canvas.create_rectangle(50, 5, 350, 15, fill=Colors.MUTED)
        
        # Seat map frame
        seat_frame = ttk.Frame(self.main_frame)
        seat_frame.pack()
        
        # Create seats (8 rows x 8 columns with aisle)
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        for row_idx, row in enumerate(rows):
            row_frame = ttk.Frame(seat_frame)
            row_frame.pack(pady=2)
            
            # Row label
            row_label = ttk.Label(row_frame, text=row, font=("Arial", 10, "bold"), width=2, foreground=Colors.MUTED)
            row_label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Left block (seats 1-3)
            for col in range(1, 4):
                seat_id = f"{row}{col}"
                btn = tk.Button(
                    row_frame, 
                    text=seat_id, 
                    width=5, 
                    height=2,
                    font=("Arial", 7, "bold"),
                    bg=Colors.AVAILABLE,
                    fg=Colors.TEXT,
                    activebackground=Colors.ACCENT,
                    activeforeground=Colors.CTA_FG,
                    relief="raised", 
                    bd=2,
                    command=lambda s=seat_id: self.toggle_seat(s)
                )
                btn.pack(side=tk.LEFT, padx=2)
                self.seat_buttons[seat_id] = btn
            
            # Aisle gap
            aisle_label = ttk.Label(row_frame, text="", width=3)
            aisle_label.pack(side=tk.LEFT, padx=5)
            
            # Right block (seats 4-8)
            for col in range(4, 9):
                seat_id = f"{row}{col}"
                btn = tk.Button(
                    row_frame, 
                    text=seat_id, 
                    width=5, 
                    height=2,
                    font=("Arial", 7, "bold"),
                    bg=Colors.AVAILABLE,
                    fg=Colors.TEXT,
                    activebackground=Colors.ACCENT,
                    activeforeground=Colors.CTA_FG,
                    relief="raised", 
                    bd=2,
                    command=lambda s=seat_id: self.toggle_seat(s)
                )
                btn.pack(side=tk.LEFT, padx=2)
                self.seat_buttons[seat_id] = btn
        
        # Legend 
        legend_frame = ttk.Frame(self.main_frame)
        legend_frame.pack(pady=(20, 0))
        
        legends = [
            ("Available", Colors.AVAILABLE),
            ("Selected", Colors.SELECTED),
            ("Reserved", Colors.RESERVED),
            ("Premium", Colors.PREMIUM)
        ]
        
        for text, colour in legends:
            legend_item = ttk.Frame(legend_frame)
            legend_item.pack(side=tk.LEFT, padx=10)
            
            colour_box = tk.Label(legend_item, text="  ", bg=colour, width=3, height=1, relief="solid", bd=1)
            colour_box.pack(side=tk.LEFT)
            
            legend_label = ttk.Label(legend_item, text=text, font=("Arial", 9), foreground=Colors.MUTED)
            legend_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def toggle_seat(self, seat_id: str):
        """Toggle seat selection and update colors"""
        if seat_id in self.reserved_seats:
            return
        
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
        else:
            self.selected_seats.append(seat_id)
        
        # schedule immediate visual update and let tkinter redraw
        self.parent.after_idle(self.update_seat_colours)
        self.parent.update_idletasks()
        if self.on_seat_selected:
            try:
                self.on_seat_selected(seat_id)
            except Exception:
                pass
    
    def update_seat_colours(self):
        """Update all seat button colors based on current state"""
        for seat_id, button in self.seat_buttons.items():
            if seat_id in self.reserved_seats:
                button.config(bg=Colors.RESERVED, fg=Colors.CTA_FG, state="disabled", activebackground=Colors.RESERVED, activeforeground=Colors.CTA_FG, relief="raised")
            elif seat_id in self.selected_seats:
                button.config(bg=Colors.SELECTED, fg=Colors.TEXT, state="normal", activebackground=Colors.SELECTED, activeforeground=Colors.TEXT, relief="sunken")
            elif seat_id in self.premium_seats:
                button.config(bg=Colors.PREMIUM, fg=Colors.TEXT, state="normal", activebackground=Colors.PREMIUM, activeforeground=Colors.TEXT, relief="raised")
            else:
                button.config(bg=Colors.AVAILABLE, fg=Colors.TEXT, state="normal", activebackground=Colors.AVAILABLE, activeforeground=Colors.TEXT, relief="raised")
            # ensure widget is redrawn
            try:
                button.update_idletasks()
            except Exception:
                pass
    
    def set_reserved_seats(self, reserved_seats: List[str]):
        """Set which seats are reserved"""
        self.reserved_seats = [seat.strip() for seat in reserved_seats if seat.strip()]
        self.parent.after_idle(self.update_seat_colours)
    
    def get_selected_seats(self) -> List[str]:
        """Get list of currently selected seats"""
        return self.selected_seats.copy()
    
    def clear_selection(self):
        """Clear all selected seats"""
        self.selected_seats.clear()
        self.parent.after_idle(self.update_seat_colours)