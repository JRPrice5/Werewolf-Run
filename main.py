import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def displayWindow():
    root.geometry("800x600")
    root.configure(background="#b3ffff")
    root.title("Alien Annihilator")
    menuLoop()

def menuLoop():
    startButton = ttk.Button(root, text="START", command=startGame())

def startGame():
    global gameScreen
    gameScreen = True

def gameLoop():
    update()

def update():
    pass

displayWindow()
if gameScreen:
    gameLoop()
root.mainloop()
