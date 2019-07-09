# ## Import Packages
import numpy as np
import cv2
from PIL import ImageFilter, Image

def sharp(image):
    #Sharpening Image
    image_2 = cv2.GaussianBlur(image,(0,0),3)
    image_3 = cv2.addWeighted(image, 2, image_2, -1, 0)# Thresholding the image
    #save sharped image
    cv2.imwrite("sharp.jpg",image_3)

#load color image
base_address = r'test/'
image_file = '6.png'
image_path = base_address + image_file
original_image = cv2.imread(image_path)
dim = (824,600)
original_image = cv2.resize(original_image,dim, interpolation = cv2.INTER_AREA)
sharp(original_image)
image_color = original_image.copy()

#load image
img = cv2.imread('sharp.jpg',0)
# A kernel of (3 X 3) ones.
kernel = np.ones((3,3),np.uint8)

# Thresholding the image
#(thresh, img_bin) = cv2.threshold(img, 200, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

img_bin = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,5)

#morpholigical operation
img_bin_eroded=cv2.erode(img_bin, kernel, iterations=1)

#Invert Image
img_bin = ~img_bin_eroded

#save image
cv2.imwrite("binary.jpg",img_bin)

#this function opens a new window to show the input image
def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#get all pixeles coordinates in a contour
def get_cord(x,y,w,h):
    idx=0
    coords = []
    for i in range (x,x+w):
        for j in range (y,y+h):
            coords.insert(idx,[i,j])
            #print(idx, coords)
            idx+=1
            
    return coords

# ###  Kernel
# **Define two kernels**
# -  Kernel to detect horizontal lines. 
# -  Kernel to detect vertical lines.

# Defining a kernel length
kernel_length = np.array(img).shape[1]//165

# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

# A kernel of (3 X 3) ones.
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

def find_boxes(img_bin):
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//195

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    #### Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
    
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
    
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    
    #img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=1)
    img_final_bin = ~img_final_bin
      
    return cv2.adaptiveThreshold(img_final_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,5)
img_final_bin = find_boxes(img_bin)
cv2.imwrite("img_final_bin.jpg",img_final_bin)

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
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
 
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

# Find contours for image, which will detect all the boxes
contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort all the contours by top to bottom.
(contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

# ### Identifying Contours
idx = 0
cropped_path = 'Cropped/'
for c in contours:
    
    # Returns the location and width,height for every contour
    x, y, w, h = cv2.boundingRect(c)
    
    #get all the pixels coordinates under contour
    coordinates=[]
    crd = get_cord(x,y,w,h)
    coordinates.append(crd)
    #
   
    if (w>15 and h>10 and w < 30 and h < 20):
        idx+=1
        #extract ROI
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(cropped_path+str(idx)+ '.png', new_img)
        
        #draw boundary of contour
        img_outlined=cv2.rectangle(image_color,(x,y),(x+w,y+h),(255,255,0),2)
    
    # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
    if (w > 20 and h > 10) and w<450 and h<40:
        idx += 1
        
        #ROI extraction
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(cropped_path+str(idx) + '.png', new_img)
        
        #draw contours
        img_outlined=cv2.rectangle(image_color,(x,y),(x+w,y+h),(0,0,255),1)
show_image(img_outlined)
del img_outlined

# 1. gets pixeles of contours
# 2. gets coordinate of right-click 
# 3. compare coordinates (click) with pixel coordinate from contour
# 4. if they match, draw boundary of that contour

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle.
def mouse_func(event, x, y, flags, param):
    global drawing,mode
    
    # 2 is the value for the right mouse click
    if event == cv2.EVENT_MOUSEMOVE:
        drawing = True
        
        #right click co-ordinates
        cord = [x,y] 
        for c in contours:
            
            #staring points (x,y) and dimensions of contour (w=width, h= height)
            x, y, w, h = cv2.boundingRect(c)
            if (w < 30 and h>15 and w>15 and h < 30):
                cor = get_cord(x,y,w,h)
                for i in cor:
                    if i == cord:
                        if drawing == True:
                            if mode == True:
                                cv2.rectangle(original_image,(x,y),(x+w,y+h),(255,255,0),2)
            if (w > 20 and h > 10) and w<445 and h<45:
                cor  = get_cord(x,y,w,h)
                for i in cor:
                    if i == cord:
                        if drawing == True:
                            if mode == True:
                                cv2.rectangle(original_image,(x,y),(x+w,y+h),(0,0,255),1)
                        #print ("It's a box\n")
                        #print ('Dimension: '+ str((x+w)-x)+ " X "+ str((y+h)-y))

cv2.namedWindow('Picture',1)
cv2.setMouseCallback("Picture",mouse_func)
while(1):
    cv2.imshow('Picture', original_image)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
        
    # if pressed "p" exit the pop-up window
    elif k == ord('p'):
        break
cv2.destroyAllWindows()

#Show all contours
for c in contours:
    
    # Returns the location and width,height for every contour
    x, y, w, h = cv2.boundingRect(c)
    
    #if w > 1.3*h and 40>h>10 and w<450:
    clk=cv2.rectangle(image_color,(x,y),(x+w,y+h),(0,150,100),2)
show_image(clk)