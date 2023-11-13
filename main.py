import tkinter as tk

root = tk.Tk()


def setup():
    root.geometry("800x600")
    root.configure(background="#b3ffff")
    root.title("Alien Annihilator")

def gameLoop():
    update()

def update():
    pass

setup()
gameLoop()
root.mainloop()
