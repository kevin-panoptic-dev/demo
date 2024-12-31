import numpy as np
import cv2 as opencv

capture = opencv.VideoCapture(0)

while True:
    ret, img = capture.read()
    width, height = int(capture.get(3)), int(capture.get(4))
    # line = source + x coordinate + y coordinate + color + width + ...
    img = opencv.line(img, (0, height // 2), (width, height // 2), (0, 255, 0), 10)
    img = opencv.line(img, (0, height), (width, 0), (0, 255, 255), 5)

    # rectangle = source, topleft, bottomright, color, thickness (-1=fill)
    img = opencv.rectangle(img, (100, 100), (400, 400), (200, 200, 200), -1)
    # circle = source, topleft, center, radius, color, thickness
    img = opencv.circle(img, (300, 300), 100, (0, 0, 255), 40)
    # text = source + text + bottomleft, + font + scale + color + thickness + Line_AA
    font = opencv.FONT_HERSHEY_COMPLEX
    img = opencv.putText(
        img,
        "Hannah is Great",
        (333, 333),
        font,
        4,
        (255, 0, 0),
        5,
        opencv.LINE_AA,
    )
    opencv.imshow("image", img)

    if opencv.waitKey(1) == ord("q"):
        break

capture.release()
opencv.destroyAllWindows()
