import cv2
import numpy as np
import pathlib
import chess
import os
from matplotlib import pyplot as plt


def filename_to_fen(filename):
    board_part = filename.split('.')[0].replace('-', '/')
    full_fen = f"{board_part} w KQkq - 0 1"
    try:
        board = chess.Board(full_fen)
        return board.fen()
    except ValueError as e:
        print(f"Error creating board from FEN: {e}")
        return None


def fen_to_all_white_pawns(fen):
    board = chess.Board(fen)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            board.set_piece_at(square, chess.Piece(chess.PAWN, chess.WHITE))
    return board.fen()


def create_square_mapping():
    square_mapping = []
    for rank in reversed(range(8)):
        for file in range(8):
            square = chess.square(file, rank)
            square_mapping.append(chess.square_name(square))
    return square_mapping


def detect_corners(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 143])
    upper_bound = np.array([179, 61, 252])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
    dilated = cv2.dilate(mask, kernel, iterations=5)
    result = 255 - cv2.bitwise_and(dilated, mask)
    result = np.uint8(result)
    ret, corners = cv2.findChessboardCorners(
        result, (7, 7), flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    return ret, corners, mask


def detect_and_extract_squares(image):
    ret, corners, mask = detect_corners(image)
    if ret:
        corners = cv2.cornerSubPix(mask, corners, (11, 11), (-1, -1),
                                   (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)).round()
        squares = []
        # Calculate average square dimensions
        dx = round(np.mean(np.diff(corners[:, 0, 0].reshape(7, 7), axis=1)))
        dy = round(np.mean(np.diff(corners[:, 0, 1].reshape(7, 7), axis=0)))
        # Estimate the full board layout
        x1, y1 = corners[0].ravel()
        # correction for square offsets
        x1 = x1 - dx
        y1 = y1 - dy
        for row in range(8):
            for col in range(8):
                x_start = x1 + col * dx
                y_start = y1 + row * dy
                squares.append((int(x_start), int(y_start), int(dx), int(dy)))
        return squares


def detect_occupancy(path_image, output_dir, threshold, output_dir_squares=None):
    name_image = pathlib.Path(path_image).name
    fen = filename_to_fen(name_image)
    fen_pawns = fen_to_all_white_pawns(fen)
    occupancy_detection_filename = f"{output_dir}/{name_image}"
    image = cv2.imread(path_image)
    squares = detect_and_extract_squares(image)
    mapping = create_square_mapping()
    occupancy_detection = image.copy()
    occupied = []
    occupied_fen = []
    for index, (x, y, w, h) in enumerate(squares):
        square_location = mapping[index]
        square = image[y:y+h, x:x+w]
        std_dev = np.std(square)
        if output_dir_squares:
            cv2.imwrite(
                f"{output_dir_squares}/{name_image}_{square_location}_stddev_{round(std_dev, 2)}.jpeg", square)
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


if __name__ == "__main__":
    directory = "data/raw/"
    for filename in os.listdir(directory):
        if filename.endswith('.jpeg'):
            # Full path to the file
            path_image = os.path.join(directory, filename)
    detect_occupancy(path_image,
                     output_dir="data/occupancy_detection/",
                     threshold=15.0,
                     output_dir_squares="data/occupancy_detection_squares/"
                     )
