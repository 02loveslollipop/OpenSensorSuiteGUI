import redis as rd
from config import config
from main_screen import main_screen
import tkinter as tk
import sv_ttk

#Set the config class
conf = config()

if __name__ == "__main__":
    root = tk.Tk()
    app = main_screen(root,conf)
    sv_ttk.set_theme("dark")
    root.mainloop()