from game.player import *
from ui.uimanager import UIManager

if __name__ == "__main__":
    UIManager([AbsractPlayer(0), AI5Player(1), AI4Player(2)], 9).run()
