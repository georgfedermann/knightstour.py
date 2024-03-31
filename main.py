import argparse
from game.knights_tour import Board, KnightsTourConfig, KnightsTour

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable detailed output for diagnostic purposes.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--closed', action='store_true', help='Attempt to find a closed Knight\'s Tour, where the tour forms a cycle.')
    group.add_argument('-r', '--randomize', action='store_true', help='Randomize the search for possible paths. Not recommended for closed tour searches.')
    args = parser.parse_args()
    config = KnightsTourConfig(verbose=args.verbose,
                               randomize_paths=args.randomize,
                               closed_paths=args.closed)

    board = Board()
    knights_tour = KnightsTour(config)
    print(knights_tour.find_knights_path(board, (6, 2), 1))

if __name__ == "__main__":
    main()
