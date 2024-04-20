import logging
import os
from src.occupancy import detect_occupancy

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    directory = "data/raw/"
    for filename in os.listdir(directory):
        if filename.endswith('.jpeg'):
            path_image = os.path.join(directory, filename)
            logging.info(f"processing {filename}")
            detect_occupancy(path_image,
                             threshold=15.0
                             )
