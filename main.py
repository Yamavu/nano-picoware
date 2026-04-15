from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import curses


TITLE = "nano 0.0.1"
NO_FILE = "new buffer"

ALT_CODES = {
    "G":  "Help",
    "X":  "Close",
    "O":  "Save",
    "R":  "Read",
    "W":  "Search",
    "\\": "Replace",
    "K":  "Cut",
    "U":  "Paste",
    "T":  "Launch",
    "J":  "Align",
    "C":  "Position",
    "/":  "Goto"
}


class Cursor:
    def __init__(self, row: int | None, col: int | None):
        self.row = row
        self.col = col

    def move_left(self, lines_s):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(lines_s[self.row])

    def move_right(self, lines_s):
        if self.col < len(lines_s[self.row]):
            self.col += 1
        elif self.row < len(lines_s) - 1:
            self.row += 1
            self.col = 0

    def move_up(self, lines_s):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.col, len(lines_s[self.row]))

    def move_down(self, lines_s):
        if self.row < len(lines_s) - 1:
            self.row += 1
            self.col = min(self.col, len(lines_s[self.row]))


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

    def load_file(self, config: Path):
        pass

    def save_file(self, config: Path):
        pass


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
            self.controls.ikey: self.toggle_mode,
            self.controls.qkey: self.quit,
            self.controls.skey: self.save_file,
            self.controls.enterkey: self.newline,
            self.controls.bspkey: self.backspace,
            self.controls.esckey: self.toggle_mode,
            self.controls.bspkey: self.backspace,
        }
        if lines_s is None:
            self.lines_s = [""]
        self.lines_s = lines_s

    def toggle_mode(self):
        self.insert = not self.insert

    def quit():
        pass

    def newline(self):
        cursor = self.cursor
        line = self.lines_s[cursor.row]
        new_line = line[cursor.col :]  # split after cursor
        self.lines_s[cursor.row] = line[: cursor.col]
        self.lines_s.insert(cursor.row + 1, new_line)
        self.cursor.row += 1
        self.cursor.col = 0

    def backspace(self):
        cursor = self.cursor
        if cursor.col > 0:
            # remove character before cursor
            self.lines_s[cursor["row"]].pop(cursor["col"] - 1)
            cursor["col"] -= 1
        elif cursor.row > 0:
            # merge with previous line
            prev_len = len(self.lines_s[cursor["row"] - 1])
            self.lines_s[cursor["row"] - 1].extend(self.lines_s[cursor["row"]])
            self.lines_s.pop(cursor["row"])
            cursor["row"] -= 1
            cursor["col"] = prev_len

    def insert_char(self, key: int):
        self.lines_s[self.cursor.row].insert(self.cursor.col, chr(key))
        self.cursor.col += 1

    def handle_key(self, key):
        if key in self.keymap_cursor:
            self.keymap_cursor[key](self.lines_s)
        if not self.insert:
            if key in self.keymap:
                self.keymap[key]()
        if key in self.keymap_insert:
            self.keymap[key]()
        elif 32 <= key <= 126:
            self.insert_char(key)

    def draw(self, stdscr):
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


def main(stdscr, filename: Optional[Path]):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    if filename is not None and filename.exists():
        lines_s = Editor.load_file(filename)
    else:
        lines_s = [[]]
    editor = Editor(
        lines_s,
    )
    while True:
        editor.draw(stdscr)
        key = stdscr.getch()
        editor.handle_key(key)


if __name__ == "__main__":
    filename: Optional[Path] = None
    p = ArgumentParser()
    p.add_argument("filename", type=Path, nargs="?")
    args = p.parse_args()
    print(args.filename)
    curses.wrapper(main, args.filename)
