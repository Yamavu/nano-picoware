import curses

def main(stdscr):
    # Clear screen and hide the cursor
    curses.curs_set(0)
    stdscr.clear()
    stdscr.keypad(True)

    stdscr.addstr(0, 0, "Press any key combination (e.g., Ctrl+X):")
    stdscr.refresh()
    stdscr.nodelay(False)

    # Get the input key code
    key = stdscr.getch()

    # Clear screen for result
    stdscr.clear()

    # Logic to identify Control sequences
    # ASCII 1-26 represent Ctrl+A through Ctrl+Z
    if 1 <= key <= 26:
        char = chr(key + 64)  # Convert back to uppercase letter
        result = f"Ctrl+{char}"
    elif key == 27:
        result = "Escape"
        stdscr.timeout(100)
        next_key = stdscr.getch()
        if next_key != -1:
            # If a key followed ESC immediately, it's likely an Alt combo
            result = f"Alt+{chr(next_key).upper()}"
        else:
            result = "Escape"

    else:
        try:
            result = chr(key)
        except ValueError:
            result = f"Special Key (Code: {key})"

    stdscr.addstr(0, 0, f"You pressed: {result}")
    stdscr.addstr(1, 0, "Press any key to exit...")
    stdscr.refresh()
    
    # Wait for one more press so the user can see the result
    stdscr.getch()
    return result, key

if __name__ == "__main__":
    # wrapper initializes curses and ensures terminal settings 
    # are restored even if the script crashes.
    result,key = curses.wrapper(main)
    print(result, key)