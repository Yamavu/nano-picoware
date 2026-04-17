from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import curses

from editor import Editor



def main(stdscr, filename: Optional[Path]):
    curses.curs_set(True) # use system cursor
    curses.noecho()
    curses.cbreak()
    #stdscr.keypad()
    editor = Editor(stdscr)
    if filename is not None and filename.exists():
        editor.load_file(filename)
    try:
        while editor.running:
            editor.renderer.draw(editor.buffer, cursor_y=editor.cursor.row, cursor_x=editor.cursor.col)
            key = stdscr.getch()
            editor.handle_key(key)
    finally:
        curses.cbreak(False)
        curses.echo()


if __name__ == "__main__":
    filename: Optional[Path] = None
    p = ArgumentParser()
    p.add_argument("filename", type=Path, nargs="?")
    args = p.parse_args()
    print(args.filename)
    curses.wrapper(main, args.filename)
