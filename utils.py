# ## Import Packages
import cv2
import numpy as np


def sharp(image):
    # Sharpening Image
    image_2 = cv2.GaussianBlur(image, (0, 0), 3)
    image_3 = cv2.addWeighted(image, 2, image_2, -1, 0)  # Apply Threshold
    # save sharped image
    cv2.imwrite("sharp.jpg", image_3)


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


def find_boxes(binary_image: np.ndarray):
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
    cv2.imwrite("verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(binary_image, horiz_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, horiz_kernel, iterations=3)
    cv2.imwrite("horizontal_lines.jpg", horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get
    # a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)

    return cv2.adaptiveThreshold(~img_final_bin, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)


def sort_contours(cnts, method="top-to-bottom"):
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
    bounding_boxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, bounding_boxes) = zip(*sorted(zip(cnts, bounding_boxes),
                                         key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return cnts, bounding_boxes
