import curses
import math
from controls import CONTROLS_STRG
# M-* means Alt+*
# ^*  means Strg+*

TITLE = "nano 0.1.0"
NO_FILE = "new buffer"

def print_header(stdscr: curses.window, text:str | None = None):
    if text is None:
        text = ""
    row = 0
    _, w = stdscr.getmaxyx()
    col = (w - len(text)) // 2
    stdscr.addstr(row, 0, " "*w, curses.A_REVERSE)
    stdscr.addstr(row, col, text, curses.A_REVERSE)
    stdscr.refresh()


def print_footer(stdscr: curses.window):
    options:list[tuple[str, str]] = [
        (f"^{chr(CONTROLS_STRG.HELP + 64)}", "Help"),
        (f"^{chr(CONTROLS_STRG.CLOSE + 64)}", "Close"),
        (f"^{chr(CONTROLS_STRG.SAVE + 64)}", "Save"),
        (f"^{chr(CONTROLS_STRG.SEARCH + 64)}", "Search"),
        (f"^{chr(CONTROLS_STRG.CUT + 64)}", "Cut"),
        (f"^{chr(CONTROLS_STRG.PASTE + 64)}", "Paste")
    ]
    window_height, window_width = stdscr.getmaxyx()
    col_width = 10
    footer_row = window_height - 1
    x_pos = 0
    for i, (shortcut, label) in enumerate(options):
        x_pos = col_width * i
        #assert len(shortcut) + len(label) + 3 < col_width, f"option string too large (> {col_width})"
        stdscr.addstr(footer_row, x_pos, shortcut, curses.A_REVERSE)
        stdscr.addnstr(footer_row, x_pos + len(shortcut) , f" {label}  ", 12)
    stdscr.refresh()

def main():
    def launch(stdscr):
        curses.curs_set(True)
        stdscr.keypad(True)
        curses.noecho()
        stdscr.clear()
        try:
            print_header(stdscr, TITLE)
            print_footer(stdscr)
        except curses.error as e:
            print("curses", e)
        except Exception as e:
            print("Exception", e)
        stdscr.move(0,0)
        stdscr.refresh()
        stdscr.getch()
        
    curses.wrapper(launch)

if __name__ == "__main__":
    main()
