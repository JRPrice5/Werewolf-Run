import tkinter as tk
from tkinter import ttk

# ensure pep 8 formatting
# comment code
window = tk.Tk()


class AlienAnnihilator:
    def __init__(self, master):
        self.master = master  # initialises master window
        self.game_start = False  # the game loop doesn't initially run
        self.start_button = ttk.Button(self.master, text="START", command=self.start_game)
        self.canvas = tk.Canvas(master, width=800, height=600, bg="black")
        self.menu()

    def configure_window(self, colour):
        self.master.geometry("800x600")
        self.master.configure(background=colour)
        self.master.title("Alien Annihilator")

    def menu(self, event=None):
        self.game_start = False
        self.start_button.pack()
        self.configure_window("#b3ffff")

    def start_game(self):
        self.game_start = True
        self.start_button.pack_forget()
        self.configure_window("#000000")
        self.master.bind("<KeyPress-Escape>", self.menu)
        self.master.after(10, self.game_loop())

    def game_loop(self):
        if self.game_start:
            print("wow")
            self.master.after(10, self.game_loop)


game = AlienAnnihilator(window)
window.mainloop()
