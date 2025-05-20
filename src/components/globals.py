import os

SRC_PATH = "\\".join(os.path.realpath(__file__).split('\\')[:-2])

DIRECTIONS = {
    "Up": (0, 1),
    "Down": (0, -1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

BLANK = ' '
BOX = '$'
PLAYER = '@'
BOX_ON_TARGET = '*'
PLAYER_ON_TARGET = '+'
PLAYER_ON_TARGET2 = '!'
TARGET = '.'
WALL = '#'
X = 'X'

IMAGES = {
    BLANK: SRC_PATH + "\\assets\\floor.png",
    BOX: SRC_PATH + "\\assets\\box-on-floor.png",
    PLAYER: SRC_PATH + "\\assets\\player-on-floor.png",
    BOX_ON_TARGET: SRC_PATH + "\\assets\\box-on-target.png",
    PLAYER_ON_TARGET: SRC_PATH + "\\assets\\player-on-target.png",
    PLAYER_ON_TARGET2: SRC_PATH + "\\assets\\player-on-target.png",
    TARGET: SRC_PATH + "\\assets\\target.png",
    WALL: SRC_PATH + "\\assets\\wall.png",
    X: SRC_PATH + "\\assets\\taboo.png"
}

INVAILD_TABOO_REPR_CHARS = [BOX_ON_TARGET, PLAYER_ON_TARGET, PLAYER_ON_TARGET2, TARGET, WALL]
LEGAL_CHARS = [BLANK, BOX, BOX_ON_TARGET, PLAYER, PLAYER_ON_TARGET, PLAYER_ON_TARGET2, TARGET, WALL, X]

VISUALIZE = 1; TABOO = 2; BUTTONS = 2.1; SEQUENCE = 3

H1 = ("Arial", 12, "bold")