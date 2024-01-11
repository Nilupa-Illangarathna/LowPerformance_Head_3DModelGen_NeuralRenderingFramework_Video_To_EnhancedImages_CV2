import cv2
import os
import json
import time
import numpy as np


def calculate_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def is_sharp(image, threshold=7):
    return calculate_blur(image) < threshold


def is_different(image1, image2, threshold=0.4):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between the images
    diff = cv2.absdiff(gray1, gray2)

    # Calculate the mean absolute difference
    mean_diff = np.mean(diff)

    return mean_diff > threshold


def extract_frames(video_path, output_dir, batch_size=1):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_count = 0
    last_saved_frame = None

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if last_saved_frame is None:
            # Save the first frame as the reference
            last_saved_frame = frame
            frame_filename = os.path.join(output_dir, f"{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        else:
            # Check if the frame is different
            if is_different(last_saved_frame, frame) and is_sharp(frame):
                frame_filename = os.path.join(output_dir, f"{frame_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_count += 1
                # Update the last saved frame for the next iteration
                last_saved_frame = frame

    cap.release()
    print(f"Frames extracted and saved to {output_dir}.")

if __name__ == "__main__":
    start_time = time.time()

    video_path = os.path.join("input", "video02.mp4")
    output_dir_video = os.path.join("output", "frames")

    extract_frames(video_path, output_dir_video)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken to complete the function: {time_taken} seconds")
