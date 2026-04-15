from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import curses

from editor import Editor

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
