import tkinter as tk
from tkinter import ttk
from typing import List, Callable

class SeatMap:
    def __init__(self, parent, on_seat_selected: Callable[[str], None]):
        self.parent = parent
        self.on_seat_selected = on_seat_selected
        self.seat_buttons = {}
        #!Preparing
        self.selected_seats = []
        self.reserved_seats = []
        #!Setting the premium seats automatically
        self.premium_seats = ['C4', 'C5', 'C6', 'C7', 'D4', 'D5', 'D6', 'D7', 'E4', 'E5', 'E6', 'E7']
        
        self.setup_ui()
    
    def setup_ui(self):
        #!Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(pady=10)
        
        #!Screen indicator
        screen_frame = ttk.Frame(self.main_frame)
        screen_frame.pack(pady=(0, 20))
        
        screen_label = ttk.Label(screen_frame, text="SCREEN", font=("Arial", 14, "bold"))
        screen_label.pack()
        
        #!Create a canvas for the screen
        screen_canvas = tk.Canvas(screen_frame, width=400, height=20, bg="lightgray")
        screen_canvas.pack()
        screen_canvas.create_rectangle(50, 5, 350, 15, fill="black")
        
        #!Seat map frame
        seat_frame = ttk.Frame(self.main_frame)
        seat_frame.pack()
        
        #!Create seats (8 rows x 5 columns with aisle)
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        for row_idx, row in enumerate(rows):
            row_frame = ttk.Frame(seat_frame)
            row_frame.pack(pady=1)  # Reduced vertical padding
            
            #!Row label
            row_label = ttk.Label(row_frame, text=row, font=("Arial", 9, "bold"))  # Slightly smaller font
            row_label.pack(side=tk.LEFT, padx=(0, 2))  # Less horizontal padding
            
            #!Left block (seats 1-3)
            for col in range(1, 4):
                seat_id = f"{row}{col}"
                btn = tk.Button(row_frame, text=seat_id, width=2, height=1,  # Smaller button
                              command=lambda s=seat_id: self.toggle_seat(s))
                btn.pack(side=tk.LEFT, padx=0)  # No extra padding
                self.seat_buttons[seat_id] = btn
            
            #!Aisle gap
            aisle_label = ttk.Label(row_frame, text="  ", width=1)  # Smaller gap
            aisle_label.pack(side=tk.LEFT)
            
            #!Right block (seats 4-8)
            for col in range(4, 9):
                seat_id = f"{row}{col}"
                btn = tk.Button(row_frame, text=seat_id, width=2, height=1,  #!Smaller button
                              command=lambda s=seat_id: self.toggle_seat(s))
                btn.pack(side=tk.LEFT, padx=0)  #!Removed padding because it didn't fit :(
                self.seat_buttons[seat_id] = btn
        
        #!Legend 
        legend_frame = ttk.Frame(self.main_frame)
        legend_frame.pack(pady=(20, 0))
        
        legends = [
            ("Available", "lightgreen"),
            ("Selected", "yellow"),
            ("Reserved", "red"),
            ("Premium", "gold")
        ]
        
        #!Assigning colours to the legend
        for text, colour in legends:
            legend_item = ttk.Frame(legend_frame)
            legend_item.pack(side=tk.LEFT, padx=10)
            
            colour_box = tk.Label(legend_item, text="  ", bg=colour, width=3, height=1)
            colour_box.pack(side=tk.LEFT)
            
            legend_label = ttk.Label(legend_item, text=text)
            legend_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.update_seat_colours()
    
    #!Toggling seat selection
    def toggle_seat(self, seat_id: str):
        if seat_id in self.reserved_seats:
            return  #!Can't select reserved seats
        
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
        else:
            self.selected_seats.append(seat_id)
        
        self.update_seat_colours()
        self.on_seat_selected(seat_id)
    #!Updating seat colours
    def update_seat_colours(self):
        for seat_id, button in self.seat_buttons.items():
            if seat_id in self.reserved_seats:
                button.config(bg="red", state="disabled")
            elif seat_id in self.selected_seats:
                button.config(bg="yellow", state="normal")
            elif seat_id in self.premium_seats:
                button.config(bg="gold", state="normal")
            else:
                button.config(bg="lightgreen", state="normal")
    
    #!Setting seat colours
    def set_reserved_seats(self, reserved_seats: List[str]):
        self.reserved_seats = reserved_seats
        self.update_seat_colours()
    
    
    def get_selected_seats(self) -> List[str]:
        return self.selected_seats.copy()
    
    #!Clearing the selection
    def clear_selection(self):
        self.selected_seats.clear()
        self.update_seat_colours()