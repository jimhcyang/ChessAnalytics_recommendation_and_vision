import chess
import cv2
import numpy as np
from src.corners import detect_corners


def create_square_mapping():
    square_mapping = []
    for rank in reversed(range(8)):
        for file in range(8):
            square = chess.square(file, rank)
            square_mapping.append(chess.square_name(square))
    return square_mapping


def extract_squares(image):
    ret, corners, viz_corners = detect_corners(image)
    if ret:
        squares = []
        square_size = int(image.shape[0]/8)
        x1, y1 = corners[0].ravel()
        # correction for square offsets
        x1 = x1 - square_size
        y1 = y1 - square_size
        for row in range(8):
            for col in range(8):
                x_start = x1 + col * square_size
                y_start = y1 + row * square_size
                squares.append((int(x_start), int(y_start),
                               int(square_size), int(square_size)))
        return squares, viz_corners
    else:
        return None, None
