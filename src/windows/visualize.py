import tkinter as tk
from src.components.board import Board 
from src.components.globals import H1

class Visualize:
    """ Lets users graphically view a Sokoban warehouse. """
    def __init__(self, root: tk.Tk, path: str):
        self.root = root
        self.root.title("SKBN - Visualizer Tool")
        wh_name = (path.split('/')[-1]).split('.txt')[0]
        tk.Label(self.root, text="Viewing " + wh_name, font=H1).pack(side=tk.TOP, pady=10)
        self.board = Board(self.root, path)
        self.root.mainloop()