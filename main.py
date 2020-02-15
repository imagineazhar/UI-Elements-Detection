import cv2
import numpy as np

from utils import find_boxes, sharp, sort_contours, get_cord

if __name__ == '__main__':
    # load color image
    base_address = r'test/'
    image_file = '6.png'
    image_path = base_address + image_file
    original_image = cv2.imread(image_path)
    dim = (824, 600)
    original_image = cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)
    sharp(original_image)
    image_color = original_image.copy()

    # load image
    img = cv2.imread('sharp.jpg', 0)
    # A kernel of (3 X 3) ones.
    kernel = np.ones((3, 3), np.uint8)

    # (thresh, img_bin) = cv2.threshold(img, 200, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    img_bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)

    # morphological operation
    img_bin_eroded = cv2.erode(img_bin, kernel, iterations=1)

    # Invert Image
    img_bin = ~img_bin_eroded

    # save image
    cv2.imwrite("binary.jpg", img_bin)

    img_final_bin = find_boxes(img_bin)
    cv2.imwrite("img_final_bin.jpg", img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

    # Identifying Contours
    idx = 0
    cropped_path = 'Cropped/'
    for c in contours:

        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)

        # get all the pixels coordinates under contour
        coordinates = []
        crd = get_cord(x, y, w, h)
        coordinates.append(crd)
        #

        if 30 > w > 15 > 10 and h < 20:
            idx += 1
            # extract ROI
            new_img = img[y:y + h, x:x + w]
            cv2.imwrite(cropped_path + str(idx) + '.png', new_img)

            # draw boundary of contour
            img_outlined = cv2.rectangle(image_color, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # If the box height is greater then 20, width is >80, then only save it as a box in "cropped/" folder.
        if 20 < w < 450 and 10 < h < 40:
            idx += 1

            # ROI extraction
            new_img = img[y:y + h, x:x + w]
            cv2.imwrite(cropped_path + str(idx) + '.png', new_img)

            # draw contours
            img_outlined = cv2.rectangle(image_color, (x, y), (x + w, y + h), (0, 0, 255), 1)
