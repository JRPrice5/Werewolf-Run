import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# ensure pep 8 formatting
# comment code
# 1920x1080 resolution
window = tk.Tk()


class AlienAnnihilator:
    def __init__(self, window):
        self.BUTTON_WIDTH = 15
        self.BUTTON_HEIGHT = 2
        self.GROUND_HEIGHT = 876

        self.time = 0
        self.scroll_speed = -5

        self.obstacles = []
        self.obstacle_spawn_range = [3000, 4500]
        self.obstacle_width = 100
        self.obstacle_height = 100

        self.pause_label_id = None
        self.resume_button_id = None
        self.menu_button_id = None
        self.quit_button_id = None
        self.time_after_id = None

        self.player = None

        self.is_paused = False

        self.master_window = window  # initialises master_window window
        self.game_start = False  # the game loop doesn't initially run

        self.canvas = tk.Canvas(self.master_window, width=800, height=600)
        self.canvas.place(x=50, y=50)

        self.start_button = tk.Button(self.master_window, text="START", width=self.BUTTON_WIDTH,
                                      height=self.BUTTON_HEIGHT, command=self.start_game)
        self.leaderboard_button = tk.Button(self.master_window, text="LEADERBOARD", width=self.BUTTON_WIDTH,
                                            height=self.BUTTON_HEIGHT, command=None)
        self.bindings_button = tk.Button(self.master_window, text="KEY BINDINGS", width=self.BUTTON_WIDTH,
                                         height=self.BUTTON_HEIGHT, command=None)
        self.quit_button = tk.Button(self.master_window, text="QUIT", width=self.BUTTON_WIDTH,
                                     height=self.BUTTON_HEIGHT,
                                     command=self.master_window.destroy)
        self.menu_button = tk.Button(self.master_window, text="MENU", width=self.BUTTON_WIDTH,
                                     height=self.BUTTON_HEIGHT,
                                     command=self.menu)
        self.resume_button = tk.Button(self.master_window, text="RESUME", width=self.BUTTON_WIDTH,
                                       height=self.BUTTON_HEIGHT,
                                       command=self.resume)
        self.time_label = tk.Label(self.master_window, text="0", fg="white", bg="black", font=("Arial Bold", 64))

        self.player_states = {"Run": 8, "Jump": 12, "Dead": 4, "Walk": 8}
        self.player_state = "Run"
        self.player_sheet_path = f"images/Shinobi/{self.player_state}.png"
        self.player_sheet = Image.open(self.player_sheet_path)
        self.player_width = self.player_sheet.width // self.player_states.get(self.player_state)
        self.player_height = self.player_sheet.height
        self.player_frames = [ImageTk.PhotoImage(self.player_sheet.crop((i * self.player_width, 0, (i + 1) *
                                                                         self.player_width, self.player_height)))
                              for i in range(self.player_states.get(self.player_state))]
        self.menu()

    def configure_window(self):
        self.master_window.geometry("1920x1080")
        self.master_window.attributes("-fullscreen", True)
        self.master_window.title("Alien Annihilator")

    def menu(self, event=None):
        self.is_paused = False
        self.master_window.bind("<KeyPress-Escape>", None)
        if self.player is not None:
            self.canvas.delete(self.player.get_id())
            self.player = None
            self.time_label.destroy()
            self.time = 0
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
        if self.player is not None and self.is_paused:
            self.canvas.delete(self.pause_label_id)
            self.canvas.delete(self.resume_button_id)
            self.canvas.delete(self.menu_button_id)
            self.canvas.delete(self.quit_button_id)
            self.player.resume()
            self.is_paused = False

            self.master_window.after(1000, self.update_time)

    def left(self, event):
        if self.player.get_state() == "Run":
            self.player.set_state("Walk")
            self.player.set_current_frame(8)
            self.player.set_sprite_frames()
            self.player.set_horizontal_velocity(-self.player.get_speed())
        elif self.player.get_is_jumping():
            self.player.set_horizontal_velocity(-self.player.get_speed())

    def right(self, event):
        if self.player.get_state() == "Walk":
            self.player.set_state("Run")
            self.player.set_current_frame(8)
            self.player.set_sprite_frames()
            self.player.set_horizontal_velocity(self.player.get_speed())
        elif self.player.get_is_jumping():
            self.player.set_horizontal_velocity(self.player.get_speed())

    def up(self, event):
        if not self.player.get_is_jumping():
            self.player.set_state("Jump")
            self.player.set_sprite_frames()
            self.player.set_current_frame(0)
            self.player.jump()

    def start_game(self):
        self.canvas.delete("all")
        self.canvas.config(bg="black")
        # entry = tk.Entry(self.master_window, width=30)
        # entry.place()
        self.game_start = True
        self.time_label = tk.Label(self.master_window, text="0", fg="white", bg="black", font=("Arial Bold", 64))
        self.time_label.place(relx=0.5, rely=0.2, anchor="center")
        self.player = Player(self.canvas, self.player_frames)
        self.master_window.bind("<KeyPress-Escape>", self.pause)
        self.master_window.bind("<Left>", self.left)
        self.master_window.bind("<Right>", self.right)
        self.master_window.bind("<Up>", self.up)

        self.master_window.after(10, self.generate_obstacles)
        self.master_window.after(10, self.game_loop)
        self.master_window.after(10, self.player.animate)
        self.master_window.after(1000, self.update_time)
        self.master_window.after(10000, self.increase_difficulty)

    def game_loop(self):
        if self.player is not None:
            self.player.update()
            self.master_window.after(10, self.game_loop)
            self.update_obstacles()

    def update_time(self):
        if not self.is_paused and self.game_start:
            self.time += 1
            self.time_label.config(text=f"{self.time}")

        if not self.is_paused:
            if self.time_after_id is not None:
                self.master_window.after_cancel(self.time_after_id)
            self.time_after_id = self.master_window.after(1000, self.update_time)

        if self.time % 10 == 0:
            self.time_label.config(fg="red")
        else:
            self.time_label.config(fg="white")

    def generate_obstacles(self):
        if self.game_start and not self.is_paused:
            width = random.randint(50, self.obstacle_width)
            height = random.randint(50, self.obstacle_height)
            x = self.canvas.winfo_width() + width
            y = self.GROUND_HEIGHT - height
            obstacle = self.canvas.create_rectangle(x, y, x + width, y + height, fill="red")
            self.obstacles.append(obstacle)
            self.master_window.after(10000, lambda: self.delete_obstacle(obstacle))
            self.master_window.after(random.randint(self.obstacle_spawn_range[0], self.obstacle_spawn_range[1]),
                                     self.generate_obstacles)

    def delete_obstacle(self, obstacle):
        self.canvas.delete(obstacle)
        self.obstacles.remove(obstacle)

    def update_obstacles(self):
        if self.game_start and not self.is_paused:
            for obstacle in self.obstacles:
                self.canvas.move(obstacle, self.scroll_speed, 0)

    def append_scroll_speed(self, dv):
        self.scroll_speed -= dv

    def increase_obstacle_size(self):
        if self.obstacle_width < 250:
            self.obstacle_width += 50
            self.obstacle_height += 50

    def increase_difficulty(self):
        if self.game_start and not self.is_paused:
            self.append_scroll_speed(0.5)
            if self.obstacle_spawn_range[0] > 1000:
                self.obstacle_spawn_range[0] -= 250
                self.obstacle_spawn_range[1] -= 250
            self.increase_obstacle_size()
            self.master_window.after(10000, self.increase_difficulty)


