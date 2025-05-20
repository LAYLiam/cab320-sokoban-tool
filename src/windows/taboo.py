import tkinter as tk
import time
from src.components.board import Board 
from src.components.globals import H1, BUTTONS, TABOO

class Taboo:
    """ 
        Lets users graphically view a Sokoban warehouse, and select tiles which 
        are classified as 'taboo'. Taboo within the context of cab320 means that if a box
        were to enter this cell, it would be stuck there (i.e., in a corner)/
    """
    def __init__(self, root: tk.Tk, path: str):
        self.path = path
        self.root = root
        self.root.title("SKBN - Taboo Cell Finder Tool")
        wh_name = (path.split('/')[-1]).split('.txt')[0]
        tk.Label(self.root, text=f"Taboo Cell Finder for {wh_name}", font=H1).pack(side=tk.TOP, pady=10)
        self.set_content()
        self.root.mainloop()

    def set_content(self) -> None:
        """ 
            Adds the board to view (in button form), 
            and the text visualizer on the right hand side.
        """
        self.text_field = tk.Text(self.root)
        self.board = Board(self.root, self.path, config={BUTTONS: True, TABOO: True}, side=tk.LEFT, text_field=self.text_field)
        self.text_field.config(width=self.board.wh.ncols + 5, height=15, state=tk.DISABLED)
        self.text_field.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.status = tk.StringVar(); self.status.set("")
        tk.Label(self.root, text="", textvariable=self.status, bg="white").pack(fill=tk.X)
        tk.Button(self.root, text="Copy REPR", command=self.to_clipboard).pack(fill=tk.X)
        self.board.update_text_field(self.board)

    def to_clipboard(self) -> None:
        """
            Clear user clipboard and replace with repr form of the board,
            which includes newline char \n.
        """
        self.status.set("Copied!")
        self.root.clipboard_clear()
        self.root.clipboard_append(self.board.__repr__())
        self.root.update()
        time.sleep(0.5)
        self.status.set("")