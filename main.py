from game.player import *
from ui.uimanager import UIManager

if __name__ == "__main__":
    UIManager(
        [
            AbsractPlayer(),
            HumanPlayer(),      #JOUEUR 1
            AI5Player()         #JOUEUR 2
        ],
        10  #DIMENSION DE LA GRILLE
    ).run()
