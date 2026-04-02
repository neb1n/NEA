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
        #!Update after the widgets are created
        self.parent.after_idle(self.update_seat_colours)
    
    def setup_ui(self):
        #!Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(pady=10)
        
        #!Screen indicator
        screen_frame = ttk.Frame(self.main_frame)
        screen_frame.pack(pady=(0, 20))
        
        screen_label = ttk.Label(screen_frame, text="SCREEN", font=("Arial", 14, "bold"))
        screen_label.pack()
        
        #!Creates a canvas for the screen
        screen_canvas = tk.Canvas(screen_frame, width=400, height=20, bg=Colors.CARD_BG, highlightthickness=0)
        screen_canvas.pack()
        screen_canvas.create_rectangle(50, 5, 350, 15, fill=Colors.MUTED)
        
        #!Seat map frame
        seat_frame = ttk.Frame(self.main_frame)
        seat_frame.pack()
        
        #!Create seats 8x8
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        for row_idx, row in enumerate(rows):
            row_frame = ttk.Frame(seat_frame)
            row_frame.pack(pady=2)
            
            #!Row label
            row_label = ttk.Label(row_frame, text=row, font=("Arial", 10, "bold"), width=2, foreground=Colors.MUTED)
            row_label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Left side
            for col in range(1, 4):
                seat_id = f"{row}{col}"
                btn = tk.Label(
                    row_frame,
                    text=seat_id,
                    width=5,
                    height=2,
                    font=("Arial", 7, "bold"),
                    bg=Colors.AVAILABLE,
                    fg=Colors.TEXT,
                    relief="raised",
                    bd=2,
                    cursor="hand2",
                )
                #!Using lambda functions to bind buttons
                btn.bind("<Button-1>", lambda e, s=seat_id: self.toggle_seat(s))
                btn.bind("<Enter>", lambda e: e.widget.config(highlightthickness=2, highlightbackground=Colors.ACCENT_HOVER))
                btn.bind("<Leave>", lambda e: e.widget.config(highlightthickness=0))
                btn.pack(side=tk.LEFT, padx=2)
                self.seat_buttons[seat_id] = btn
            
            #!Aisle gap
            aisle_label = ttk.Label(row_frame, text="", width=3)
            aisle_label.pack(side=tk.LEFT, padx=5)
            
            #!Right block
            for col in range(4, 9):
                seat_id = f"{row}{col}"
                btn = tk.Label(
                    row_frame,
                    text=seat_id,
                    width=5,
                    height=2,
                    font=("Arial", 7, "bold"),
                    bg=Colors.AVAILABLE,
                    fg=Colors.TEXT,
                    relief="raised",
                    bd=2,
                    cursor="hand2",
                )
                btn.bind("<Button-1>", lambda e, s=seat_id: self.toggle_seat(s))
                btn.bind("<Enter>", lambda e: e.widget.config(highlightthickness=2, highlightbackground=Colors.ACCENT_HOVER))
                btn.bind("<Leave>", lambda e: e.widget.config(highlightthickness=0))
                btn.pack(side=tk.LEFT, padx=2)
                self.seat_buttons[seat_id] = btn
        
        #!Colour Legend 
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
        #!Toggling seat function
        if seat_id in self.reserved_seats:
            return
        
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
        else:
            self.selected_seats.append(seat_id)
        
        #!Visual updating and tkinter drawing
        self.parent.after_idle(self.update_seat_colours)
        self.parent.update_idletasks()
        if self.on_seat_selected:
            try:
                self.on_seat_selected(seat_id)
            except Exception:
                pass
    
    def update_seat_colours(self):
        #!Seat colour changed based on state
        for seat_id, button in self.seat_buttons.items():
            #!Reserved seats
            if seat_id in self.reserved_seats:
                button.config(bg=Colors.RESERVED, fg=Colors.CTA_FG, relief="raised")
                try:
                    button.unbind("<Button-1>")
                    button.config(cursor="")
                except Exception:
                    pass
            #!Selected Seats
            elif seat_id in self.selected_seats:
                button.config(bg=Colors.SELECTED, fg=Colors.TEXT, relief="sunken")
                try:
                    button.unbind("<Button-1>")
                    button.bind("<Button-1>", lambda e, s=seat_id: self.toggle_seat(s))
                    button.config(cursor="hand2")
                except Exception:
                    pass
            #!Premium seats
            elif seat_id in self.premium_seats:
                button.config(bg=Colors.PREMIUM, fg=Colors.TEXT, relief="raised")
                try:
                    button.unbind("<Button-1>")
                    button.bind("<Button-1>", lambda e, s=seat_id: self.toggle_seat(s))
                    button.config(cursor="hand2")
                except Exception:
                    pass
            #!Available seats
            else:
                button.config(bg=Colors.AVAILABLE, fg=Colors.TEXT, relief="raised")
                try:
                    button.unbind("<Button-1>")
                    button.bind("<Button-1>", lambda e, s=seat_id: self.toggle_seat(s))
                    button.config(cursor="hand2")
                except Exception:
                    pass
            #!Redraw the widget
            try:
                button.update_idletasks()
            except Exception:
                #!Exception handling
                pass
    
    def set_reserved_seats(self, reserved_seats: List[str]):
        #!Seat reservations
        self.reserved_seats = [seat.strip() for seat in reserved_seats if seat.strip()]
        self.parent.after_idle(self.update_seat_colours)
    
    def get_selected_seats(self) -> List[str]:
        #!Selected seats
        return self.selected_seats.copy()
    
    def clear_selection(self):
        #!Clear the selected seats
        self.selected_seats.clear()
        self.parent.after_idle(self.update_seat_colours)
