
from pathlib import Path
import curses

from cursor import Cursor
from controls import Controls
from buffer import Buffer
from command_manager import CommandManager
from command import Newline, Backspace, InsertChar, MoveDown, MoveLeft, MoveRight, MoveUp, Quit
from gui import Renderer, TITLE

class Editor:
    def __init__(self, stdscr: curses.window):
        self.running = True
        self.buffer = Buffer()
        self.cursor = Cursor(0, 0)
        self.commands = CommandManager()
        self.renderer = Renderer(stdscr)

        self.keymap = {
            Controls.LEFT: MoveLeft,
            Controls.RIGHT: MoveRight,
            Controls.UP: MoveUp,
            Controls.DOWN: MoveDown,
            Controls.ENTERKEY: Newline,
            Controls.BSPKEY: Backspace,
            Controls.CLOSE: Quit
            #Controls.qkey: self.quit,
            #Controls.skey: self.save_file,
        }

    def handle_key(self, key):
        if key in self.keymap:
            self.keymap[key]().execute(self)
        elif 32 <= key <= 126:
            self.commands.execute(InsertChar(chr(key)), self)
        else:
            raise ValueError(key)

    def quit(self):
        self.running = False
        del self.buffer
        del self.cursor
        del self.commands
        del self.keymap


    def draw(self, stdscr: curses.window):
        # start_col, start_row # upper left corner of the displayed data
        stdscr.clear()
        if self.cursor is None:
            raise ValueError("Why is cursor None?")
        col, row = self.cursor.pos
        max_rows, max_cols = stdscr.getmaxyx()
        self.renderer.header(stdscr ,TITLE)
        for i, line in enumerate(self.buffer.lines):
            if i > max_rows-3:
                break
            display_line = self.buffer.draw_line(i, 0, max_cols)
            #if i == row: # only if system cursor is unavailable
            #    display_line = display_line[: col] + "|" + display_line[col:] 
            stdscr.addstr(i, 0, display_line)
        self.renderer.footer(stdscr)
        stdscr.move(row, col) # move cursor position   
        stdscr.refresh()

    def save_file(self, filename):
        self.buffer.save(filename)
        
    def load_file(self, filename: Path):
        self.buffer.load(filename)
