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
    """
    This game engine manages a chessboard with which the user can interact to
    try and finish a knight's tour.
    Also, it drives an algorithm to provide solutions to inspire the user with
    ever new solutions.

    The chessboard: the chessboard consists of 64 squares.
    Each square has an index from 0 to 63. The indices are counted from the
    top left corner to the bottom right corner row by row.
    00 01 02 03 04 05 06 07
    08 09 10 11 12 13 14 15
    16 17 18 19 20 21 22 23
    24 25 26 27 28 29 30 31
    32 33 34 35 36 37 38 39
    40 41 42 43 44 45 46 47
    48 49 50 51 52 53 54 55
    56 57 58 59 60 61 62 63
    The user can interact with the squares by clicking them with the mouse.
    E.g. to select a start field for the algorithm.
    E.g. to setup an initial configuration to have the algorithm resolve a given
    configuration.

    The user can configure the algorithm with a selection of checkboxes or
    radio buttons:
    - Randomize solution
    - Search for closed tours, where the last move ends within on knight's
      move to the starting field, so the knight could just go through another
      loop.

    The algorithm can be triggered at any time by clicking the button
    "Solve Now" (or similar).
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_DIMENSION)
        pygame.display.set_caption('Grimbart\'s Knight\'s Tour\'s Solver')

        self.blink_counter = 0.1

        self.clock = pygame.time.Clock()
        self.keep_running = True

        self.path = self.get_path()

        self.squares_group = Group()
        for idx in range(64):
            self.squares_group.add(Square(idx))

    def generate_move_labels_from_path(self, path: List[int]) -> List[int]:
        result = [0] * len(path)
        for move_number, square_idx in enumerate(path):
            result[square_idx] = move_number
        return result

    def coordinate_to_index(self, coordinate: Tuple[int, int]) -> int:
        return coordinate[0] * 8 + coordinate[1]

    def get_path(self) -> List[int]:
        """
        Returns the list of indices of the squares for the Knight's Tour.
        """
        board = Board()
        config = KnightsTourConfig()
        config.closed_paths = True
        config.verbose = False
        knights_tour = KnightsTour(config)
        coordinates = knights_tour.find_knights_path(board, (6, 2), 1)
        return [self.coordinate_to_index(coordinate) for coordinate in coordinates]

    def get_square_mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        for square in self.squares_group:
            if square.rect.collidepoint(mouse_pos):
                return square

    def reveal_next_square(self):
        if self.reveal_index < len(self.path):
            square_idx = self.path[self.reveal_index]
            square = self.squares_group.sprites()[square_idx]
            square.set_label(str(self.reveal_index + 1))
            self.reveal_index += 1

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.keep_running = False

        if pygame.time.get_ticks() - self.last_reveal_time > 1500:
            self.reveal_next_square()
            self.last_reveal_time = pygame.time.get_ticks()

        self.get_square_mouse_over()

    def run_knights_tour(self):
        self.last_reveal_time = pygame.time.get_ticks()
        self.reveal_index = 0

        while self.keep_running:
            self.run_game()

            self.squares_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(GameConfig.FPS)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_knights_tour()
