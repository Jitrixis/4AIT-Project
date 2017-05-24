import random

from game.board import VirtualBoard
from ui.uiutils import UIUtils


class AbsractPlayer():
    def __init__(self, player):
        self._player = player

    def get_player(self):
        return self._player

    def run(self, semaphore_event, board):
        pass


class HumanPlayer(AbsractPlayer):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        if semaphore_event is not None:
            board.play(semaphore_event)


class AI1Player(AbsractPlayer):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        l = self._pos_of(self._available_square(board))
        board.play(random.choice(l))

    def _available_square(self, board):
        return [square for row in board.get_squares() for square in row if not square]

    def _pos_of(self, squares):
        lines = []
        for square in squares:
            lines += [line.get_pos() for line in square.get_lines() if not line]
        lines = set(lines)
        return list(lines)


class AI2Player(AI1Player):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        l = self._pos_of(self._priority_square(board))
        if len(l) == 0:
            l = self._pos_of(self._available_square(board))
        board.play(random.choice(l))

    def _priority_square(self, board):
        return [square for row in board.get_squares() for square in row if len(square) == 3]


class AI3Player(AI2Player):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        l = self._pos_of(self._priority_square(board))
        if len(l) == 0:
            d = self._pos_of(self._dangerous_square(board))
            a = self._pos_of(self._available_square(board))
            l = [line for line in a if line not in d]
        if len(l) == 0:
            l = self._pos_of(self._available_square(board))
        board.play(random.choice(l))

    def _dangerous_square(self, board):
        return [square for row in board.get_squares() for square in row if len(square) == 2]


class AI4Player(AI3Player):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        l = self._pos_of(self._priority_square(board))
        if len(l) == 0:
            d = self._pos_of(self._dangerous_square(board))
            a = self._pos_of(self._available_square(board))
            l = [line for line in a if line not in d]
        if len(l) == 0:
            e = self._count_effect(board)
            if len(e):
                l = [p for f in min(e, key=len) for p in f]
        if len(l) == 0:
            l = self._pos_of(self._available_square(board))
        board.play(random.choice(l))

    def _count_effect(self, board):
        pairs = [[tuple(line.get_pos() for line in square.get_lines() if not line)] for square in
                 self._dangerous_square(board)]
        changed = True
        while changed:
            changed = False
            for i in range(len(pairs) - 1):
                for j in range(i + 1, len(pairs)):
                    if bool(set(p for e in pairs[i] for p in e) & set(p for e in pairs[j] for p in e)):
                        pairs[i] += pairs[j]
                        pairs[j] = []
                        changed = True
        pairs = [e for e in pairs if len(e)]
        return pairs


class AI5Player(AI4Player):
    def __init__(self, player):
        super().__init__(player)

    def run(self, semaphore_event, board):
        d = self._pos_of(self._dangerous_square(board))
        a = self._pos_of(self._available_square(board))
        e = self._count_effect(board)
        o = self._pos_of(self._priority_square(board))
        l = []
        if len(l) == 0:
            l = o
            if len(l) > 0:
                ef = self._count_effect(board)
                if len(ef) > 0 and not len([line for line in a if line not in d]):
                    mef = []
                    oef = []
                    for pef in ef:
                        if bool(set(p for sq in pef for p in sq) & set(l)):
                            mef.append(pef)
                        else:
                            oef.append(pef)
                    if len(mef) == 1:
                        if len(mef[0]) == 1:
                            if len(oef) % board.get_num_player():
                                l = [p for p in mef[0][0] if p not in l]
        if len(l) == 0:
            l = [line for line in a if line not in d]
        if len(l) == 0:
            if len(e):
                l = [p for f in min(e, key=len) for p in f]
        if len(l) == 0:
            l = self._pos_of(self._available_square(board))
        board.play(random.choice(l))


class Developer(AbsractPlayer):
    def __init__(self, cls):
        super().__init__(cls.get_player())
        self.__cls_player = cls
        self.__want = None

    def run(self, semaphore_event, board):
        if self.__want is None:
            v = VirtualBoard(board)
            self.__cls_player.run(None, v)
            self.__want = v.get_last_play()
        else:
            UIUtils.debug_line(self.__want)
        if type(semaphore_event) is tuple:
            board.play(semaphore_event)
            self.__want = None
        elif semaphore_event == 'N':
            board.play(self.__want)
            self.__want = None
