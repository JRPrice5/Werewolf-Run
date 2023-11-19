import tkinter as tk
from tkinter import ttk

# ensure pep 8 formatting
# comment code
# 1920x1080 resolution
window = tk.Tk()

global BUTTON_WIDTH
BUTTON_WIDTH = 15
global BUTTON_HEIGHT
BUTTON_HEIGHT = 2


class AlienAnnihilator:
    def __init__(self, master):
        self.BUTTON_WIDTH = 15
        self.BUTTON_HEIGHT = 2
        self.master = master  # initialises master window
        self.game_start = False  # the game loop doesn't initially run
        # self.start_button = ttk.Button(self.master, text="START", command=self.start_game)
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.place(x=50, y=50)
        self.start_button = tk.Button(self.master, text="START", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                      command=self.start_game)
        self.leaderboard_button = tk.Button(self.master, text="LEADERBOARD", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                            command=None)
        self.bindings_button = tk.Button(self.master, text="KEY BINDINGS", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                         command=None)
        self.quit_button = tk.Button(self.master, text="QUIT", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     command=self.master.destroy)
        self.menu_button = tk.Button(self.master, text="MENU", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     command=self.menu)
        self.resume_button = tk.Button(self.master, text="RESUME", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                       command=self.resume)
        self.menu()

    def configure_window(self):
        self.master.geometry("1920x1080")
        self.master.attributes("-fullscreen", True)
        self.master.title("Alien Annihilator")

    def menu(self, event=None):
        self.canvas.delete("all")
        self.canvas.config(bg="blue")
        self.game_start = False
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.configure_window()
        self.canvas.create_text(960, 250, text="ALIEN ANNIHILATOR", fill="white", font=("Arial Bold", 80))
        self.canvas.create_window(960, 450, window=self.start_button)
        self.canvas.create_window(960, 500, window=self.leaderboard_button)
        self.canvas.create_window(960, 550, window=self.bindings_button)
        self.canvas.create_window(960, 600, window=self.quit_button)
        self.configure_window()

    def pause(self, event=None):
        self.canvas.delete("all")
        self.canvas.create_text(960, 350, text="PAUSE MENU", fill="white", font=("Arial Bold", 40))
        self.canvas.create_window(960, 450, window=self.resume_button)
        self.canvas.create_window(960, 500, window=self.menu_button)
        self.canvas.create_window(960, 550, window=self.quit_button)

    def resume(self, event=None):
        self.canvas.delete("all")

    def start_game(self):
        self.game_start = True
        self.canvas.delete("all")
        self.canvas.config(bg="black")
        # self.start_button.pack_forget()
        self.configure_window()
        self.master.geometry("1920x1080")
        self.master.bind("<KeyPress-Escape>", self.pause)
        self.master.after(10, self.game_loop())

    def game_loop(self):
        pass


game = AlienAnnihilator(window)
window.mainloop()  # tells Python to run the Tkinter event loop.
# This method listens for events, such as button clicks or keypresses,
# and blocks any code that comes after it from running until you close
# the window where you called the method.
