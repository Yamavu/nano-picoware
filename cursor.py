

class Cursor:
    def __init__(self, row: int, col: int):
        if row is None:
            row = 0
        if col is None:
            col = 0
        self.row:int = row
        self.col:int = col

    @property
    def pos(self) -> tuple[int, int]:
        return (self.col, self.row)

    