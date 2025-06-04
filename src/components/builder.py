import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import time
from typing import Tuple, List
from components.globals import *

class Builder:
    """ 
        Lets users graphically build Sokoban warehouse,
        and then save the warehouse in string form, or to a text file.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.buttons = {}
        self.dimensionality = (8, 8)
        self.content = tk.Frame(self.root); self.content.pack(side=tk.LEFT, fill=tk.Y)
        self.grid = tk.Frame(self.content); self.grid.pack(side=tk.TOP)
        self.setup_board()
        self.setup_control_panel()

    def new_tile(self, x: int, y: int, tile: str) -> None:
        """ Creates and stores a new tile (i.e., blank tile). """
        img = Image.open(IMAGES[tile])
        img = img.resize((35,35)); img = ImageTk.PhotoImage(img)
        button = tk.Button(self.grid, image=img, 
                            command=lambda x=x, y=y: self.replace_tile(key=(x, y)),
                            highlightthickness = 2, bd = 1)
        button.grid(row=y, column=x, sticky=tk.NSEW)
        self.buttons[(x, y)] = (button, img, BLANK) # Save tile/image avoid garbage collection.

    def setup_board(self) -> None:
        """ 
            Creates an initial board of size 8x8,
            or is conformed to the tuple sizing of self.dimensonality.
        """
        for y in range(self.dimensionality[1]):
            for x in range(self.dimensionality[0]):
                self.new_tile(x, y, BLANK)

    def setup_control_panel(self) -> None:
        """ Sets up the additional user controls for creating the warehouse. """
        self.choice = tk.IntVar()
        panel = tk.Frame(self.root); panel.pack(side=tk.RIGHT, expand=True, fill=tk.Y)
        
        # Display tile options in order of globals.LEGAL_CHARS, 
        # value is index of char in LEGAL_CHARS
        tk.Label(panel, text="Select:").pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Blank", variable=self.choice, value=0).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Box", variable=self.choice, value=1).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Box on target", variable=self.choice, value=2).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Player", variable=self.choice, value=3).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Player on target", variable=self.choice, value=4).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Target", variable=self.choice, value=6).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Wall", variable=self.choice, value=7).pack(side=tk.TOP, anchor=tk.NW)
        tk.Radiobutton(panel, text="Taboo", variable=self.choice, value=8).pack(side=tk.TOP, anchor=tk.NW)
        self.choice.set(0)

        # Give option for the user to clear all tiles, and copy the board in repr form
        self.status = tk.StringVar(); self.status.set("")
        tk.Button(panel, text="Save Board", command=self.save_board).pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(panel, text="Copy Board", command=self.copy_board).pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(panel, text="", textvariable=self.status, bg="white").pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(panel, text="Clear", command=self.clear).pack(side=tk.BOTTOM, fill=tk.X)

        # Give option to take or remove columns
        modifiers = tk.Frame(self.content); modifiers.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(modifiers, text=" ➕ ", command=lambda: self.modify(0, 0)).pack(side=tk.LEFT)
        tk.Label(modifiers, text=" Row ").pack(side=tk.LEFT)
        tk.Button(modifiers, text=" ➖ ", command=lambda: self.modify(1, 0)).pack(side=tk.LEFT) 
        
        tk.Button(modifiers, text=" ➖ ", command=lambda: self.modify(1, 1)).pack(side=tk.RIGHT) 
        tk.Label(modifiers, text=" Column ").pack(side=tk.RIGHT)
        tk.Button(modifiers, text=" ➕ ", command=lambda: self.modify(0, 1)).pack(side=tk.RIGHT)

    def replace_tile(self, key: Tuple[int, int]) -> None:
        """ 
            Replace a tile in the grid with whatever tile is selected. 
            If the tile being requested is already the same type of tile,
            assume a request is being made to turn the tile into BLANK.
        """
        button, img, tile = self.buttons[key]
        tile = (
            BLANK if tile == LEGAL_CHARS[self.choice.get()] 
            else LEGAL_CHARS[self.choice.get()]
        )
        img = Image.open(IMAGES[tile])
        img = img.resize((35,35)); img = ImageTk.PhotoImage(img)
        button.config(image=img)
        self.buttons[key] = (button, img, tile)

    def clear(self) -> None:
        """ Sets all the tiles in the board to BLANK. """
        for y in range(self.dimensionality[1]):
            for x in range(self.dimensionality[0]):
                self.choice.set(0)
                self.replace_tile(key=(x, y))

    def modify(self, action: int, direction: int) -> None:
        """ 
            Can add, or subtract rows and columns from the grid.
            If action is equal to 0, consider that the user
            is requesting to add. Otherwise, if 1, the user is
            requesting to remove. 

            If direction is 0, the user is requesting to perform
            the action on a row. Otherwise, if 1, by column. 
        """
        # If remove, avoid going below dimensionality of 3x3
        if (action == 1 and self.dimensionality[1 if direction == 0 else 0] <= 3): return

        # Where action=0, add, action=1, remove 
        # and direction=0, row, direction=1, col
        for i in range(self.dimensionality[direction]):
            x = i if direction == 0 else self.dimensionality[0]
            y = i if direction == 1 else self.dimensionality[1]
            if action == 0: self.new_tile(x, y, BLANK)
            else:
                button, _, _ = self.buttons[
                    (x, y - 1) if direction == 0 else (x - 1, y)
                ]
                button.grid_forget()
        
        # Update the dimensionality of the board
        modifier = 1 if action == 0 else -1
        x, y = self.dimensionality
        self.dimensionality = (x + modifier, y) if direction == 1 else (x, y + modifier)

    def as_rows(self) -> List[str]:
        """ Get the grid representation as an array of string rows. """
        board = []
        for y in range(self.dimensionality[1]):
            row = ""
            for x in range(self.dimensionality[0]):
                if (x, y) in self.buttons:
                    _, _, tile = self.buttons[(x, y)] 
                    row += tile
                else: row += BLANK
            board.append(row)
        return board

    def copy_board(self) -> None:
        """ Copy the repr version of the board to clipboard. """
        self.status.set("Copied!")
        self.root.clipboard_clear()
        self.root.clipboard_append(repr('\n'.join(self.as_rows())))
        self.root.update()
        time.sleep(0.5)
        self.status.set("")

    def save_board(self) -> None:
        """ 
            Save the board to a text file, which the user chooses the
            location for by using tkinter asksavefilename.
            If the user does not provide .txt at the end, add it.
        """
        rows = [row + '\n' for row in self.as_rows()]
        self.status.set("Saving...")

        # Request for filename & absolute path from pop-up window, then        
        # Write rows to txt file and save
        filename = filedialog.asksaveasfilename()
        if filename != "": 
            if filename[-4:] != ".txt": filename += ".txt"
            with open(filename, "w") as file:
                file.writelines(rows)
        else: self.status.set("Cancelled...")

        self.root.update()
        time.sleep(0.5)
        self.status.set("")
        pass