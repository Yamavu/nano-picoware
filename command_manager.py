class CommandManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command, editor):
        command.execute(editor)
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self, editor):
        if self.undo_stack:
            cmd = self.undo_stack.pop()
            cmd.undo(editor)
            self.redo_stack.append(cmd)

    def redo(self, editor):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute(editor)
            self.undo_stack.append(cmd)