from game.knights_tour import Board, KnightsTour

def main():
    board = Board()
    knights_tour = KnightsTour()
    print(knights_tour.find_knights_path(board, (6, 2), 1))

if __name__ == "__main__":
    main()
