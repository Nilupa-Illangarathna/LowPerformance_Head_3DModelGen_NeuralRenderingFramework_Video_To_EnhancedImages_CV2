import cv2
import os
import shutil
from itertools import combinations

def calculate_similarity(image1_path, image2_path, sift, similarity_threshold):
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    similarity_score = len(good_matches) / len(keypoints1)

    return similarity_score

def filter_similar_images(input_dir, output_dir, similarity_threshold):
    os.makedirs(output_dir, exist_ok=True)

    # Create a SIFT detector
    sift = cv2.SIFT_create()

    image_paths = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir)]
    
    distinct_images = []

    for image_path1, image_path2 in combinations(image_paths, 2):
        similarity_score = calculate_similarity(image_path1, image_path2, sift, similarity_threshold)
        
        if similarity_score < similarity_threshold:
            distinct_images.append(image_path1)
    
    for image_path in distinct_images:
        shutil.copy(image_path, output_dir)

if __name__ == "__main__":
    # Load configuration from the JSON file
    with open("input.json", "r") as json_file:
        config = json.load(json_file)

    # Check if the image similarity check task is defined
    if "image_similarity_check" in config:
        similarity_config = config["image_similarity_check"]
        input_dir = similarity_config["input_dir"]
        output_dir = similarity_config["output_dir"]
        similarity_threshold = similarity_config["similarity_threshold"]

        filter_similar_images(input_dir, output_dir, similarity_threshold)
        print("Image similarity check task completed.")
