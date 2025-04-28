import tkinter as tk
from PIL import Image
from PIL import ImageTk
from typing import List, Tuple
import os
from globals import IMAGES, VALID_CHARS
from sokoban import Warehouse

class Board:
    def __init__(self, root: tk.Frame, path: str, buttons=False) -> None:
        self.wh = Warehouse(); self.wh.load_warehouse(path)
        self.board = self.wh.as_array()
        self.root: tk.Frame = root
        self.gui: tk.Frame = tk.Frame(self.root).pack()
        self.path: str = path
        self.buttons: bool = buttons
        self.tiles = {}
        self.set_gui()
    
    def set_gui(self) -> None:
        board = tk.Frame(self.root); board.pack()
        for y in range(self.wh.nrows):
            for x in range(self.wh.ncols):
                img = Image.open(IMAGES[self.board[y][x]])
                img = img.resize((35,35)); img = ImageTk.PhotoImage(img)
                if self.buttons:
                    tile = tk.Button(board, image=img, 
                    command=lambda x=x, y=y: self.tile_toggled(key=(x, y)), 
                    highlightthickness = 2, bd = 1)
                else: tile = tk.Label(board, image=img, borderwidth=0)  
                tile.grid(row=y, column=x)
                self.tiles[(x, y)] = (tile, img, False)
    
    def tile_toggled(self, key: Tuple[int, int]) -> None:
        x, y = key
        c = self.board[y][x] if self.board[y][x] == "#" else " "
        button, image, taboo = self.tiles[key]
        if (not taboo and self.board[y][x] not in ['*', '#', '!', '+', '.']):
            bg = "red"; c = "X"
        else: bg = self.root.cget('bg')
        button.config(bg=bg)
        self.tiles[key] = (button, image, not taboo)

if __name__ == "__main__":
    root = tk.Tk()
    path = "C:\\Users\\liaml\\OneDrive\\Desktop\\_\\CAB302\\cab320-sokoban-tool\\warehouses\\wh_1.txt"
    board = Board(root, path, buttons=True)
    root.mainloop()