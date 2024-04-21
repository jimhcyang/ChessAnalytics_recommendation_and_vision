import logging
import os
import pathlib
from src.occupancy import detect_occupancy
from src.data import initialize_data_folders, simulate_games
from collections import Counter

logging.basicConfig(level=logging.INFO,
                    format="%(name)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    path_data = pathlib.Path("data").expanduser()
    initialize_data_folders(path_data)
    simulate_games(path_data, 10)
    results = []
    for index, filename in enumerate(os.listdir(path_data)):
        if index == 0:
            save_squares = True
        else:
            save_squares = False
        if filename.endswith(".jpeg"):
            path_image = path_data.joinpath(filename)
            results.append(
                detect_occupancy(path_image, threshold=60.0,
                                 save_squares=save_squares)
            )
    frequency_count = Counter(results)
    for value, count in frequency_count.items():
        logging.info(f"{value}: {count}")
