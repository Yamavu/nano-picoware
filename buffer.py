from cursor import Cursor
import curses

class Buffer:
    def __init__(self):
        self.lines: list[list[str]] = [[]]

    def insert_char(self, cursor:Cursor, char:str) -> Cursor:
        col, row = cursor.pos
        line = self.lines[row]
        self.lines[row] = line[:col] + [char] + line[col:]
        cursor.col += 1
        return cursor

    def newline(self, cursor:Cursor) -> Cursor:
        col, row = cursor.pos
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row + 1, line[col:])
        cursor.row += 1
        cursor.col = 0
        return cursor

    def backspace(self, cursor: Cursor):
        col, row = cursor.pos
        if col > 0:
            line = self.lines[row]
            self.lines[row] = line[:col - 1] + line[col:]
            cursor.col -= 1
        elif row > 0:
            prev_len = len(self.lines[row - 1])
            self.lines[row - 1] += self.lines[row]
            del self.lines[row]
            cursor.col = prev_len
            cursor.row -= 1
        return cursor
    