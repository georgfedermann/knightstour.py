from copy import deepcopy
from random import sample
from typing import List, Tuple

class Commons:
    knight_moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

class Board:
    """
    Represents a chessboard for the Knight's Tour problem.

    The Board class is responsible for managing the state of the board,
    including the positions visited by the Knight. It offers functionality
    to add a new position makring the knight's move and tracks the start
    position and the total number of moves made.
    """
    def __init__(self):
        self.squares = [[0 for _ in range(8)] for _ in range(8)]
        self.move_count = 0
        self.start_position = None

    def __str__(self):
        result = ""
        heuristics = self.get_heuristics()
        for row in range(8):
            result += f'{self.squares[row]}   ---   {heuristics[row]}\n'

        return result

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Check if a proposed position is valid on the board.
        A position is considered valid if it is within the 8x8 board boundaries
        and the square has not been previously visited.
        Args:
            position (Tuple[int,int]): To position to check, represented as a tuple of (row, column).
        Returns:
            bool: True if the position is valid and unvisited, False otherwise.
        """
        return (0 <= position[0] <= 7 and
                0 <= position[1] <= 7 and
                self.squares[position[0]][position[1]] == 0)

    def add_position(self, position: Tuple[int, int]) -> bool:
        if not self.is_valid_position(position):
            return False

        if (self.move_count == 0):
            self.start_position = position

        self.move_count += 1
        self.squares[position[0]][position[1]] = self.move_count
        return True

    def get_heuristics(self) -> List[List[int]]:
        heuristics = [[0 for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if self.squares[row][col] != 0:
                    heuristics[row][col] = -1
                else:
                    for move in Commons.knight_moves:
                        new_position = (row + move[0], col + move[1])
                        if self.is_valid_position(new_position):
                            heuristics[row][col] += 1
        return heuristics

    def get_moves_ranked_by_accessibility(self, current_position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns the indices of Commons.knight_moves which constitute valid
        moves from the indicated current position.
        The moves are sorted by the accessibility of the target squares of the
        move in ascending order.
        """
        moves = [[] for _ in range(9)]
        heuristics = self.get_heuristics()
        for move in Commons.knight_moves:
            new_position = (current_position[0] + move[0], current_position[1] + move[1])
            if self.is_valid_position(new_position):
                moves[heuristics[new_position[0]][new_position[1]]].append(move)

        return [move for sublist in moves for move in sublist]
        # return [move for sublist in moves for move in sample(sublist, len(sublist))]

class KnightsTour:
    """
    Implements a solution for finding a Knight's Tour on a chessboard.
    This class utilizes the Warnsdorff's Heuristic along with backtracking
    to calculate the tour.

    The algorithm is designed to find either oopen or closed tours, depending
    on the termination conditions specified within the 'find_knights_path'
    method.

    Adjusting these conditions allows for flexible usage according to different
    requirements or constraints.
    """

    def find_knights_path(self, current_board: 'Board', current_position: Tuple[int, int], move_index: int) -> List[Tuple[int, int]]:
        """
        Recursively calculates a Knight's Tour path from the given position on the chessboard.

        The method clones the current board and attempts to add the current
        position as a step in the tour. If the move index reaches the total
        number of squares and the tour can be closed with a knight's move back
        to the start, the tour is considered complete.

        Parameters:
            current_board (Board): The current state of the chessboard.
            current_position (Tuple[int, int]): The current position of the knight, represented as (row, column).
            move_index (int): The current step number in the tour.

        Returns:
            List[Tuple[int, int]]: A list of tuples representing the positions of
            the knight's tour, or an empty list if no tour is found from this position.
        """
        board_clone = deepcopy(current_board)
        board_clone.add_position(current_position)
        print(f'move_index: {move_index} current_position {current_position}')
        print(board_clone)
        # Check termination condition
        if move_index == 64 and (board_clone.start_position[0] - current_position[0], board_clone.start_position[1] - current_position[1]) in Commons.knight_moves:
            return [current_position]
        # get a list of all possible moves and rank them according to heuristics
        moves = board_clone.get_moves_ranked_by_accessibility(current_position)
        # iterate over moves until a path is found that fullfils the termination condition
        for move in moves:
           board_clone = deepcopy(current_board)
           board_clone.add_position(current_position)
           new_position = (current_position[0] + move[0], current_position[1] + move[1])
           sub_path = self.find_knights_path(board_clone, new_position, move_index + 1)
           if len(sub_path) > 0:
               return [current_position] + sub_path

        # if no move is available that can generate a sub path that satisfies the condition, hand back an empty path so that the caller can backtrack
        return []
