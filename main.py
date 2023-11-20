import tkinter as tk
from tkinter import ttk

# ensure pep 8 formatting
# comment code
# 1920x1080 resolution
window = tk.Tk()


class AlienAnnihilator:
    def __init__(self, master):
        self.BUTTON_WIDTH = 15
        self.BUTTON_HEIGHT = 2

        self.score = 0
        self.scroll_speed = 1

        self.obstacles = []

        self.pause_label_id = None
        self.resume_button_id = None
        self.menu_button_id = None
        self.quit_button_id = None

        self.player = None

        self.is_paused = False

        self.master = master  # initialises master window
        self.game_start = False  # the game loop doesn't initially run

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.place(x=50, y=50)

        self.start_button = tk.Button(self.master, text="START", width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT,
                                      command=self.start_game)
        self.leaderboard_button = tk.Button(self.master, text="LEADERBOARD", width=self.BUTTON_WIDTH,
                                            height=self.BUTTON_HEIGHT, command=None)
        self.bindings_button = tk.Button(self.master, text="KEY BINDINGS", width=self.BUTTON_WIDTH,
                                         height=self.BUTTON_HEIGHT, command=None)
        self.quit_button = tk.Button(self.master, text="QUIT", width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT,
                                     command=self.master.destroy)
        self.menu_button = tk.Button(self.master, text="MENU", width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT,
                                     command=self.menu)
        self.resume_button = tk.Button(self.master, text="RESUME", width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT,
                                       command=self.resume)
        self.score_label = tk.Label(self.master, text="Score: 0", fg="white", bg="black", font=("Arial Bold", 32))
        self.menu()

    def configure_window(self):
        self.master.geometry("1920x1080")
        self.master.attributes("-fullscreen", True)
        self.master.title("Alien Annihilator")

    def menu(self, event=None):
        self.is_paused = False
        self.master.bind("<KeyPress-Escape>", None)
        if self.player is not None:
            self.canvas.delete(self.player.get_id())
            self.player = None
            self.score_label.destroy()
            self.score = 0
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
        if self.is_paused:
            self.resume()
        else:
            self.is_paused = True
            self.player.pause()
            self.pause_label_id = self.canvas.create_text(960, 350, text="PAUSE MENU", fill="white",
                                                          font=("Arial Bold", 40))
            self.resume_button_id = self.canvas.create_window(960, 450, window=self.resume_button)
            self.menu_button_id = self.canvas.create_window(960, 500, window=self.menu_button)
            self.quit_button_id = self.canvas.create_window(960, 550, window=self.quit_button)

    def resume(self, event=None):
        if self.player is not None:
            self.canvas.delete(self.pause_label_id)
            self.canvas.delete(self.resume_button_id)
            self.canvas.delete(self.menu_button_id)
            self.canvas.delete(self.quit_button_id)
            self.player.resume()
            self.is_paused = False

    def left(self, event):
        self.player.set_horizontal_velocity(-self.player.get_speed())

    def right(self, event):
        self.player.set_horizontal_velocity(self.player.get_speed())

    def up(self, event):
        self.player.jump()

    def start_game(self):
        self.game_start = True
        self.canvas.delete("all")
        self.canvas.config(bg="black")
        self.configure_window()
        self.master.geometry("1920x1080")
        self.score_label = tk.Label(self.master, text="Score: 0", fg="white", bg="black", font=("Arial Bold", 32))
        self.score_label.place(x=100, y=100)
        self.player = Player(self.canvas)
        self.master.bind("<KeyPress-Escape>", self.pause)
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.after(10, self.game_loop())

    def game_loop(self):
        if self.player is not None:
            self.player.update()
            self.master.after(10, self.game_loop)
            self.update_score()

    def update_score(self):
        if not self.is_paused and self.game_start is True:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.master.after(1000, self.update_score)

    def generate_obstacle(self):
        pass

    def update_obstacles(self):
        pass

    def append_scroll_speed(self, dv):
        self.scroll_speed += dv


class Player:
    def __init__(self, canvas):
        self.id = canvas.create_rectangle(0, 0, 100, 100, fill="white")
        self.canvas = canvas
        self.velocity = [0, 0]
        self.gravity = 0.25
        self.speed = 5
        self.jump_speed = -10
        self.is_jumping = False
        self.is_paused = False

    def update(self):
        if not self.is_paused:
            bbox = self.canvas.bbox(self.id)
            if bbox[3] >= (self.canvas.winfo_height() - 2 * (bbox[3] - bbox[1])) and self.velocity[1] >= 0:
                self.velocity[1] = 0
                self.is_jumping = False
            else:
                self.velocity[1] += self.gravity

            if bbox[2] >= self.canvas.winfo_width() and self.velocity[0] >= 0:
                self.set_horizontal_velocity(0)

            if bbox[0] <= 0 and self.velocity[0] <= 0:
                self.set_horizontal_velocity(0)

            self.canvas.move(self.id, self.velocity[0], self.velocity[1])

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def jump(self):
        if not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True

    def get_id(self):
        return self.id

    def get_velocity(self):
        return self.velocity

    def get_speed(self):
        return self.speed

    def set_horizontal_velocity(self, v):
        self.velocity[0] = v


game = AlienAnnihilator(window)
window.mainloop()  # tells Python to run the Tkinter event loop.
# This method listens for events, such as button clicks or keypresses,
# and blocks any code that comes after it from running until you close
# the window where you called the method.
