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

        self.name = ""
        self.time = 0
        # self.scroll_speed = -5

        self.enemies = []
        self.enemy_spawn_range = [3000, 4500]
        self.enemy_width = 100
        self.enemy_height = 100
        self.enemy_speed = -1.5

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
                                      height=self.BUTTON_HEIGHT, command=self.input_name)
        self.leaderboard_label = None
        self.leaderboard_button = tk.Button(self.master_window, text="LEADERBOARD", width=self.BUTTON_WIDTH,
                                            height=self.BUTTON_HEIGHT, command=self.show_leaderboard)
        self.leaderboard_frame = None
        self.bindings_button = tk.Button(self.master_window, text="KEY BINDINGS", width=self.BUTTON_WIDTH,
                                         height=self.BUTTON_HEIGHT, command=self.show_key_bindings)
        self.quit_button = tk.Button(self.master_window, text="QUIT", width=self.BUTTON_WIDTH,
                                     height=self.BUTTON_HEIGHT,
                                     command=self.master_window.destroy)
        self.menu_button = tk.Button(self.master_window, text="MENU", width=self.BUTTON_WIDTH,
                                     height=self.BUTTON_HEIGHT,
                                     command=self.menu)
        self.resume_button = tk.Button(self.master_window, text="RESUME", width=self.BUTTON_WIDTH,
                                       height=self.BUTTON_HEIGHT,
                                       command=self.resume)
        self.time_label = tk.Label(self.master_window, text="0", fg="white", bg="black", bd=0,
                                   font=("Arial Bold", 64))

        self.enter_name_label = tk.Label(self.master_window, text="ENTER NAME", fg="white", bg="black",
                                         font=("Arial Bold", 32))
        self.name_label = tk.Label(self.master_window, text="", fg="white", bg="black", font=("Arial Bold", 32))
        self.name_entry = tk.Entry(self.master_window, width=30)
        self.submit_button = tk.Button(self.master_window, text="Submit", command=self.submit_name)

        self.player_states = {"Run": 8, "Jump": 12, "Dead": 4, "Walk": 8, "Idle": 6}
        self.player_state = "Run"
        self.player_sheet_path = f"images/Shinobi/{self.player_state}.png"
        self.player_sheet = Image.open(self.player_sheet_path)
        self.player_width = self.player_sheet.width // self.player_states.get(self.player_state)
        self.player_height = self.player_sheet.height
        self.player_frames = [ImageTk.PhotoImage(self.player_sheet.crop((i * self.player_width, 0, (i + 1) *
                                                                         self.player_width, self.player_height)))
                              for i in range(self.player_states.get(self.player_state))]

        self.enemy_states = {"Run": 9, "walk": 11}
        self.enemy_state = "walk"
        self.enemy_sheet_path = f"images/Black_Werewolf/{self.enemy_state}.png"
        self.enemy_sheet = Image.open(self.enemy_sheet_path)
        self.enemy_width = self.enemy_sheet.width // self.enemy_states.get(self.enemy_state)
        self.enemy_height = self.enemy_sheet.height
        self.enemy_frames = [ImageTk.PhotoImage(self.enemy_sheet.crop((i * self.enemy_width, 0, (i + 1) *
                                                                       self.enemy_width, self.enemy_height)))
                             for i in range(self.enemy_states.get(self.enemy_state))]

        self.background_images = []
        self.background_images.append(ImageTk.PhotoImage(Image.open("images/m8/first.png")))
        self.background_images.append(ImageTk.PhotoImage(Image.open("images/m8/second.png")))
        self.background_images.append(ImageTk.PhotoImage(Image.open("images/m8/third.png")))
        self.background_image_ids = []

        self.platform_image = ImageTk.PhotoImage(Image.open("images/platformv3.png"))

        self.menu()

    def configure_window(self):
        self.master_window.geometry("1920x1080")
        self.master_window.attributes("-fullscreen", True)
        self.master_window.title("Werewolf Run")

    def set_background(self, is_running=True):
        self.canvas.delete("all")  # Clear the canvas
        if is_running:
            for image in self.background_images:
                self.canvas.create_image((0, 0), image=image, anchor="nw")
            for i in range(0, 4):
                self.canvas.create_image((i * self.platform_image.width(), (4 * self.canvas.winfo_height() / 5) + 25),
                                         image=self.platform_image, anchor="nw")
        else:
            # Code to set the background for the menu screen
            pass

    def menu(self, event=None):
        self.is_paused = False
        self.master_window.bind("<KeyPress-Escape>", None)
        if self.player is not None:
            self.canvas.delete(self.player.get_id())
            self.player = None
            self.time_label.destroy()
            self.time = 0
        self.canvas.delete("all")
        self.canvas.config(bg="black")
        self.set_background(is_running=False)
        self.game_start = False
        self.canvas.pack(fill="both", expand=True)
        self.configure_window()
        self.canvas.create_text(960, 250, text="WEREWOLF RUN", fill="white", font=("Arial Bold", 80))
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
            for enemy in self.enemies:
                enemy.pause()
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
            for enemy in self.enemies:
                enemy.resume()
            self.is_paused = False

            self.master_window.after(1000, self.update_time)

    def left(self, event):
        if self.player.get_state() == "Run" or self.player.get_state() == "Idle":
            self.player.set_state("Walk")
            self.player.set_current_frame(8)
            self.player.set_sprite_frames()
            self.player.set_horizontal_velocity(-2 * self.player.get_speed() / 3)
        elif self.player.get_is_jumping():
            self.player.set_horizontal_velocity(-2 * self.player.get_speed() / 3)

    def right(self, event):
        if self.player.get_state() == "Walk" or self.player.get_state() == "Idle":
            self.player.set_state("Run")
            self.player.set_current_frame(8)
            self.player.set_sprite_frames()
            self.player.set_horizontal_velocity(self.player.get_speed())
        elif self.player.get_is_jumping():
            self.player.set_horizontal_velocity(self.player.get_speed())

    def up(self, event):
        if not self.player.get_is_jumping() and self.player.get_state != "Death":
            self.player.set_state("Jump")
            self.player.set_sprite_frames()
            self.player.set_current_frame(0)
            self.player.jump()

    def start_game(self):
        self.canvas.delete("all")
        self.canvas.config(bg="black")

        self.set_background(is_running=True)

        self.name_label.destroy()
        self.name_entry.destroy()
        self.submit_button.destroy()

        self.game_start = True
        self.time_label = tk.Label(self.master_window, text="0", fg="white", bg="black", font=("Arial Bold", 64))
        self.time_label.place(relx=0.5, rely=0.2, anchor="center")
        self.player = Player(self.canvas, self.player_frames)

        self.master_window.bind("<Left>", self.left)
        self.master_window.bind("<Right>", self.right)
        self.master_window.bind("<Up>", self.up)

        self.master_window.after(10, self.generate_enemies)
        self.master_window.after(10, self.game_loop)
        self.master_window.after(100, self.player.animate)
        self.master_window.after(1000, self.update_time)
        self.master_window.after(15000, self.increase_difficulty)
        # self.master_window.after(2000, self.game_over)

    def input_name(self):
        self.canvas.delete("all")
        self.canvas.config(bg="black")
        self.enter_name_label.place(relx=0.5, rely=0.4, anchor="center")
        self.name_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.submit_button.place(relx=0.5, rely=0.55, anchor="center")
        self.master_window.bind("<Return>", self.enter_pressed)

    def submit_name(self):
        self.master_window.bind("<Return>", None)
        self.enter_name_label.destroy()
        self.name = self.name_entry.get()
        self.name_label.place(relx=0.5, rely=0.4, anchor="center")
        self.name_label.config(text=f"YOUR NAME IS {self.name.upper()}")
        self.master_window.after(3000, self.start_game)

    def enter_pressed(self, event):
        self.submit_button.invoke()

    def game_loop(self):
        if self.player is not None:
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
            self.master_window.after(10, self.game_loop)

    def update_time(self):
        if not self.is_paused and self.game_start:
            self.time += 1
            self.time_label.config(text=f"{self.time}")

        if not self.is_paused:
            if self.time_after_id is not None:
                self.master_window.after_cancel(self.time_after_id)
            self.time_after_id = self.master_window.after(1000, self.update_time)

        if self.time % 15 == 0:
            self.time_label.config(fg="red")
        else:
            self.time_label.config(fg="white")

    def generate_enemies(self):
        if self.game_start and not self.is_paused:
            if self.time >= 105:
                type = 3
                state = "Run"
            elif self.time >= 90:
                type = random.randint(2, 3)
                state = "Run"
            elif self.time >= 75:
                type = random.randint(1, 3)
                state = "Run"
            elif self.time >= 60:
                type = random.randint(1, 3)
                if type == 3:
                    state = "Walk"
                else:
                    state = "Run"
            elif self.time >= 45:
                type = random.randint(1, 2)
                state = "Run"
            elif self.time >= 30:
                type = random.randint(1, 2)
                if type == 2:
                    state = "Walk"
                else:
                    state = "Run"
            elif self.time >= 15:
                type = 1
                state = "Run"
            else:
                type = 1
                state = "Walk"

            enemy = Enemy(self.canvas, self.enemies, state, type, self.enemy_frames, self.enemy_speed)

            self.enemies.append(enemy)
            self.master_window.after(100, enemy.animate)
            self.master_window.after(13000, lambda: self.delete_enemy(enemy))
            self.master_window.after(random.randint(self.enemy_spawn_range[0], self.enemy_spawn_range[1]),
                                     self.generate_enemies)

    def delete_enemy(self, enemy):
        self.enemies.remove(enemy)
        self.canvas.delete(enemy.get_id())

    def increase_difficulty(self):
        if self.game_start and not self.is_paused:
            self.enemy_speed -= 1.5
            if self.enemy_spawn_range[0] >= 1000:
                self.enemy_spawn_range[0] -= 250
                self.enemy_spawn_range[1] -= 250
            self.master_window.after(15000, self.increase_difficulty)

    def game_over(self):
        self.game_start = False
        self.master_window.bind("<KeyPress-Escape>", None)
        self.canvas.delete(self.player.get_id())
        self.player = None
        self.time_label.destroy()
        self.canvas.delete("all")

        leaderboard = {}
        file = open("leaderboard.txt", "r")
        for line in file:
            name, time = line.strip().split(",")
            leaderboard[name] = int(time)

        leaderboard[self.name.upper()] = self.time

        file = open("leaderboard.txt", "w")
        for entry in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
            file.write(f"{entry[0]},{entry[1]}\n")

    def show_leaderboard(self):
        self.canvas.delete("all")
        self.canvas.config(bg="black")

        self.leaderboard_frame = tk.Frame(self.master_window, bg="black")
        self.leaderboard_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.leaderboard_label = tk.Label(self.master_window, text="LEADERBOARD", fg="white", bg="black",
                                          font=("Arial Bold", 64))
        self.leaderboard_label.place(relx=0.5, rely=0.2, anchor="center")

        leaderboard_canvas = tk.Canvas(self.leaderboard_frame, bg="black", width=500, height=400)
        scrollbar = tk.Scrollbar(self.leaderboard_frame, orient="vertical", command=leaderboard_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        leaderboard_canvas.pack(side="left", fill="both", expand=True)
        leaderboard_canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(leaderboard_canvas, bg="black")
        leaderboard_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        file = open("leaderboard.txt", "r")
        i = 1
        for line in file:
            name, time = line.strip().split(",")
            entry_text = f"{i}. {name}: {time}"
            entry_label = tk.Label(inner_frame, text=entry_text, fg="white", bg="black", font=("Arial Bold", 20))
            entry_label.pack(pady=5)
            i += 1

        back_button = tk.Button(self.leaderboard_frame, text="Back to Menu", command=self.clear_leaderboard,
                                width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, font=("Arial Bold", 16))
        back_button.place(relx=0.5, rely=0.9, anchor="center")

        inner_frame.update_idletasks()
        leaderboard_canvas.config(scrollregion=leaderboard_canvas.bbox("all"))

    def clear_leaderboard(self):
        self.leaderboard_label.destroy()
        self.leaderboard_frame.destroy()
        self.menu()

    def show_key_bindings(self):
        pass

    def check_collisions(self):
        pass


class Player:
    def __init__(self, canvas, sprite_frames):
        self.canvas = canvas
        self.states = {"Run": 8, "Jump": 12, "Dead": 4, "Walk": 8, "Idle": 6}
        self.state = "Walk"
        self.sprite_sheet_path = f"images/Shinobi/{self.state}.png"
        self.sprite_sheet = Image.open(self.sprite_sheet_path)
        self.width = self.sprite_sheet.width // self.states.get(self.state)
        self.height = self.sprite_sheet.height
        self.sprite_frames = [ImageTk.PhotoImage(self.sprite_sheet.crop((i * self.width, 0, (i + 1) *
                                                                         self.width, self.height)))
                              for i in range(self.states.get(self.state))]
        self.current_frame = 0
        self.id = canvas.create_image(0, (4 * canvas.winfo_height() / 5) + 33 - self.height, anchor=tk.NW,
                                      image=sprite_frames[0])
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.speed = 4
        self.jump_speed = -16
        self.is_jumping = False
        self.is_paused = False

    def update(self):
        if not self.is_paused:
            bbox = self.canvas.bbox(self.id)
            if bbox[3] >= ((4 * self.canvas.winfo_height() / 5) + 25) and self.velocity[1] >= 0:
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
                if not self.is_jumping and self.state != "Idle":
                    self.state = "Idle"
                    self.set_sprite_frames()
                self.set_horizontal_velocity(0)

            if bbox[0] <= 0 and self.velocity[0] <= 0:
                if not self.is_jumping and self.state != "Idle":
                    self.state = "Idle"
                    self.set_sprite_frames()
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
            if self.state == "Walk":
                self.current_frame = (self.current_frame - 1) % len(self.sprite_frames)
            else:
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


class Enemy:
    def __init__(self, canvas, enemies, state, sprite_type, sprite_frames, speed):
        enemies.append(self)
        self.is_paused = False
        self.canvas = canvas
        self.speed = speed
        self.states = {"Run": 9, "Walk": 11}
        self.types = ["White_Werewolf", "Black_Werewolf", "Red_Werewolf"]
        self.type = self.types[sprite_type-1]
        self.state = state
        self.sprite_sheet_path = f"images/{self.type}/{self.state}.png"
        self.sprite_sheet = Image.open(self.sprite_sheet_path).transpose(Image.FLIP_LEFT_RIGHT)
        self.width = self.sprite_sheet.width // self.states.get(self.state)
        self.height = self.sprite_sheet.height
        self.id = canvas.create_image(canvas.winfo_width() + self.width, (4 * canvas.winfo_height() / 5) + 33 -
                                      self.height, anchor=tk.NW, image=sprite_frames[0])

        self.sprite_frames = [ImageTk.PhotoImage(self.sprite_sheet.crop((i * self.width, 0, (i + 1) *
                                                                         self.width, self.height)))
                              for i in range(self.states.get(self.state))]
        self.current_frame = 0

    def update(self):
        if not self.is_paused:
            self.canvas.move(self.id, self.speed, 0)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        self.animate()

    def animate(self):
        if not self.is_paused:
            self.current_frame = (self.current_frame - 1) % len(self.sprite_frames)
            image = self.sprite_frames[self.current_frame]
            self.canvas.itemconfig(self.id, image=image)
            self.canvas.after(100, self.animate)

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def get_current_frame(self):
        return self.current_frame

    def set_state(self, state):
        self.state = state


game = AlienAnnihilator(window)
window.mainloop()  # tells Python to run the Tkinter event loop.
# This method listens for events, such as button clicks or key presses,
# and blocks any code that comes after it from running until you close
# the window where you called the method.
