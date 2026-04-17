import curses
from controls import OPTIONS
from buffer import Buffer
# M-* means Alt+*
# ^*  means Strg+*

TITLE = "nano 0.1.0"
NO_FILE = "new buffer"


class Renderer:
    header_height = 1
    footer_height = 1

    def __init__(self, stdscr: curses.window):
        self.stdscr: curses.window = stdscr
        self.offset_x = 0
        self.offset_y = 0

    def set_offset_by_cursor_position(self, buffer, cursor_x, cursor_y):
        max_y, max_x = self.stdscr.getmaxyx()
        if cursor_y + Renderer.header_height < self.offset_y:
            self.offset_y = cursor_y + Renderer.header_height
        elif (
            cursor_y
            >= self.offset_y + max_y - Renderer.footer_height - Renderer.header_height
        ):
            self.offset_y = cursor_y - max_y + 1 + Renderer.header_height
        if cursor_x < self.offset_x:
            self.offset_x = cursor_x
        elif cursor_x >= self.offset_x + max_x - 1:
            self.offset_x = cursor_x - max_x + 2

    def draw(self, buffer, cursor_x, cursor_y):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.header(self.stdscr, TITLE)
        self.draw_buffer(buffer, h, w)
        self.draw_scrollbar(buffer, h, w)
        self.footer(self.stdscr)
        self.stdscr.move(
            cursor_y - self.offset_y + Renderer.header_height, cursor_x - self.offset_x
        )

        self.stdscr.refresh()

    def draw_buffer(self, buffer, h, w):
        content_width = w - 1 # leave space for scrollbar
        content_height = h - Renderer.header_height - Renderer.footer_height
        for i in range(content_height):
            i = i + Renderer.header_height
            line_index = self.offset_y + i - Renderer.header_height
            text = buffer.draw_line(line_index, self.offset_x, content_width)
            self.stdscr.addstr(i, 0, text)

    def draw_scrollbar(self, buffer, h, w):
        total_lines = len(buffer.lines)
        h = h - Renderer.header_height - Renderer.footer_height
        if total_lines <= h:
            return
        bar_height = max(1, int(h * (h / total_lines)) - Renderer.header_height - Renderer.footer_height)
        scroll_ratio = self.offset_y / (total_lines - h)
        bar_start = int(scroll_ratio * (h - bar_height))
        for i in range(h):
            if bar_start <= i < bar_start + bar_height:
                self.stdscr.addstr(i, w - 1, "█")
            else:
                self.stdscr.addstr(i, w - 1, "│")

    def header(self, stdscr: curses.window, text: str | None = None):
        if text is None:
            text = ""
        row = 0
        _, w = stdscr.getmaxyx()
        col = (w - len(text)) // 2
        stdscr.addstr(row, 0, " " * w, curses.A_REVERSE)
        stdscr.addstr(row, col, text, curses.A_REVERSE)
        stdscr.refresh()

    def footer(self, stdscr: curses.window):
        window_height, window_width = stdscr.getmaxyx()
        col_width = 10
        footer_row = window_height - 1
        x_pos = 0
        for i, (shortcut, label) in enumerate(OPTIONS):
            x_pos = col_width * i
            # assert len(shortcut) + len(label) + 3 < col_width, f"option string too large (> {col_width})"
            stdscr.addstr(footer_row, x_pos, shortcut, curses.A_REVERSE)
            stdscr.addnstr(footer_row, x_pos + len(shortcut), f" {label}  ", 12)
        stdscr.refresh()


def draw_textbox(
    stdscr: curses.window,
    buffer: Buffer,
    rows: tuple[int, int],
    cols: tuple[int, int],
    cursor_pos: tuple[int, int],
):
    row_start, row_end = rows
    col_start, col_end = cols
    for i in range(row_start, row_end + 1):
        display_line = buffer.draw_line(i, col_start, col_end)
        # if i == row: # only if system cursor is unavailable
        #    display_line = display_line[: col] + "|" + display_line[col:]
        stdscr.addstr(i, 0, display_line)


def main():
    def launch(stdscr):
        curses.curs_set(True)
        stdscr.keypad(True)
        curses.noecho()
        stdscr.clear()
        r = Renderer(stdscr)
        try:
            r.header(stdscr, TITLE)
            r.footer(stdscr)
        except curses.error as e:
            print("curses", e)
        except Exception as e:
            print("Exception", e)
        stdscr.move(0, 0)
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(launch)


if __name__ == "__main__":
    main()
