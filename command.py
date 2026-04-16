class Command:
    def execute(self, editor):
        raise NotImplementedError()

    def undo(self, editor):
        raise NotImplementedError()


class InsertChar(Command):
    def __init__(self, char):
        self.char = char
        self.pos = None

    def execute(self, editor):
        col, row = editor.cursor.pos
        self.pos = (row, col)
        editor.buffer.lines[row].insert(col, ord(self.char))
        editor.cursor.col += 1

    def undo(self, editor):
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

    def execute(self, editor):
        col, row = editor.cursor.pos

        if col > 0:
            self.deleted = editor.buffer.lines[row][col - 1]
            self.pos = (col - 1, row)
        elif row > 0:
            self.merge = True
            prev_len = len(editor.buffer.lines[row - 1])
            editor.buffer.lines[row - 1].extend(editor.buffer.lines[row])
            del editor.buffer.lines[row]
            self.pos = (col, row)
            editor.cursor.col = prev_len
            editor.cursor.row -= 1

    def undo(self, editor):
        row, col = self.pos

        if row > 0:
            self.deleted = editor.buffer.lines[col][row - 1]
            self.pos = (row - 1, col)
            del editor.buffer.lines[col][row - 1]
            editor.cursor.col -= 1

        elif col > 0:
            self.merge = True
            self.pos = (row, col)

            prev_len = len(editor.buffer.lines[col - 1])
            editor.buffer.lines[col - 1].extend(editor.buffer.lines[col])
            del editor.buffer.lines[col]

            editor.cursor.col = prev_len
            editor.cursor.row -= 1


class Newline(Command):
    def __init__(self) -> None:
        self.pos = None

    def execute(self, editor):
        self.pos = editor.cursor.pos
        editor.buffer.lines.append(bytearray())
        editor.cursor.col = 0
        editor.cursor.row += 1

    def undo(self, editor):
        col, row = editor.cursor.pos
        editor.buffer.lines[row].extend(editor.buffer.lines[row + 1])
        del editor.buffer.lines[row + 1]


class MoveLeft(Command):
    def __init__(self):
        pass

    def execute(self, editor):
        if editor.cursor.col > 0:
            editor.cursor.col -= 1
        elif editor.cursor.row > 0:
            editor.cursor.row -= 1
            editor.cursor.col = len(editor.buffer.lines[editor.cursor.row])

    def undo(self, editor):
        MoveRight().execute(editor)


class MoveRight(Command):
    def __init__(self):
        pass

    def execute(self, editor):
        # def move_right(self, lines_s):
        if editor.cursor.col < len(editor.buffer.lines[editor.cursor.row]):
            editor.cursor.col += 1
        elif editor.cursor.row < len(editor.buffer.lines[editor.cursor.row]) - 1:
            editor.cursor.row += 1
            editor.cursor.col = 0

    def undo(self, editor):
        MoveLeft().execute(editor)


class MoveUp(Command):
    def __init__(self):
        pass

    def execute(self, editor):
        if editor.cursor.row > 0:
            editor.cursor.row -= 1
            editor.cursor.col = min(
                editor.cursor.col, len(editor.buffer.lines[editor.cursor.row])
            )

    def undo(self, editor):
        MoveUp().execute()


class MoveDown(Command):
    def __init__(self):
        pass

    def execute(self, editor):
        if editor.cursor.row < len(editor.buffer.lines[editor.cursor.row]) - 1:
            editor.cursor.row += 1
            editor.cursor.col = min(editor.cursor.col, len(editor.buffer.lines[editor.cursor.row]))

    def undo(self, editor):
        MoveDown().execute()
