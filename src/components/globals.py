DIRECTIONS = {
    "Up": (0, 1),
    "Down": (0, -1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

IMAGES = {
    " ": "./assets/floor.png",
    "$": "./assets/box-on-floor.png",
    "@": "./assets/player-on-floor.png",
    "*": "./assets/box-on-target.png",
    "!": "./assets/player-on-target.png",
    "+": "./assets/player-on-target.png",
    ".": "./assets/target.png",
    "#": "./assets/wall.png",
}

VALID_CHARS = [" ", "X", "$", "@", "*", "!", "+", ".", "#"]

VISUALIZE = 1; TABOO = 2; SEQUENCE = 3

H1 = ("Arial", 12, "bold")