from pathlib import Path


class Buffer:
    def __init__(self):
        self.lines = [bytearray()]

    def load(self, path: Path):
        try:
            # TODO: handle encodings
            with open(path, "r", encoding="utf-8") as f:
                lines_s = [list(line.rstrip("\n")) for line in f.readlines()]
        except IOError | FileNotFoundError:
            # TODO: error message
            lines_s = [""]
        self.lines = lines_s

    def save(self, path: Path):
        pass

    def draw_line(self, row: int, start: int, max_length: int) -> str:
        if row < 0 or row >= len(self.lines):
            return ""
        line:bytearray = self.lines[row]
        if start < 0:
            start = 0
        if start >= len(line):
            return ""
        visible = line[start:start + max_length]
        return visible.decode(errors="ignore")