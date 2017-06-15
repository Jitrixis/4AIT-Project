class Board:
    def __init__(self, size=5, num_player=2):
        self.__size = size
        self.__num_player = num_player if num_player >= 2 else 2
        self.__cur_player = 1
        self.__lines = [[Line((j, i)) for i in range(self.__size + j % 2)] for j in range(self.__size * 2 + 1)]
        self.__squares = [[Square(
            [self.__lines[j * 2][i],
             self.__lines[j * 2 + 1][i],
             self.__lines[j * 2 + 1][i + 1],
             self.__lines[j * 2 + 2][i]],
            (j, i)) for i in range(self.__size)] for j in range(self.__size)]

    def get_size(self):
        return self.__size

    def get_lines(self):
        return self.__lines

    def get_squares(self):
        return self.__squares

    def get_num_player(self):
        return self.__num_player

    def get_cur_player(self):
        return self.__cur_player

    def get_score(self):
        r = [int(square) for row in self.__squares for square in row]
        return {player: r.count(player) for player in set(r)}

    def play(self, key):
        try:
            x, y = key
            self.__lines[x][y].set_player(self.__cur_player)
            self.__next_player()
        except LineException as e:
            raise e
        except:
            raise Exception('Wrong coordinate')

    def __next_player(self):
        if len([square for row in self.__squares for square in row if square.is_new()]) == 0:
            self.__cur_player = (self.__cur_player % self.__num_player) + 1

    def __bool__(self):
        return len([square for row in self.__squares for square in row if not square]) == 0

    def __int__(self):
        if not self:
            return 0
        score = self.get_score()
        return max(score, key=score.get)


class Square:
    def __init__(self, lines, pos):
        self.__pos = pos
        self.__lines = lines

    def get_pos(self):
        return self.__pos

    def get_lines(self):
        return self.__lines

    def is_new(self):
        return len([line for line in self.__lines if line.is_last()]) == 1 and self

    def __bool__(self):
        return len([line for line in self.__lines if not line]) == 0

    def __int__(self):
        return int(max(self.__lines))

    def __len__(self):
        return len([line for line in self.__lines if line])


class Line:
    ORDER_SEG = 0

    def __init__(self, pos):
        self.__pos = pos
        self.__order = 0
        self.__player = 0

    def get_pos(self):
        return self.__pos

    def get_order(self):
        return self.__order

    def get_player(self):
        return self.__player

    def set_player(self, player, order=None, force=False):
        if self and not force:
            raise LineException('Already chosen')
        self.__player = player
        if order is not None:
            self.__order = order
        else:
            Line.ORDER_SEG += 1
            self.__order = Line.ORDER_SEG
        return self

    def is_last(self):
        return self.__order == Line.ORDER_SEG

    def __int__(self):
        return self.__player

    def __bool__(self):
        return self.__player != 0

    def __eq__(self, other):
        return self.__player == other

    def __lt__(self, other):
        if not self:
            return False
        if not other:
            return True
        return self.get_order() < other.get_order()


class LineException(Exception):
    pass


class VirtualBoard(Board):
    def __init__(self, board):
        super().__init__(board.get_size(), board.get_num_player())
        self.__last_play = None
        self.__virtual_player = None
        self.__copy(board)

    def get_last_play(self):
        return self.__last_play

    def play(self, key):
        try:
            self.__revoke()
            x, y = key
            self.get_lines()[x][y].set_player(self.__virtual_player, order=Line.ORDER_SEG + 1)
            self.__last_play = key
        except LineException as e:
            raise e
        except:
            raise Exception('Wrong coordinate')

    def __copy(self, other):
        self.__virtual_player = other.get_cur_player()
        for r1, r2 in zip(self.get_lines(), other.get_lines()):
            for e1, e2 in zip(r1, r2):
                e1.set_player(e2.get_player(), e2.get_order())

    def __revoke(self):
        if self.__last_play is not None:
            x, y = self.__last_play
            self.get_lines()[x][y].set_player(0, order=0, force=True)
