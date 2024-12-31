import cv2 as opencv
import numpy as np
from numpy.typing import NDArray as npArray


# def convert_hsv(array: npArray[np.uint8]):
#     return opencv.cvtColor(np.array([[array]]), opencv.COLOR_BGR2HSV)[0][0]

capture = opencv.VideoCapture(0)

while True:
    _, frame = capture.read()
    width, height = int(capture.get(3)), int(capture.get(4))

    hsv = opencv.cvtColor(frame, opencv.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = opencv.inRange(hsv, lower_blue, upper_blue)
    frame = opencv.bitwise_and(frame, frame, mask=mask)

    opencv.imshow("frame", frame)

    if opencv.waitKey(1) == ord("q"):
        break

capture.release()
opencv.destroyAllWindows()
