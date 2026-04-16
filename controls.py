import curses
from typing import Any

class Controls:
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    IKEY = ord("i")
    QKEY = ord("q")
    SKEY = ord("s")
    ESCKEY = 27
    BSPKEY = curses.KEY_BACKSPACE
    ENTERKEY = 10


class CONTROLS_STRG:
    HELP = ord("G")-64
    CLOSE = ord("X")-64
    SAVE = ord("O")-64
    READ = ord("R")-64
    SEARCH = ord("W")-64
    REPLACE = ord("\\")-64
    CUT = ord("K")-64
    PASTE = ord("U")-64
    LAUNCH = ord("T")-64
    ALIGN = ord("J")-64
    POSITION = ord("C")-64
    GOTO = ord("/")-64


class CONTROLS_ALT:
    UNDO = ord("u")
    REDO = ord("e")