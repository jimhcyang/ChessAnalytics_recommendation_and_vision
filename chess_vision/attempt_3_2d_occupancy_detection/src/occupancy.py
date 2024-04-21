import chess
import cv2
import numpy as np
import pathlib
from src.evaluate import compare_occupancy
from src.squares import extract_squares, create_square_mapping
from src.utils import filename_to_fen
from src.visualization import (save_corner_visualization,
                               save_squares_visualizations,
                               save_occupancy_detection_visualization
                               )
import logging

logger = logging.getLogger(__name__)


def map_occupied_to_pawns(occupied_fen):
    board = chess.Board(None)
    for square in occupied_fen:
        board.set_piece_at(chess.parse_square(square),
                           chess.Piece(chess.PAWN, chess.WHITE))
    return board.fen()


def detect_occupancy(path_image, threshold, save_squares=False):
    name_image = pathlib.Path(path_image).name
    original_fen = filename_to_fen(name_image)
    image = cv2.imread(str(path_image))
    squares, viz_corners = extract_squares(image)
    if viz_corners is not None:
        save_corner_visualization(name_image, viz_corners)
    mapping = create_square_mapping()
    occupancy_detection = image.copy()
    occupied = []
    occupied_fen = []
    if squares:
        for index, (x, y, w, h) in enumerate(squares):
            square_location = mapping[index]
            square = image[y:y+h, x:x+w]
            std_dev = np.std(square)
            if not np.isnan(std_dev) and save_squares:
                save_squares_visualizations(
                    name_image, square, square_location, std_dev)
            if std_dev > threshold:
                occupied.append((x, y))
                occupied_fen.append(square_location)
                cv2.rectangle(occupancy_detection, (x, y),
                              (x+w, y+h), (0, 0, 255), 2)
        save_occupancy_detection_visualization(name_image, occupancy_detection)
        predicted_occupancy = map_occupied_to_pawns(occupied_fen)
        result = compare_occupancy(
            original_fen=original_fen,
            predicted_occupancy=predicted_occupancy
        )
        return result
    else:
        return "Failed to detect squares"
