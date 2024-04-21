import cv2


def save_corner_visualization(name_image, viz_corners):
    cv2.imwrite(f"data/corner_detection/{name_image}", viz_corners)


def save_squares_visualizations(name_image, square, square_location, std_dev):
    cv2.imwrite(f"data/square_extraction/stddev-{round(std_dev, 2)}_{
                square_location}_{name_image}", square)


def save_occupancy_detection_visualization(name_image, occupancy_detection):
    occupancy_detection_filename = f"data/occupancy_detection/{name_image}"
    cv2.imwrite(occupancy_detection_filename, occupancy_detection)
