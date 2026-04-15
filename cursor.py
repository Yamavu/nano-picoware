class Cursor:
    def __init__(self, row: int | None, col: int | None):
        self.row = row
        self.col = col

    def move_left(self, lines_s):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(lines_s[self.row])

    def move_right(self, lines_s):
        if self.col < len(lines_s[self.row]):
            self.col += 1
        elif self.row < len(lines_s) - 1:
            self.row += 1
            self.col = 0

    def move_up(self, lines_s):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.col, len(lines_s[self.row]))

    def move_down(self, lines_s):
        if self.row < len(lines_s) - 1:
            self.row += 1
            self.col = min(self.col, len(lines_s[self.row]))