import os
import csv

# Path to your dataset folder containing the images
# or 'chessboard_dataset/test' depending on your need
image_folder_path = 'data/occupancy/train'

# The uniform label for the starting position
chess_starting_position_label = '1111111111111111000000000000000000000000000000001111111111111111'

# The output CSV file
labels_csv_path = 'data/occupancy/train/labels.csv'

# Listing all image files in the folder
image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(
    os.path.join(image_folder_path, f))]

# Writing to the labels.csv file
with open(labels_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['filename', 'label'])

    for image_file in image_files:
        csvwriter.writerow([image_file, chess_starting_position_label])

print(f"labels.csv has been created with {len(image_files)} entries.")
