import numpy as np
import cv2 as opencv

base = opencv.resize(  # bad resize
    opencv.imread("assets/soccer_practice.jpg", 0), None, fx=1.1, fy=1.1
)
template = opencv.resize(opencv.imread("assets/shoe.PNG", 0), None, fx=1.4, fy=1.4)

height, width = template.shape  # gray scale, only width and hight

# method
methods = [
    opencv.TM_CCOEFF,
    opencv.TM_CCOEFF_NORMED,
    opencv.TM_CCORR,
    opencv.TM_CCORR_NORMED,
    opencv.TM_SQDIFF,
    opencv.TM_SQDIFF_NORMED,
]

for each_method in methods:
    img = base.copy()
    result = opencv.matchTemplate(img, template, each_method)
    # result = (W - w + 1, H - h + 1)
    *_, min_location, max_location = opencv.minMaxLoc(result)
    if each_method in [opencv.TM_SQDIFF, opencv.TM_SQDIFF_NORMED]:
        location = min_location
    else:
        location = max_location

    bottom_right = (location[0] + width, location[1] + height)
    opencv.rectangle(img, location, bottom_right, 255, 5)
    opencv.imshow("match", img)
    opencv.waitKey(0)
    opencv.destroyAllWindows()
