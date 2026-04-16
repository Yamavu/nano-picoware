import curses
import math
from controls import CONTROLS_STRG, CONTROLS_ALT
# M-* means Alt+*
# ^*  means Strg+*

ALT_CODES = {
    f"^{chr(CONTROLS_STRG.HELP + 64)}": "Help",
    f"^{chr(CONTROLS_STRG.CLOSE + 64)}": "Close",
    f"^{chr(CONTROLS_STRG.SAVE + 64)}": "Save",
    f"^{chr(CONTROLS_STRG.READ + 64)}": "Read",  # Insert a file into current one
    f"^{chr(CONTROLS_STRG.SEARCH + 64)}": "Search",
    f"^{chr(CONTROLS_STRG.REPLACE + 64)}": "Replace",
    f"^{chr(CONTROLS_STRG.CUT + 64)}": "Cut",
    f"^{chr(CONTROLS_STRG.PASTE + 64)}": "Paste",
    f"^{chr(CONTROLS_STRG.LAUNCH + 64)}": "Launch",
    f"^{chr(CONTROLS_STRG.ALIGN + 64)}": "Align",
    f"^{chr(CONTROLS_STRG.POSITION + 64)}": "Position",
    f"^{chr(CONTROLS_STRG.GOTO + 64)}": "Goto",
    f"M-{chr(CONTROLS_ALT.UNDO).upper()}": "Undo",
    f"M-{chr(CONTROLS_ALT.REDO).upper()}": "Redo",
}


def print_controls(stdscr: curses.window, codes: dict[str, str]):
    rows = 2
    items = [["" for _ in range(math.floor(len(codes) / rows))]] * 2
    for i, (k, v) in enumerate(codes.items()):
        col = math.floor(i / 2)
        row = i % rows
        items[row][col] = f"{k:<3}{v:>8}"
    print(items)


print_controls(None, ALT_CODES)
