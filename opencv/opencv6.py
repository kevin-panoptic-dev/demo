import cv2 as opencv
import numpy as np

img = opencv.imread("assets/logo1.png")
img = opencv.resize(img, None, fx=0.75, fy=0.75)
gray = opencv.cvtColor(img, opencv.COLOR_BGR2GRAY)

# source image, N corners, quality, minimum
corners: np.ndarray = opencv.goodFeaturesToTrack(gray, 100, 0.8, 10)
if corners is not None:
    corners: np.ndarray = np.int32(corners)  # type: ignore

    for corner in corners:
        x, y = corner.ravel()
        opencv.circle(img, (x, y), 10, (0, 0, 255), -1)
else:
    print("No corner in this image")

for i in range(len(corners)):
    for j in range(i + 1, len(corners)):
        corner1 = tuple(corners[i][0])
        corner2 = tuple(corners[j][0])
        color = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3)))
        opencv.line(img, corner1, corner2, color, 2)


opencv.imshow("Frame", img)
opencv.waitKey(0)
opencv.destroyAllWindows()
