import logging
import os
from src.occupancy import detect_occupancy

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    directory = "data/raw/"
    for index, filename in enumerate(os.listdir(directory)):
        if index == 0:
            save_squares = True
        else:
            save_squares = False
        if filename.endswith('.jpeg'):
            path_image = os.path.join(directory, filename)
            logging.info(f"processing {filename}")
            detect_occupancy(path_image,
                             threshold=15.0,
                             save_squares=save_squares
                             )
