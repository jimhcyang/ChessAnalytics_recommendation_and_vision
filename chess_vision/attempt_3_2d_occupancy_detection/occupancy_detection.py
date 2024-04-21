import logging
import os
from src.occupancy import detect_occupancy
from src.data import initialize_data_folders, simulate_games
from collections import Counter

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    initialize_data_folders()
    path_simulated_data = "data/generated/"
    path_logs = "data/logs"
    simulate_games(path_simulated_data, path_logs, 10)
    results = []
    for index, filename in enumerate(os.listdir(path_simulated_data)):
        if index == 0:
            save_squares = True
        else:
            save_squares = False
        if filename.endswith('.jpeg'):
            path_image = os.path.join(path_simulated_data, filename)
            results.append(detect_occupancy(path_image,
                                            threshold=60.0,
                                            save_squares=save_squares
                                            ))
    frequency_count = Counter(results)
    for value, count in frequency_count.items():
        logging.info(f"{value}: {count}")
