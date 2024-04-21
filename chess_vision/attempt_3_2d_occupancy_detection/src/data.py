from cairosvg import svg2png
import chess
import chess.svg
import logging
import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')


def initialize_data_folders():
    main_dir = 'data'
    subdirectories = ['corner_detection', 'generated',
                      'occupancy_detection', 'square_extraction', 'logs']
    for subdir in subdirectories:
        dir_path = os.path.join(main_dir, subdir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    logging.info("Data folders have been initialized.")


def save_board_image(board, filename):
    board_svg = chess.svg.board(board, coordinates=False)
    svg2png(bytestring=board_svg, write_to=filename,
            output_width=400, output_height=400)


def simulate_game(folder_path, log_path, game_id):
    board = chess.Board()
    move_count = 0
    game_log_filename = os.path.join(log_path, f"game_{game_id}.log")

    with open(game_log_filename, 'w') as log_file:
        try:
            while not board.is_game_over():
                move = random.choice(list(board.legal_moves))
                board.push(move)
                move_count += 1

                # use modified FEN notation for filename
                fen = board.fen().split(' ')[0]
                fen_modified = fen.replace('/', '-')
                filename = os.path.join(folder_path, f"{fen_modified}.jpeg")
                save_board_image(board, filename)
                log_file.write(f"{board.fen()}\n")

        except Exception as e:
            logging.warning(f"Error during game {game_id}: {e}")

    return f"Game {game_id} over after {move_count} moves."


def simulate_games(folder_path, log_path, num_games):
    results = []
    num_cpus = os.cpu_count() or 1
    logging.info(
        f"""
            =========== Playing simulated games ===========
            {num_cpus} CPUs available, simulating {num_games} games
            playing {min(num_cpus, num_games)} in parallel
            saving images to {folder_path}

        """
    )
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        futures = [executor.submit(simulate_game, folder_path, log_path, i)
                   for i in range(num_games)]
        for future in as_completed(futures):
            results.append(future.result())

    for result in results:
        logging.info(result)


if __name__ == "__main__":
    initialize_data_folders()
    simulate_games('data/generated', 'data/logs', 10)
