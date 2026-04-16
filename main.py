from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import curses

from editor import Editor



def main(stdscr, filename: Optional[Path]):
    curses.curs_set(True) # use system cursor
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
    try:
        while True:
            editor.draw(stdscr)
            key = stdscr.getch()
            editor.handle_key(key)
    finally:
        curses.cbreak(False)


if __name__ == "__main__":
    filename: Optional[Path] = None
    p = ArgumentParser()
    p.add_argument("filename", type=Path, nargs="?")
    args = p.parse_args()
    print(args.filename)
    curses.wrapper(main, args.filename)
