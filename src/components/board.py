import tkinter as tk
from PIL import Image
from PIL import ImageTk
from typing import Tuple, Dict
from components.globals import IMAGES, BUTTONS, TABOO, INVAILD_TABOO_REPR_CHARS, WALL, BLANK
from components.sokoban import Warehouse

class Board:
    """ 
        Creates a new board instance, which is a 
        modifiable representation of the .txt warehouse.
    """
    def __init__(self, root: tk.Frame, path: str, config=None) -> None:
        self.wh = Warehouse(); self.wh.load_warehouse(path)
        self.immutable_board = self.board = self.wh.as_array()
        self.root = root
        self.gui = tk.Frame(self.root).pack()
        self.path = path
        self.config: Dict[str: bool] = config if config != None else {BUTTONS: False, TABOO: False}
        self.tiles = {}
        self.set_gui()
    
    def set_gui(self) -> None:
        """
            Turns character array representation of the board into
            a gui graphical version of the board. 
            If the configuration has buttons enabled, each of the tiles
            will become buttons, otherwise labels are used to display images. 
        """
        board = tk.Frame(self.root); board.pack()
        for y in range(self.wh.nrows):
            for x in range(self.wh.ncols):
                img = Image.open(IMAGES[self.board[y][x]])
                img = img.resize((35,35)); img = ImageTk.PhotoImage(img)
                if self.config[BUTTONS]:
                    # If the config for buttons is enabled, the tiles will
                    # be clickable buttons instead of Labels. Commands can also
                    # be assigned to a mode (i.e., taboo) here.
                    cmd = lambda: print("Nothing assigned to board gui buttons.")
                    if self.config[TABOO]: cmd = lambda x=x, y=y: self.tile_toggled(key=(x, y))
                    tile = tk.Button(board, image=img, command=cmd,
                                     highlightthickness = 2, bd = 1)
                else: tile = tk.Label(board, image=img, borderwidth=0)  
                tile.grid(row=y, column=x)
                self.tiles[(x, y)] = (tile, img, False) # Save tile/image avoid garbage collection.
        if self.config[TABOO]: self.board = self.wh.as_array(walls_only=True)
    
    def tile_toggled(self, key: Tuple[int, int]) -> None:
        """
            Only to be used in conjunction with the taboo setting
            in response to a click event. Takes the tuple key of the tile
            to be toggled to suggest it is a taboo tile. 

            Once clicked, turn red if it is tabooable, otherwise, if
            already taboo, revert to background colour.
        """
        x, y = key
        c = self.board[y][x] if self.board[y][x] == WALL else BLANK
        button, image, taboo = self.tiles[key]
        if (not taboo and self.immutable_board[y][x] not in INVAILD_TABOO_REPR_CHARS):
            bg = "red"; c = "X"
        else: bg = self.root.cget('bg')
        self.board[y][x] = c
        button.config(bg=bg)
        self.tiles[key] = (button, image, not taboo)

    def reset(self) -> None:
        """ Reset the board back to original .txt warehouse. """
        self.board = self.wh.as_array()

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.board])
    
    def __repr__(self) -> str:
        return repr(self.__str__())

if __name__ == "__main__":
    root = tk.Tk()
    path = "C:\\Users\\liaml\\OneDrive\\Desktop\\_\\CAB302\\cab320-sokoban-tool\\warehouses\\wh_1.txt"
    board = Board(root, path, config={BUTTONS: True, TABOO: True})

    def get_repr():
        return print(board.__repr__())

    tk.Button(root, text="Click for repr", command=get_repr).pack()
    root.mainloop()