from typing import List, Tuple

class KnightMoves:
    """
    The class provides an algorithm to solve the Knight's Tour problem.
    """

    def __init__(self):
        self.knight_moves = [(2, -1), (1, 2), (-2, -1), (-1, -2), (2, 1), (-2, 1), (1, -2), (-1, 2)]

    def apply_knight_move(self, col, row, move) -> Tuple[int, int]:
        return (col + move[0], row + move[1]) 


    def initialize_chess_board(self) -> List[List[int]]:
        return [[0 for _ in range(8)] for _ in range(8)]

    def generate_heuristics(self, board) -> List[List[int]]:
        """
        Calculates for each field of the chess board from how many other unvisited
        fields it is still reachable.
        """
        heuristics_board = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                if board[x][y] != 0:
                    heuristics_board[x][y] = -1
                else:
                    for move in self.knight_moves:
                        target = self.apply_knight_move(x, y, move)
                        if 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and board[target[0]][target[1]] == 0:
                            # increase the reachability count for a field for each field from which it can be accessed
                            heuristics_board[x][y] += 1
        return heuristics_board

    def print_board(self, board) -> None:
        """
        Prints the given board to stdout
        """
        for y in range(8):
            for x in range(8):
                print(board[y][x], end=' ')
            print()

    def print_side_by_side(self, board1, board2) -> None:
        """
        Prints 2 boards side by side. E.g. to log the current game status and the
        heuristics based on which the decision making is done
        """
        for y in range(8):
            for x in range(8):
                print(board1[y][x], end=' ')
            print('   ', end='')
            for x in range(8):
                print(board2[y][x], end=' ')
            print()
        print(35 * '*')

    def evaluate_moves(self, board, position, moves) -> List[List[int]]:
        heuristics = self.generate_heuristics(board)
        evaluation = [[] for _ in range(9)]
        for idx, move in enumerate(moves):
            target = [position[0] + move[0], position[1] + move[1]]
            if 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and heuristics[target[0]][target[1]] >= 0:
                evaluation[heuristics[target[0]][target[1]]].append(idx)
        return evaluation

    def find_path(self, chess_board, position=None) -> List[Tuple[int, int]]:
        suggested_moves = []
        if not position:
            position = (0, 0)

        keep_going = True
        step = 1

        while keep_going:
            chess_board[position[0]][position[1]] = step
            step += 1
            heuristics = self.generate_heuristics(chess_board)
            self.print_side_by_side(chess_board, heuristics)

            evaluation = list(filter(lambda x: len(x) > 0, self.evaluate_moves(chess_board, position, self.knight_moves)))

            if len(evaluation) > 0:
                suggested_move = self.knight_moves[evaluation[0][0]]
                suggested_moves.append(suggested_move)

                position = (position[0] + suggested_move[0], position[1] + suggested_move[1])

                print(f'Suggested next move is {self.knight_moves[evaluation[0][0]]}')
                print(evaluation)
            else:
                keep_going = False
                print('Done.')

        return suggested_moves
