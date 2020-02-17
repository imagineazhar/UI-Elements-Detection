from pathlib import Path

import cv2
import numpy as np

from utils import find_boxes, sort_contours, get_cord, preprocess_image, save_results

if __name__ == '__main__':
    # load color image
    base_address = Path('Inputs')
    image_paths = base_address.glob('*.png')
    results_save_dir = Path('results')
    results_save_dir.mkdir(parents=True, exist_ok=True)

    dim = (820, 600)

    for image_path in image_paths:
        print(image_path)
        original_image = cv2.imread(str(image_path))

        original_image = cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)

        image_color = original_image.copy()

        processed_image = preprocess_image(image=original_image)

        img_final_bin = find_boxes(processed_image)

        # Find contours for image, which will detect all the boxes
        contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

        save_results(save_dir=results_save_dir, image=image_color, all_contours=contours, image_name=image_path.name)

