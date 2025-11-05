# main.py

import sys
from gui import GameGUI

if __name__ == '__main__':
    try:
        game_gui = GameGUI()
        game_gui.run()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit()