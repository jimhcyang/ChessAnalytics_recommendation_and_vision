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
