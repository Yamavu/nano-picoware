import curses

class Controls:
    def __init__(self):
        self.left = curses.KEY_LEFT
        self.right = curses.KEY_RIGHT
        self.up = curses.KEY_UP
        self.down = curses.KEY_DOWN
        self.ikey = ord("i")
        self.qkey = ord("q")
        self.skey = ord("s")
        self.esckey = 27
        self.bspkey = curses.KEY_BACKSPACE
        self.enterkey = 10
