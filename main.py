import tkinter as tk
from tkinter import ttk

# ensure pep 8 formatting
# comment code
window = tk.Tk()


class AlienAnnihilator:
    def __init__(self, master):
        self.master = master  # initialises master window
        self.game_start = False  # the game loop doesn't initially run
        # self.start_button = ttk.Button(self.master, text="START", command=self.start_game)
        self.canvas = tk.Canvas(master, width=800, height=600, bg="blue")
        self.canvas.place(x=50, y=50)
        self.start_button = tk.Button(self.master, text="START", width=15, height=2, command=self.start_game)
        self.leaderboard_button = tk.Button(self.master, text="LEADERBOARD", width=15, height=2, command=self
                                            .start_game)
        self.bindings_button = tk.Button(self.master, text="KEY BINDINGS", width=15, height=2, command=self.start_game)
        self.canvas.create_text(400, 150, text="ALIEN ANNIHILATOR", fill="black", font=("Arial Bold", 40))
        self.menu()

    def configure_window(self):
        self.master.geometry("800x600")
        self.master.title("Alien Annihilator")

    def menu(self, event=None):
        self.game_start = False
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.configure_window()
        self.canvas.create_window(400, 250, window=self.start_button)
        self.canvas.create_window(400, 300, window=self.leaderboard_button)
        self.canvas.create_window(400, 350, window=self.bindings_button)
        self.configure_window()

    def start_game(self):
        self.game_start = True
        self.start_button.pack_forget()
        self.configure_window()
        self.master.bind("<KeyPress-Escape>", self.menu)
        self.master.after(10, self.game_loop())

    def game_loop(self):
        if self.game_start:
            print("wow")
            self.master.after(10, self.game_loop)


game = AlienAnnihilator(window)
window.mainloop()  # tells Python to run the Tkinter event loop.
# This method listens for events, such as button clicks or keypresses,
# and blocks any code that comes after it from running until you close
# the window where you called the method.
