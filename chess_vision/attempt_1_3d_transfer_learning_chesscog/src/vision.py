import cv2
import os


def mov_to_images(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = cv2.VideoCapture(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_count = 0
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_path = os.path.join(
            output_dir, f'{video_name}_frame_{frame_count:04d}.png')
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()
    print(
        f'Frames extracted and saved to {output_dir}. Total frames: {frame_count}.')


if __name__ == "__main__":
    mov_to_images("data/raw/chessboard_video_1.MOV", "data/processed")
