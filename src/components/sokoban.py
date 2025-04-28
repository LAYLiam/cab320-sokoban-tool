from typing import List, Tuple

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
    
    def load_warehouse(self, file_path) -> None:
        """ Load warehouse from .txt file, and record coordinates of elements. """
        with open(file_path, 'r') as f:
            lines = f.readlines() 
        self.from_lines(lines)

    def from_lines(self, lines) -> None:
        """ Iterate over each .txt line, and record coordinates of elements. """
        self.nrows = len(lines) - 2
        self.ncols = len(lines[1])
        for r in range(self.nrows):
            if len(lines[r + 1]) > self.ncols: self.ncols = len(lines[r + 1]) 
            for c in range(len(lines[r + 1])):
                char: str = lines[r + 1][c]
                if char == '@': self.worker = (r, c)
                elif char == '$': self.boxes.append((r, c))
                elif char == '.': self.targets.append((r, c))
                elif char == '#': self.walls.append((r, c))

    def as_array(self) -> List[str]:
        """ Return two dimensional array with warehouse elements added. """
        def insert(grid: List[str], c: Tuple[int, int], char: str) -> None:
            grid[c[0]][c[1]] = char

        grid = [[' ' for i in range(self.ncols)] for j in range(self.nrows)]
        insert(grid, self.worker, '@')
        for box in self.boxes: insert(grid, box, '$')
        for target in self.targets: insert(grid, target, '.')
        for wall in self.walls: insert(grid, wall, '#')
        return grid

    def __str__(self):
        """ Return a string representation of warehouse board. """
        return "\n".join(["".join(r) for r in self.as_array()])

if __name__ == "__main__":
    wh = Warehouse()
    wh.load_warehouse("./warehouses/wh_3.txt")
    print(wh.__str__())