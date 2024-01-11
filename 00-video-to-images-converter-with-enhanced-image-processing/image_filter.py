import cv2
import os

def filter_and_save_large_images(input_dir, output_dir, min_width=200, min_height=200):
    # Create the output directory structure
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            file_path = os.path.join(input_dir, filename)
            image = cv2.imread(file_path)

            if image is not None:
                height, width, _ = image.shape

                if width >= min_width and height >= min_height:
                    output_file = os.path.join(output_dir, filename)
                    cv2.imwrite(output_file, image)


if __name__ == "__main__":
    # Code to execute when run directly as a script
    pass
