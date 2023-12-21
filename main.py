from game.knights_tour import KnightMoves

def main():
    knight_moves = KnightMoves()
    knight_moves.find_path(knight_moves.initialize_chess_board(), (3, 4))

if __name__ == "__main__":
    main()