class Player:
    def __init__(self, canvas, sprite_frames):
        self.canvas = canvas
        self.states = {"Run": 8, "Jump": 12, "Dead": 4, "Walk": 8}
        self.state = "Walk"
        self.sprite_sheet_path = f"images/Shinobi/{self.state}.png"
        self.sprite_sheet = Image.open(self.sprite_sheet_path)
        self.width = self.sprite_sheet.width // self.states.get(self.state)
        self.height = self.sprite_sheet.height
        self.sprite_frames = [ImageTk.PhotoImage(self.sprite_sheet.crop((i * self.width, 0, (i + 1) *
                                                                         self.width, self.height)))
                              for i in range(self.states.get(self.state))]
        self.current_frame = 0
        self.id = canvas.create_image(0, 0, anchor=tk.NW, image=sprite_frames[0])
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.speed = 4
        self.jump_speed = -16
        self.is_jumping = False
        self.is_paused = False

    def update(self):
        if not self.is_paused:
            bbox = self.canvas.bbox(self.id)
            if bbox[3] >= (self.canvas.winfo_height() - 200) and self.velocity[1] >= 0:
                self.velocity[1] = 0
                self.is_jumping = False
                if (self.velocity[0] > 0 or bbox[2] >= self.canvas.winfo_width()) and self.state == "Jump":
                    self.current_frame = 8
                    self.state = "Run"
                    self.set_sprite_frames()
                elif (self.velocity[0] < 0 or bbox[0] <= 0) and self.state == "Jump":
                    self.current_frame = 8
                    self.state = "Walk"
                    self.set_sprite_frames()
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
        self.animate()

    def jump(self):
        if not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True

    def animate(self):
        if not self.is_paused:
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.canvas.itemconfig(self.id, image=self.sprite_frames[self.current_frame])
            self.canvas.after(100, self.animate)

    def get_is_jumping(self):
        return self.is_jumping

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def get_velocity(self):
        return self.velocity

    def get_speed(self):
        return self.speed

    def get_horizontal_velocity(self):
        return self.velocity[0]

    def set_horizontal_velocity(self, v):
        self.velocity[0] = v

    def set_sprite_frames(self):
        if self.state is not None:
            self.sprite_sheet_path = f"images/Shinobi/{self.state}.png"
            self.sprite_sheet = Image.open(self.sprite_sheet_path)
            self.width = self.sprite_sheet.width // self.states.get(self.state)
            self.height = self.sprite_sheet.height
            self.current_frame = min(self.current_frame, self.states.get(self.state) - 1)
            self.sprite_frames = [ImageTk.PhotoImage(self.sprite_sheet.crop((i * self.width, 0, (i + 1) *
                                                                             self.width, self.height)))
                                  for i in range(self.states.get(self.state))]

    def set_current_frame(self, current_frame):
        self.current_frame = current_frame

    def set_state(self, state):
        self.state = state


game = AlienAnnihilator(window)
window.mainloop()  # tells Python to run the Tkinter event loop.
# This method listens for events, such as button clicks or keypresses,
# and blocks any code that comes after it from running until you close
# the window where you called the method.
