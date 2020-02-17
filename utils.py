from pathlib import Path
from typing import List

import cv2
import numpy as np


def save_results(save_dir: Path, image: np.ndarray, all_contours: List, image_name: str):
    for c in all_contours:

        # Returns the location and width,height for every contour
        x, y, width, h = cv2.boundingRect(c)

        # get all the pixels coordinates under contour
        coordinates = []
        crd = get_cord(x, y, width, h)
        coordinates.append(crd)
        #

        if 30 > width > 15 > 10 and h < 20:
            # draw boundary of contour
            img_outlined = cv2.rectangle(image, (x, y), (x + width, y + h), (255, 255, 0), 2)

        # If the box height is greater then 20, width is >80,
        if 20 < width < 450 and 10 < h < 40:
            # draw contours
            img_outlined = cv2.rectangle(image, (x, y), (x + width, y + h), (0, 0, 255), 1)
    cv2.imwrite(f'{save_dir}/{image_name}', img_outlined)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    # Sharpening Image
    blurry_image = cv2.GaussianBlur(image, (0, 0), 3)
    sharp_image = cv2.addWeighted(image, 2, blurry_image, -1, 0)
    sharp_image = cv2.cvtColor(sharp_image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(sharp_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)

    # A kernel of (3 X 3) ones.
    kernel = np.ones((3, 3), np.uint8)
    img_bin_eroded = cv2.erode(binary_image, kernel, iterations=1)

    return ~img_bin_eroded


def get_cord(x, y, width, height):
    # get all pixels coordinates in a contour
    index = 0
    coords = []
    for i in range(x, x + width):
        for j in range(y, y + height):
            coords.insert(index, [i, j])
            # print(idx, coords)
            index += 1

    return coords


def find_boxes(binary_image: np.ndarray)->np.ndarray:
    # Defining a kernel length

    kernel_length = np.array(binary_image).shape[1] // 195

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(binary_image, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(binary_image, horiz_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, horiz_kernel, iterations=3)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get
    # a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)

    return cv2.adaptiveThreshold(~img_final_bin, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)


def sort_contours(contours, method="top-to-bottom"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to bottom
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    (contours, bounding_boxes) = zip(*sorted(zip(contours, bounding_boxes),
                                             key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return contours, bounding_boxes
