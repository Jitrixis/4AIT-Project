import pygame
from pygame.locals import *

from game.board import Board
from ui.uiutils import UIUtils


class UIManager:
    def __init__(self, player, size=5):
        self.__players = player
        self.__board = Board(size=size, num_player=len(self.__players) - 1)
        self.__semaphore_event = None
        pygame.init()
        UIUtils.BOARD_SIZE = self.__board.get_size()
        UIUtils.init_surface()
        # stats
        # self.__stats = [0 for _ in range(len(self.__players))]
        # print(self.__players)

    def run(self):
        q = True
        while q:
            # GUI
            UIUtils.draw_squares(self.__board)
            UIUtils.draw_lines(self.__board)
            # EVENT
            for event in pygame.event.get():
                if event.type == QUIT:
                    q = False
                if event.type == MOUSEBUTTONUP:
                    self.__semaphore_event = UIUtils.select(event.pos)
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.__board = Board(self.__board.get_size(), self.__board.get_num_player())
                        self.__semaphore_event = None
                    if event.key == K_n:
                        self.__semaphore_event = 'N'
            # GAME
            if self.__board:
                UIUtils.main_text(' WIN USER ' + str(int(self.__board)),
                                  UIUtils.PLAYERS_SQUARE_COLOR[int(self.__board)])
                UIUtils.second_text(str(self.__board.get_score()))
                # stat
                # self.__stats[int(self.__board)] += 1
                # if sum(self.__stats) in range(10, 101, 10):
                #     print('STATS for', sum(self.__stats), self.__stats)
                # if sum(self.__stats) == 100:
                #     q = False
                # self.__board = Board(self.__board.get_size())
                # self.__semaphore_event = None
            else:
                UIUtils.main_text('USER TURN ' + str(self.__board.get_cur_player()), (0, 0, 0))
                UIUtils.second_text(str(self.__board.get_score()))
                try:
                    self.__players[self.__board.get_cur_player()].run(self.__semaphore_event, self.__board)
                except Exception as e:
                    print(e)
            # END
            self.__semaphore_event = None
            pygame.display.update()
        pygame.quit()
