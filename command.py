from editor import Editor


class Command:
    def execute(self, editor: Editor):
        raise NotImplementedError()

    def undo(self, editor: Editor):
        raise NotImplementedError()


class InsertChar(Command):
    def __init__(self, char):
        self.char = char
        self.pos = None

    def execute(self, editor: Editor):
        col, row = editor.cursor.pos
        self.pos = (row, col)
        editor.cursor = editor.buffer.lines[row].insert(col, ord(self.char))

    def undo(self, editor: Editor):
        if self.pos is None:
            raise ValueError("invalid pos in InsertChar")
        col, row = self.pos
        editor.buffer.lines[row].pop(col)
        editor.cursor.row = row
        editor.cursor.col = col

class Backspace(Command):
    def __init__(self) -> None:
        self.deleted = None
        self.pos = None
        self.merge = False

    def execute(self, editor: Editor):
        col, row = editor.cursor.pos

        if col > 0:
            self.deleted = editor.buffer.lines[row][col-1]
            self.pos = (col-1, row)
        elif row > 0:
            self.merge = True
            prev_len = len(editor.buffer.lines[row-1])
            editor.buffer.lines[row-1].extend(editor.buffer.lines[row])
            del editor.buffer.lines[row]
            self.pos = (col, row)
            editor.cursor.col = prev_len
            editor.cursor.row -= 1

        
     def undo(self, editor):
        row, col = self.pos

        if row > 0:
            self.deleted = editor.buffer.lines[col][row-1]
            self.pos = (row-1, col)
            del editor.buffer.lines[col][row-1]
            editor.cursor.col -= 1

        elif col > 0:
            self.merge = True
            self.pos = (row, col)

            prev_len = len(editor.buffer.lines[col-1])
            editor.buffer.lines[col-1].extend(editor.buffer.lines[col])
            del editor.buffer.lines[col]

            editor.cursor.col = prev_len
            editor.cursor.row -= 1

class Newline(Command):
    def __init__(self) -> None:
        self.pos = None
    def execute(self, editor: Editor):
        self.pos = editor.cursor.pos
        editor.cursor = editor.buffer.newline(editor.cursor)
    def undo(self, editor: Editor):
        col, row = editor.cursor.pos
        editor.buffer.lines[row].extend(editor.buffer.lines[row+1])
        del editor.buffer.lines[row+1]
