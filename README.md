# UI Elements Recognition
This repo is about detection and recogniton of UI elements of SAP interface
- [x] Detection
- [ ] Recognition

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
