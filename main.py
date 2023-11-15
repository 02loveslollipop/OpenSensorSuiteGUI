import redis as rd
from config import config
from main_screen import main_screen
import tkinter as tk
import sv_ttk

#Set the config class
conf = config()
#Init the redis connection

def connect():
  return rd.Redis(host=conf.host, port=conf.port, c=conf.password)



if __name__ == "__main__":
    root = tk.Tk()
    app = main_screen(root)
    sv_ttk.set_theme("dark")
    root.mainloop()



