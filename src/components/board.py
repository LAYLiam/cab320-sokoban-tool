import tkinter as tk
from PIL import Image
from PIL import ImageTk
from typing import Tuple, Dict
from components.globals import *
from components.sokoban import Warehouse

class Board:
    """ 
        Creates a new board instance, which is a 
        modifiable representation of the .txt warehouse.
    """
    def __init__(self, root: tk.Frame, path: str, 
                 config=None, side=tk.TOP, text_field=None, build_warehouse_from_array=None) -> None:
        # Create warehouse instance, either use path, or an existing array
        self.wh = Warehouse()
        if build_warehouse_from_array == None: self.wh.load_warehouse(path)
        else: self.wh.from_lines(build_warehouse_from_array)
        self.immutable_board = self.board = self.wh.as_array()
        self.player = self.wh.worker[1], self.wh.worker[0]

        # Save parameters for board visualization 
        self.root = root
        self.gui = tk.Frame(self.root).pack()
        self.path = path
        self.config: Dict[str: bool] = config if config != None else {BUTTONS: False, TABOO: False}
        self.side = side
        self.tiles = {}
        self.text_field = text_field
        self.set_gui()
    
    def set_gui(self) -> None:
        """
            Turns character array representation of the board into
            a gui graphical version of the board. 
            If the configuration has buttons enabled, each of the tiles
            will become buttons, otherwise labels are used to display images. 
        """
        board = tk.Frame(self.root); board.pack(side=self.side)
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
                tile.grid(row=y, column=x, sticky=tk.NSEW)
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
            image = Image.open(IMAGES[X]); c = "X"
        else: image = Image.open(IMAGES[self.immutable_board[y][x]]) 
        image = image.resize((35,35)); image = ImageTk.PhotoImage(image)
        button.config(image=image)
        self.tiles[key] = (button, image, not taboo)
        self.board[y][x] = c
        self.update_text_field(self.__str__())

    def try_tile_shift(self, direction: Tuple[int, int]) -> bool:
        """
            Attempt to shift the player position tile by a direction vector.
            Return true if the shift is possible, otherwise false.
            Direction cannot move the tile > 1 cell in any direction (i.e., (0, 1) UP, (-1, 0) LEFT).
            Impossible moves includes the player tile through a wall, 
            or trying to push a block into another block, or a block into a wall.
        """
        def image_from_char(char: str) -> ImageTk.PhotoImage:
            image = Image.open(IMAGES[char])
            image = image.resize((35,35))
            return ImageTk.PhotoImage(image)
        
        shift = lambda pos, delta: (pos[0] + delta[0], pos[1] + delta[1])
        cell_from_pos = lambda pos: self.board[pos[1]][pos[0]]
        current_cell = cell_from_pos(self.player)
        next_pos = shift(self.player, direction); next_cell = cell_from_pos(next_pos)

        # Player can move to blank or target cell
        if next_cell in [BLANK, TARGET]:
            procedure = [(self.player, BLANK if current_cell == PLAYER else TARGET), 
                         (next_pos, PLAYER if next_cell == BLANK else PLAYER_ON_TARGET)]
            
        # Player can also push a box, or a box which is on a target
        elif next_cell in [BOX, BOX_ON_TARGET]:
            # Only if the to be moved box is not obstructed
            next_next_pos = shift(next_pos, direction)
            next_next_cell = cell_from_pos(next_next_pos)
            if next_next_cell not in [BLANK, TARGET]: return False
            procedure = [(self.player, BLANK if current_cell == PLAYER else TARGET), 
                         (next_pos, PLAYER if next_cell in [BLANK, BOX] else PLAYER_ON_TARGET),
                         (next_next_pos, BOX if next_next_cell == BLANK else BOX_ON_TARGET)]

        # Running into a wall or any other tile is an illegal move
        else: return False
            
        # Apply procedure
        self.player = next_pos
        for cell, char in procedure:
            x, y = cell; self.board[y][x] = char
            tkobj, image, taboo = self.tiles[cell]
            image = image_from_char(char)
            tkobj.config(image=image, borderwidth=0)
            self.tiles[cell] = tkobj, image, taboo
        return True

    def update_text_field(self, text: str) -> None:
        """ If text field is provided, delete all contents and replace with given text. """
        if self.text_field != None: 
            self.text_field.config(state=tk.NORMAL)
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(tk.END, text)
            self.text_field.config(state=tk.DISABLED)

    def reset(self) -> None:
        """ Reset the board back to original .txt warehouse. """
        self.board = self.wh.as_array()

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.board])
    
    def __repr__(self) -> str:
        return repr(self.__str__())