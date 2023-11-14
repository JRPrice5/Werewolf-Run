import tkinter as tk
from tkinter import ttk

# ensure pep 8 formatting
# comment code
window = tk.Tk()


class AlienAnnihilator:
    def __init__(self, master):
        self.master = master  # initialises master window
        self.game_start = False  # the game loop doesn't initially run
        self.configure_window()
        self.canvas = tk.Canvas(master, width=800, height=600, bg="black")
        self.menu()

    def configure_window(self):
        self.master.geometry("800x600")
        self.master.configure(background='#b3ffff')
        self.master.title("Alien Annihilator")

    def menu(self):
        start_button = ttk.Button(window, text="START", command=self.start_game())
        start_button.pack()

    def start_game(self):
        self.canvas.delete("all")
        self.game_start = True

    def game_loop(self):
        pass


game = AlienAnnihilator(window)
window.mainloop()
