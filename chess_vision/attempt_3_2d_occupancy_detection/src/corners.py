import cv2
import numpy as np


def detect_corners(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect chessboard corners
    ret, corners = cv2.findChessboardCorners(
        gray_image,
        (7, 7),
        flags=cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_FAST_CHECK
        + cv2.CALIB_CB_NORMALIZE_IMAGE,
    )

    if ret:
        square_size = int(image.shape[0] / 8)
        corners = np.round(corners / square_size) * square_size
        # Draw corners on the original image
        viz_corners = cv2.drawChessboardCorners(image.copy(), (7, 7), corners, ret)
    else:
        viz_corners = None

    return ret, corners, viz_corners
