import tkinter as tk
from components.builder import Builder
from components.globals import H1

class BuildBoard:
    """ Lets users graphically build a Sokoban warehouse. """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.focus_force()
        self.root.title("SKBN - Builder Tool")
        tk.Label(self.root, text="Build Sokoban Warehouse Tool", font=H1).pack(side=tk.TOP, pady=10)
        self.builder = Builder(self.root)
        self.root.mainloop()