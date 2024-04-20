import chess
import cv2
import numpy as np
import pathlib
from src.utils import filename_to_fen, fen_to_all_white_pawns
from src.squares import extract_squares, create_square_mapping


def detect_occupancy(path_image, threshold):
    name_image = pathlib.Path(path_image).name
    fen = filename_to_fen(name_image)
    fen_pawns = fen_to_all_white_pawns(fen)
    occupancy_detection_filename = f"data/occupancy_detection/{name_image}"
    image = cv2.imread(path_image)
    squares, viz_corners = extract_squares(image)
    if viz_corners is not None:
        cv2.imwrite(f"data/corner_detection/{name_image}", viz_corners)
    mapping = create_square_mapping()
    occupancy_detection = image.copy()
    occupied = []
    occupied_fen = []
    if squares:
        for index, (x, y, w, h) in enumerate(squares):
            square_location = mapping[index]
            square = image[y:y+h, x:x+w]
            std_dev = np.std(square)
            cv2.imwrite(
                f"data/square_extraction/{name_image}_{square_location}_stddev_{round(std_dev, 2)}.jpeg", square)
            if std_dev > threshold:
                occupied.append((x, y))
                occupied_fen.append(square_location)
                cv2.rectangle(occupancy_detection, (x, y),
                              (x+w, y+h), (0, 0, 255), 2)
        cv2.imwrite(occupancy_detection_filename, occupancy_detection)
        board = chess.Board(None)
        for square in occupied_fen:
            board.set_piece_at(chess.parse_square(square),
                               chess.Piece(chess.PAWN, chess.WHITE))
        if board.fen() == fen_pawns:
            print("Correct")
        else:
            print("Mismatch")
