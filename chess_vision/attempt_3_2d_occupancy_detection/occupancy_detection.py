from collections import Counter
from src.data import initialize_data_folders, simulate_games
from src.occupancy import detect_occupancy
import logging
import os
import pathlib

path_data = pathlib.Path("data").expanduser()
log_file_path = path_data.joinpath("logs").expanduser()
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)
log_file = log_file_path.joinpath("occupancy_detection.log")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file.as_posix(),
                    filemode='a')


def process_game_data(path_data):
    logging.info("Processing images...")
    results = []
    for index, filename in enumerate(os.listdir(path_data.joinpath("generated"))):
        if index == 0:
            save_squares = True
        else:
            save_squares = False
        if filename.endswith(".png"):
            path_image = path_data.joinpath("generated").joinpath(filename)
            results.append(
                detect_occupancy(path_image, threshold=60.0,
                                 save_squares=save_squares)
            )
    frequency_count = Counter(results)
    logging.info(f"Total samples: {len(results)}")
    for value, count in frequency_count.items():
        logging.info(f"{value}: {count}")


if __name__ == "__main__":
    initialize_data_folders(path_data)
    simulate_games(path_data, 10)
    process_game_data(path_data)
