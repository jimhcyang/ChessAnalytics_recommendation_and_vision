import cv2
import numpy as np


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
    if ret:
        viz_corners = cv2.drawChessboardCorners(result, (7, 7), corners, ret)
    return ret, corners, mask, viz_corners
