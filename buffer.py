from cursor import Cursor

class Buffer:
    def __init__(self):
        self.lines = [""]

    def insert_char(self, col, row, char):
        line = self.lines[row]
        self.lines[row] = line[:col] + char + line[col:]
        return col + 1, row

    def newline(self, col, row):
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row + 1, line[col:])
        return 0, row + 1

    def draw(self, start_col, start_row):
        pass

    def backspace(self, x, y):
        if x > 0:
            line = self.lines[y]
            self.lines[y] = line[:x - 1] + line[x:]
            return x - 1, y
        elif y > 0:
            prev_len = len(self.lines[y - 1])
            self.lines[y - 1] += self.lines[y]
            del self.lines[y]
            return prev_len, y - 1
        return x, y
    