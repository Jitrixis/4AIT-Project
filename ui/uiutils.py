import pygame


class UIUtils:
    BOARD_SIZE = 5
    SQUARE_SIZE = 80
    LINE_SIZE = 10
    PADDING = 20
    BACKGROUND_COLOR = (255, 255, 255)
    PLAYERS_LINE_COLOR = [(220, 220, 220), (205, 50, 50), (50, 205, 50), (50, 50, 205), (205, 205, 50), (50, 205, 205),
                          (205, 50, 205)]
    PLAYERS_SQUARE_COLOR = [(240, 240, 240), (205, 50, 50), (50, 205, 50), (50, 50, 205), (205, 205, 50),
                            (50, 205, 205), (205, 50, 205)]
    SURFACE = None

    @classmethod
    def init_surface(cls):
        cls.SURFACE = pygame.display.set_mode((
            cls.BOARD_SIZE * cls.SQUARE_SIZE + cls.PADDING * 2,
            cls.BOARD_SIZE * cls.SQUARE_SIZE + cls.PADDING * 2 + 100
        ))
        cls.SURFACE.fill(cls.BACKGROUND_COLOR)

    @classmethod
    def draw_lines(cls, board):
        for x, r in enumerate(board.get_lines()):
            for y, l in enumerate(r):
                cls.__draw_line(x, y, int(l))

    @classmethod
    def __draw_line(cls, x, y, player, color=None):
        p1 = (
            cls.PADDING + y * cls.SQUARE_SIZE,
            cls.PADDING + x // 2 * cls.SQUARE_SIZE
        )
        p2 = (
            (p1[0] + cls.SQUARE_SIZE if x % 2 == 0 else p1[0]),
            (p1[1] + cls.SQUARE_SIZE if x % 2 == 1 else p1[1])
        )
        pygame.draw.line(cls.SURFACE, cls.PLAYERS_LINE_COLOR[player] if color is None else color, p1, p2, cls.LINE_SIZE)

    @classmethod
    def draw_squares(cls, board):
        for x, r in enumerate(board.get_squares()):
            for y, s in enumerate(r):
                cls.__draw_square(x, y, int(s))

    @classmethod
    def __draw_square(cls, x, y, player):
        p = (
            cls.PADDING + y * cls.SQUARE_SIZE + cls.LINE_SIZE,
            cls.PADDING + x * cls.SQUARE_SIZE + cls.LINE_SIZE,
            cls.SQUARE_SIZE - cls.LINE_SIZE * 2,
            cls.SQUARE_SIZE - cls.LINE_SIZE * 2
        )
        pygame.draw.rect(cls.SURFACE, cls.PLAYERS_SQUARE_COLOR[player], p)

    @classmethod
    def select(cls, pos):
        x, y = pos
        if cls.LINE_SIZE < (x - cls.PADDING) % cls.SQUARE_SIZE < cls.SQUARE_SIZE - cls.LINE_SIZE:
            if (y - cls.PADDING) % cls.SQUARE_SIZE < cls.LINE_SIZE or (
                        y - cls.PADDING) % cls.SQUARE_SIZE > cls.SQUARE_SIZE - cls.LINE_SIZE:
                return round((y - cls.PADDING) / cls.SQUARE_SIZE) * 2, (
                    x - cls.PADDING) // cls.SQUARE_SIZE
        if cls.LINE_SIZE < (y - cls.PADDING) % cls.SQUARE_SIZE < cls.SQUARE_SIZE - cls.LINE_SIZE:
            if (x - cls.PADDING) % cls.SQUARE_SIZE < cls.LINE_SIZE or (
                        x - cls.PADDING) % cls.SQUARE_SIZE > cls.SQUARE_SIZE - cls.LINE_SIZE:
                return (y - cls.PADDING) // cls.SQUARE_SIZE * 2 + 1, round(
                    (x - cls.PADDING) / cls.SQUARE_SIZE)
        return None

    @classmethod
    def main_text(cls, text, color):
        cls.__text(text, (cls.PADDING + 20, cls.BOARD_SIZE * cls.SQUARE_SIZE + cls.PADDING + 20),
                   color, "courrier", 50, cls.BACKGROUND_COLOR)

    @classmethod
    def second_text(cls, text):
        cls.__text(text, (cls.PADDING + 20, cls.BOARD_SIZE * cls.SQUARE_SIZE + cls.PADDING + 80),
                   (0, 0, 0), "courrier", 20, cls.BACKGROUND_COLOR)

    @classmethod
    def __text(cls, text, pos, color, font, size, background):
        myfont = pygame.font.SysFont(font, size)
        label = myfont.render(text, 1, color, background)
        cls.SURFACE.blit(label, pos)
        pass

    @classmethod
    def debug_line(cls, pos, color=(255, 255, 0)):
        x, y = pos
        cls.__draw_line(x, y, 3, color)
