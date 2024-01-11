# import cv2
# import os
#
# def calculate_blur(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Calculate the Laplacian variance as a measure of blur
#     return cv2.Laplacian(gray, cv2.CV_64F).var()
#
# def calculate_sharpness(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Calculate the variance of the gradient as a measure of sharpness
#     return cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5).var()
#
# def extract_frames(video_path, output_dir, batch_size=20, blur_threshold=5, sharpness_threshold=100):
#     # Create the output directory structure
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Open the video file
#     cap = cv2.VideoCapture(video_path)
#
#     # Check if the video file was successfully opened
#     if not cap.isOpened():
#         print("Error: Could not open video file.")
#         return
#
#     # Initialize a frame counter
#     frame_count = 0
#     reference_frame = None
#
#     while True:
#         frames = []
#         for _ in range(batch_size):
#             ret, frame = cap.read()
#
#             if not ret:
#                 break
#
#             frames.append(frame)
#
#         if not frames:
#             break
#
#         # Save frames as images with monotonically increasing sequence numbers
#         for i, frame in enumerate(frames):
#             if reference_frame is None:
#                 # Save the first frame as the reference frame
#                 reference_frame = frame
#                 frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
#                 cv2.imwrite(frame_filename, frame)
#                 frame_count += 1
#             else:
#                 # Calculate the difference between the current frame and the reference frame
#                 diff = cv2.absdiff(reference_frame, frame)
#                 overall_difference = (diff.sum() / float(frame.size)) * 100
#
#                 if overall_difference > 5:
#                     # Check blur and sharpness constraints
#                     blur_level = calculate_blur(frame)
#                     sharpness_level = calculate_sharpness(frame)
#
#                     if blur_level < blur_threshold and sharpness_level > sharpness_threshold:
#                         # Save the frame as a different-looking frame
#                         frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
#                         cv2.imwrite(frame_filename, frame)
#                         frame_count += 1
#
#         if len(frames) < batch_size:
#             break
#
#     # Release the video capture object
#     cap.release()
#
#     print(f"Frames extracted and saved to {output_dir} in batches of {batch_size}.")
#
# # Rest of your code...
#
# if __name__ == "__main__":
#     # Code to execute when run directly as a script
#     pass











import cv2
import os

def calculate_blur(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the Laplacian variance as a measure of blur
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_sharpness(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the variance of the gradient as a measure of sharpness
    return cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5).var()

def extract_frames(video_path, output_dir, batch_size=20, blur_threshold=5, sharpness_threshold=100):
    # Create the output directory structure
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Initialize a frame counter
    frame_count = 0
    reference_frame = None

    while True:
        frames = []
        for _ in range(batch_size):
            ret, frame = cap.read()

            if not ret:
                break

            frames.append(frame)

        if not frames:
            break

        # Save frames as images with monotonically increasing sequence numbers
        for i, frame in enumerate(frames):
            if reference_frame is None:
                # Save the first frame as the reference frame
                reference_frame = frame
                frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_count += 1
            else:
                # Calculate the difference between the current frame and the reference frame
                diff = cv2.absdiff(reference_frame, frame)
                overall_difference = (diff.sum() / float(frame.size)) * 100

                if overall_difference > 5:
                    # Check blur and sharpness constraints
                    blur_level = calculate_blur(frame)
                    sharpness_level = calculate_sharpness(frame)

                    if blur_level < blur_threshold and sharpness_level > sharpness_threshold:
                        # Save the frame as a different-looking frame
                        frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
                        cv2.imwrite(frame_filename, frame)
                        frame_count += 1

        if len(frames) < batch_size:
            break

    # Release the video capture object
    cap.release()

    print(f"Frames extracted and saved to {output_dir} in batches of {batch_size}.")

# Rest of your code...

if __name__ == "__main__":
    # Code to execute when run directly as a script
    pass
