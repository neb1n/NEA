import tkinter as tk
from tkinter import ttk
from ui.theme import Colors


class SplashScreen:
    def __init__(self, parent, words=None, duration=3000, on_close=None):
        self.parent = parent
        self.words = words or [
            "Waiting for Database...",
            "Loading Admin Panel...",
            "Loading Database...",
        ]
        self.duration = duration
        self.on_close = on_close
        self.index = 0
        self._after_id = None

        self.top = tk.Toplevel(parent)
        self.top.overrideredirect(True)
        self.top.transient(parent)

        # Position and size to cover parent window
        parent.update_idletasks()
        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        w = parent.winfo_width()
        h = parent.winfo_height()
        if w <= 1 or h <= 1:
            # fallback if parent not yet sized
            w = parent.winfo_screenwidth()
            h = parent.winfo_screenheight()
            x = 0
            y = 0

        self.top.geometry(f"{w}x{h}+{x}+{y}")
        try:
            # slight transparency if supported
            self.top.attributes("-alpha", 0.98)
        except Exception:
            pass

        # Background
        self.top.configure(bg=Colors.BACKGROUND)

        # Center frame
        frame = ttk.Frame(self.top, padding=20, style="Splash.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Splash.TFrame", background=Colors.BACKGROUND)
        style.configure("Splash.Title.TLabel", font=("Arial", 20, "bold"), foreground=Colors.ACCENT, background=Colors.BACKGROUND)
        style.configure("Splash.Word.TLabel", font=("Courier", 16), foreground=Colors.TEXT, background=Colors.BACKGROUND)

        title = ttk.Label(frame, text="Loading Admin Panel", style="Splash.Title.TLabel")
        title.pack(pady=(0, 10))

        self.word_label = ttk.Label(frame, text=self.words[0], style="Splash.Word.TLabel")
        self.word_label.pack()

        # Start cycling words
        self.interval = 1300
        self._start_time = self.top.after(0, self._tick)
        # schedule finish
        self.top.after(self.duration, self.finish)

    def _tick(self):
        self.word_label.config(text=self.words[self.index % len(self.words)])
        self.index += 1
        self._after_id = self.top.after(self.interval, self._tick)

    def finish(self):
        if self._after_id:
            try:
                self.top.after_cancel(self._after_id)
            except Exception:
                pass
        try:
            self.top.destroy()
        except Exception:
            pass
        if callable(self.on_close):
            self.on_close()
