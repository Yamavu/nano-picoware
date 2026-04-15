
from pathlib import Path
import curses

from cursor import Cursor
from controls import Controls
from buffer import Buffer

class Editor:
    def __init__(self, lines: list[str]):
        self.cursor = Cursor(0, 0)
        self.controls = Controls()
        self.buffer = Buffer()
        if lines is not None:
            self.buffer.lines = lines
        self.keymap_buffer = {
            self.controls.left: self.cursor.move_left,
            self.controls.right: self.cursor.move_right,
            self.controls.up: self.cursor.move_down,
            self.controls.down: self.cursor.move_down,
        }
        self.keymap_cursor = {
            self.controls.enterkey: self.buffer.newline,
            self.controls.bspkey: self.buffer.backspace,
        }
        self.keymap = {
            #self.controls.qkey: self.quit,
            #self.controls.skey: self.save_file,
        }
    def quit():
        pass

    def handle_key(self, key):
        if key in self.keymap_buffer:
            self.keymap_buffer[key](self.lines_s)
        elif key in self.keymap_cursor:
            self.keymap_cursor[key](self.cursor)
        elif key in self.keymap:
                self.keymap[key]()
        elif 32 <= key <= 126:
            self.cursor = self.buffer.insert_char(self.cursor, chr(key))
        else:
            raise ValueError(key)

    def draw(self, stdscr: curses.window):
        # start_col, start_row # upper left corner of the displayed data
        stdscr.clear()
        col, row = self.cursor.pos
        for i, line in enumerate(self.buffer.lines):
            if i > curses.LINES:
                break
            display_line = "".join(line[0:curses.COLS])
            #if i == row: # only if system cursor is unavailable
            #    display_line = display_line[: col] + "|" + display_line[col:] 
            stdscr.addstr(i, 0, display_line)
        stdscr.move(row, col) # mmove cursor position
        stdscr.refresh()

    def save_file(self, filename):
        with open(filename, "w") as f:
            for line in self.lines_s:
                f.write("".join(line) + "\n")

    @staticmethod
    def load_file(filename: Path) -> list[str]:
        try:
            # TODO: handle encodings
            with open(filename, "r", encoding="utf-8") as f:
                lines_s = [list(line.rstrip("\n")) for line in f.readlines()]
        except IOError | FileNotFoundError:
            # TODO: error message
            lines_s = [""]
        return lines_s