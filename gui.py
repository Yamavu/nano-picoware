import curses
from controls import OPTIONS
from buffer import Buffer
# M-* means Alt+*
# ^*  means Strg+*

TITLE = "nano 0.1.0"
NO_FILE = "new buffer"

def header(stdscr: curses.window, text:str | None = None):
    if text is None:
        text = ""
    row = 0
    _, w = stdscr.getmaxyx()
    col = (w - len(text)) // 2
    stdscr.addstr(row, 0, " "*w, curses.A_REVERSE)
    stdscr.addstr(row, col, text, curses.A_REVERSE)
    stdscr.refresh()


def footer(stdscr: curses.window):
    window_height, window_width = stdscr.getmaxyx()
    col_width = 10
    footer_row = window_height - 1
    x_pos = 0
    for i, (shortcut, label) in enumerate(OPTIONS):
        x_pos = col_width * i
        #assert len(shortcut) + len(label) + 3 < col_width, f"option string too large (> {col_width})"
        stdscr.addstr(footer_row, x_pos, shortcut, curses.A_REVERSE)
        stdscr.addnstr(footer_row, x_pos + len(shortcut) , f" {label}  ", 12)
    stdscr.refresh()

def draw_textbox(stdscr: curses.window, buffer: Buffer, rows: tuple[int,int], cols:tuple[int,int], cursor_pos: tuple[int,int]):
    row_start, row_end = rows
    col_start, col_end = cols
    for i in range(row_start, row_end+1):
        display_line = buffer.draw_line(i, col_start, col_end)
        #if i == row: # only if system cursor is unavailable
        #    display_line = display_line[: col] + "|" + display_line[col:] 
        stdscr.addstr(i, 0, display_line)

def main():
    def launch(stdscr):
        curses.curs_set(True)
        stdscr.keypad(True)
        curses.noecho()
        stdscr.clear()
        try:
            header(stdscr, TITLE)
            footer(stdscr)
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
