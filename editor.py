
from pathlib import Path
import curses

from cursor import Cursor
from controls import Controls
from buffer import Buffer
from command_manager import CommandManager
from command import Newline, Backspace, InsertChar

class Editor:
    def __init__(self):
        self.cursor = Cursor(0, 0)
        self.buffer = Buffer()
        self.commands = CommandManager()

        self.keymap_buffer = {
            Controls.LEFT: self.cursor.move_left,
            Controls.RIGHT: self.cursor.move_right,
            Controls.UP: self.cursor.move_down,
            Controls.DOWN: self.cursor.move_down,
        }
        self.keymap_cursor = {
            Controls.ENTERKEY: Newline,
            Controls.BSPKEY: Backspace,
        }
        self.keymap = {
            #Controls.qkey: self.quit,
            #Controls.skey: self.save_file,
        }
    def quit():
        pass

    def handle_key(self, key):
        if key in self.keymap_buffer:
            self.keymap_buffer[key](self.buffer.lines)
        elif key in self.keymap_cursor:
            self.cursor = self.commands.execute
            self.keymap_cursor[key](self.cursor)
        elif key in self.keymap:
                self.keymap[key]()
        elif 32 <= key <= 126:
            self.cursor = self.commands.execute(InsertChar(chr(key)),self)
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
            for line in self.buffer.lines:
                f.write("".join(line) + "\n")

    @staticmethod
    def load_file(filename: Path) -> list[str]:
        