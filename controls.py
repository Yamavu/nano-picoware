import curses


def Strg(char: str) -> int:
    """return key value for Strg+char"""
    return ord(char) - 64


def unStrg(key: int) -> str:
    """revert Strg() and get the underlying character"""
    return chr(key + 64)


class Controls:
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    ESCKEY = 27
    BSPKEY = curses.KEY_BACKSPACE
    ENTERKEY = 10
    HELP = Strg("H")
    CLOSE = Strg("X")
    SAVE = Strg("O")
    READ = Strg("R")
    SEARCH = Strg("W")
    REPLACE = Strg("E")
    CUT = Strg("K")
    PASTE = Strg("U")
    LAUNCH = Strg("T")
    ALIGN = Strg("J")
    POSITION = Strg("C")
    GOTO = Strg("G")


OPTIONS: list[tuple[str, str]] = [
    (f"^{unStrg(Controls.HELP)}", "Help"),
    (f"^{unStrg(Controls.CLOSE)}", "Close"),
    (f"^{unStrg(Controls.SAVE)}", "Save"),
    (f"^{unStrg(Controls.SEARCH)}", "Search"),
    (f"^{unStrg(Controls.CUT)}", "Cut"),
    (f"^{unStrg(Controls.PASTE)}", "Paste"),
]


class Controls_Alt:
    UNDO = ord("u")
    REDO = ord("e")
