import curses

ALT_CODES = {
    "G":  "Help", 
    "X":  "Close",
    "O":  "Save",
    "R":  "Read", # Insert a file into current one
    "W":  "Search", 
    "\\": "Replace",
    "K":  "Cut",
    "U":  "Paste",
    "T":  "Launch",
    "J":  "Align",
    "C":  "Position",
    "/":  "Goto"
}

def print_controlls(stdscr, codes: dict[str,str]):
    pass
