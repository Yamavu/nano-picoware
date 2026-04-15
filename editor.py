
from pathlib import Path
import curses

from cursor import Cursor
from controls import Controls
from buffer import Buffer

class Editor:
    def __init__(self, lines_s: list[str]):
        self.cursor = Cursor(0, 0)
        self.controls = Controls()
        self.keymap_cursor = {
            self.controls.left: self.cursor.move_left,
            self.controls.right: self.cursor.move_right,
            self.controls.up: self.cursor.move_down,
            self.controls.down: self.cursor.move_down,
        }
        self.keymap = {
            self.controls.qkey: self.quit,
            self.controls.skey: self.save_file,
            self.controls.enterkey: self.newline,
            self.controls.bspkey: self.backspace,
        }
        if lines_s is None:
            self.lines_s = [""]
        self.lines_s = lines_s

    def quit():
        pass

    

    def handle_key(self, key):
        if key in self.keymap_cursor:
            self.keymap_cursor[key](self.lines_s)
        if key in self.keymap:
                self.keymap[key]()
        elif 32 <= key <= 126:
            self.buffer.insert_char(self.cursor.col, self.cursor.row, key)
        else:
            raise ValueError(key)

    def draw(self, stdscr: curses.window):
        stdscr.clear()
        cursor = self.cursor
        for i, line in enumerate(self.lines_s):
            line_str = "".join(line)
            if i == cursor.row:
                display_line = line_str[: cursor.col] + "|" + line_str[cursor.col :]
            else:
                display_line = line_str
            stdscr.addstr(i, 0, f"{i + 1} | {display_line}")
        stdscr.move(cursor.row, cursor.col)
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