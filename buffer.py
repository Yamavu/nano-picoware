from pathlib import Path
from collections.abc import Iterator

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

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, row: int) -> bytearray:
        if row >= len(self):
            raise IndexError(f"no line nr {row}")
        return self.lines[row]

    def __iter__(self) -> Iterator[bytearray]:
        for line in self.lines:
            yield line

    def enumerate_lines(self) -> Iterator[tuple[int,bytearray]]:
        for i, line in enumerate(self.lines):
            yield i, line
    
    def append(self, line: bytearray):
        self.lines.append(line.encode(encoding="utf-8"))

    def save(self, path: Path):
        pass

    def draw_line(self, row: int, start: int, max_length: int) -> str:
        if row < 0 or row >= len(self.lines):
            return ""
        line:bytearray = self[row]
        if start < 0:
            start = 0
        if start >= len(line):
            return ""
        visible = line[start:start + max_length]
        return visible.decode(errors="ignore")

