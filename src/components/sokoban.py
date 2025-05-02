from typing import List, Tuple
from src.components.globals import TARGET, PLAYER, BOX, WALL, PLAYER_ON_TARGET, BOX_ON_TARGET

"""
    This class handles parsing .txt file warehouses.
    It removes any padding surrounding the warehouse and stores the
    relative coordinates (with 0,0 starting at the first row and col 
    containing a wall character) for each element in the warehouse.

    For format of this implementation is intended to be compatible
    with warehouses from QUT's CAB320 AI Sokoban assignment. 
    This tool contains 0 answers for the Sokoban assignment, please do not cheat!

    In CAB320's warehouses the characters are as such:
        ' ' -> BLANK                Floor character
        '$' -> BOX                  Box to be pushed onto target
        '@' -> PLAYER               The player character
        '*' -> BOX_ON_TARGET        A box on a target
        '+' -> PLAYER_ON_TARGET     A player on a target
        '!' -> PLAYER_ON_TARGET2    ^ Alternative character 
        '.' -> TARGET               A target for a box to be pushed on
        '#' -> WALL                 A wall character
        'X' -> X                    A taboo cell

    Here's what a warehouse in this style could look like.
        ######      You could copy this warehouse into a text file,
        #   .#      and put it into a directory where you are looking
        #  ###      to store some warehouses.
        #*@  #
        #  $ #      You could then access the directory through main.py,
        #  ####     and double click the warehouse to load it and graphically
        #    *#     see what it looks like with the Visualize tool, 
        #######     or play the warehouse with the Sequence tool.
"""

class Warehouse:
    """
        Creates a new Sokoban warehouse instance.
        Requires self.load_warehouse() to load data from .txt
        to the program. 
    """
    def __init__(self) -> None:
        self.worker: Tuple[int, int] = None
        self.boxes: List[Tuple[int, int]] = []
        self.weights: List[int] = []
        self.targets: List[Tuple[int, int]] = []
        self.walls: List[Tuple[int, int]] = []
        self.ncols: int = None
        self.nrows: int = None

    def copy(self):
        """
            Creates duplicate of a warehouse without having to load .txt file.
            Returns a new Warehouse instance.
        """
        clone = Warehouse()
        clone.worker = self.worker
        clone.boxes = self.boxes
        clone.weights = self.weights
        clone.targets = self.targets
        clone.walls = self.walls
        clone.ncols = self.ncols
        clone.nrows = self.nrows
        return clone
    
    def load_warehouse(self, file_path: str) -> None:
        """ Load warehouse from .txt file, and record coordinates of elements. """
        with open(file_path, 'r') as f:
            lines = f.readlines() 
        self.from_lines(lines)

    def from_lines(self, lines: List[str]) -> None:
        """ 
            Iterate over each .txt line, and record coordinates of elements. 
            Make warehouse coordinates cannonical, where row 0 has at least 1 wall
            and col 0 has at least 1 wall.
        """
        formatted_lines = [r.replace('\n', '') for r in lines if '#' in r]
        self.nrows = len(formatted_lines)

        # Go forward and search for empty no wall columns
        # Remove all no wall columns after.
        forward_start_col = None
        min_cols = min([len(r) for r in formatted_lines])
        for i in range(min_cols):
            for r in formatted_lines:
                if r[i] == WALL: forward_start_col = i; break
            if forward_start_col != None: break
        formatted_lines = [r[forward_start_col:] for r in formatted_lines]

        # Get the coordinates of all the elements in the warehouse
        for r, row in enumerate(formatted_lines):
            for c, char in enumerate(row):
                if char == PLAYER: self.worker = (r, c)
                elif char == BOX: self.boxes.append((r, c))
                elif char == TARGET: self.targets.append((r, c))
                elif char == WALL: self.walls.append((r, c))
                elif char == PLAYER_ON_TARGET: self.worker = (r, c); self.targets.append((r, c))
                elif char == BOX_ON_TARGET: self.boxes.append((r, c)); self.targets.append((r, c))
        self.ncols = max({cell[1] for cell in self.walls}) + 1

    def as_array(self, walls_only=False) -> List[str]:
        """ 
            Return two dimensional array with warehouse elements added. 
            Option to get array with only walls and empty spaces.
        """
        def insert(grid: List[str], c: Tuple[int, int], char: str) -> None:
            grid[c[0]][c[1]] = char

        grid = [[' ' for i in range(self.ncols)] for j in range(self.nrows)]
        for wall in self.walls: insert(grid, wall, WALL)
        if not walls_only:
            for target in self.targets: insert(grid, target, TARGET)
            for box in self.boxes: 
                if box in self.targets: insert(grid, box, BOX_ON_TARGET)
                else: insert(grid, box, BOX)
            if self.worker in self.targets: insert(grid, self.worker, PLAYER_ON_TARGET)
            else: insert(grid, self.worker, PLAYER)
        return grid

    def __str__(self):
        """ Return a string representation of warehouse board. """
        return "\n".join(["".join(r) for r in self.as_array()])

if __name__ == "__main__":
    wh = Warehouse()
    wh.load_warehouse("./warehouses/wh_3.txt")
    print(wh.__str__())