# UI Elements Detection
This repo is about detection and recogniton of UI elements of SAP interface
- [x] Detection

## Custom Functions

| **Function**  | **Description** | **Input**|**Output**|
| :--------: | :----------: |:-----:|:---------:|
|    sharp()    | enhances edges of the image  |Image|enhanced Image|
| show_image()  | shows input image in a separate window, which can'e closed by pressing "0| Image | Image |
| get_cord()  | captures each pixel inside boundary decribed by<br>(x,y) = starting coordinates of contour<br>(x+w, y+h) = ending coordinates of contour<br>*h = depth of contour <br> w = width of contour*| x , y , w , h| all the pixel values inside region(x:x+w,y:y+h)|
| find_boxes  | takes binary image as input and does the following**<br>1. Finds verticle and horizontol lines and saves them separately<br>2. Adds both verticle & horizontol images to form contour image<br>3. inverts the image and saves it| binary Image|Image with contours|
|mouse_func()|1. gets pixeles of contours<br>2. gets coordinate of mouse-pointer's location<br>3. compares those coordinates with pixel coordinate from contour<br>4. if they match, draw boundary of that contour|x , y| Localization of detected contour|





## Method<br>
### 1. Binarization of input<br>
binarizing input image using *adaptive Gaussian filter*
<br>
<img src="binary.jpg" alt="binary image" width="450" height="300" />
<br>
### 2. Creating Image for contour detection<br>
>#### 2.1 horizontol lines<br>
<img src="horizontal_lines.jpg" alt="horizontal_lines" width="450" height="300" /> <br>
>#### 2.2 Verticle lines  <br>
<img src="verticle_lines.jpg" alt="Verticle lines" width="450" height="300"/><br>
>#### 2.3 Add horizontol and verticls lines to get full image 
<br><img src="img_final_bin.jpg" alt="img_final_bin" width="450" height="300" /><br>

### 3. Detection and Localization of contours<br>

** Dimensions of the contours are controlled by:<br>
> w = width<br>
> h = depth <br>
```
 if (w < 30 and h>15 and w>15 and h < 30):
 if (w > 20 and h > 10) and w<450 and h<40:
```

<img src="outlined.jpg" alt="Detected contours" width="450" height="300" /><br>
