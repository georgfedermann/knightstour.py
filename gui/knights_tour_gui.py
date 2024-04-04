from warnings import warn
import pygame
from pygame.font import Font
from pygame.sprite import Group, Sprite
from typing import List, Tuple

from game.knights_tour import Board, KnightsTour, KnightsTourConfig

class GameConfig:
    FPS = 60
    SCREEN_DIMENSION = (800, 800)

    # chessboard
    BLACK = (125, 135, 150)
    WHITE = (232, 235, 239)
    LABEL_COLOR = (50, 50, 200)

    SQUARE_DIMENSION = (80, 80)

class Square(Sprite):

    _font = None

    def __init__(self, index, label: str=""):
        super().__init__()
        self.index = index
        self.row = index // 8
        self.col = index % 8
        self.color = GameConfig.WHITE if (self.row + self.col) % 2 == 0 else GameConfig.BLACK
        self.position = (GameConfig.SQUARE_DIMENSION[0] * self.col,
                         GameConfig.SQUARE_DIMENSION[1] * self.row)
        self.image = pygame.Surface(GameConfig.SQUARE_DIMENSION)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.position)
        self.set_label(label)

    def set_label(self, label: str=''):
        if label:
            text = self.font.render(label, True, GameConfig.LABEL_COLOR) 
            text_rect = text.get_rect(center=(GameConfig.SQUARE_DIMENSION[0] / 2,
                                              GameConfig.SQUARE_DIMENSION[1] / 2))
            self.image.blit(text, text_rect)

    @property
    def font(self) -> Font:
        if not Square._font:
            Square._font = pygame.font.Font('font/Pixeltype.ttf', 50)
        return Square._font

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_DIMENSION)
        pygame.display.set_caption('Grimbart\'s Knight\'s Tour\'s Solver')

        self.blink_counter = 0.1

        self.clock = pygame.time.Clock()
        self.keep_running = True

        path = self.get_path()
        labels = list(range(64))
        for move, square_idx in enumerate(path):
            labels[square_idx] = move

        self.squares_group = Group()
        for idx in range(64):
            self.squares_group.add(Square(idx, str(labels[idx] + 1)))


    def coordinate_to_index(self, coordinate: Tuple[int, int]) -> int:
        return coordinate[0] * 8 + coordinate[1]

    def get_path(self) -> List[int]:
        """
        Returns the list of indices of the squares for the Knight's Tour.
        """
        board = Board()
        config = KnightsTourConfig()
        config.closed_paths = True
        knights_tour = KnightsTour(config)
        coordinates = knights_tour.find_knights_path(board, (6, 2), 1)
        return [self.coordinate_to_index(coordinate) for coordinate in coordinates]

    def get_square_mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        for square in self.squares_group:
            if square.rect.collidepoint(mouse_pos):
                return square

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.keep_running = False

        self.get_square_mouse_over()

    def run_knights_tour(self):
        while self.keep_running:
            self.run_game()

            self.squares_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(GameConfig.FPS)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_knights_tour()
