from cairosvg import svg2png
import chess
import chess.svg
import logging
import os
import pathlib
import random
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils import fen_to_filename

logging.basicConfig(level=logging.INFO,
                    format="%(name)s - %(levelname)s - %(message)s")


def initialize_data_folders(path_data: pathlib.Path):
    if not os.path.exists(path_data):
        os.makedirs(path_data)
    subdirectories = [
        "corner_detection",
        "generated",
        "occupancy_detection",
        "square_extraction",
        "logs",
    ]
    for subdir in subdirectories:
        dir_path = path_data.joinpath(subdir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    logging.info("Data folders have been initialized.")


def save_board_image(board, filename):
    board_svg = chess.svg.board(board, coordinates=False)
    svg2png(
        bytestring=board_svg, write_to=filename, output_width=400, output_height=400
    )


def simulate_game(path_data: pathlib.Path, game_id):
    random.seed(42)
    board = chess.Board()
    move_count = 0
    game_log_filename = path_data.joinpath(
        "logs").joinpath(f"game_{game_id}.log")

    with open(game_log_filename, "w") as log_file:
        try:
            while not board.is_game_over():
                move = random.choice(list(board.legal_moves))
                board.push(move)
                move_count += 1
                save_board_image(board, str(path_data.joinpath(
                    "generated").joinpath(fen_to_filename(board.fen()))))
                log_file.write(f"{board.fen()}\n")

        except Exception as e:
            logging.warning(f"Error during game {game_id}: {e}")

    return f"Game {game_id} over after {move_count} moves."


def simulate_games(path_data, num_games):
    path_simulated = path_data.joinpath("generated")
    results = []
    num_cpus = os.cpu_count() or 1
    logging.info(
        f"""
            =========== Playing simulated games ===========
            {num_cpus} CPUs available, simulating {num_games} games
            playing {min(num_cpus, num_games)} in parallel
            saving images to {path_simulated}

        """
    )
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        futures = [
            executor.submit(simulate_game, path_data, i)
            for i in range(num_games)
        ]
        for future in as_completed(futures):
            results.append(future.result())

    for result in results:
        logging.info(result)
