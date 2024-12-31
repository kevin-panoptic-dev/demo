import numpy as np
import cv2 as opencv

capture = opencv.VideoCapture(0)

while True:
    ret, frame = capture.read()
    width, height = int(capture.get(3)), int(capture.get(4))
    image = np.zeros(frame.shape, np.uint8)  # same shape with zeros
    smaller_frame = opencv.resize(frame, None, fx=0.5, fy=0.5)

    image[: height // 2, : width // 2] = opencv.rotate(smaller_frame, opencv.ROTATE_180)
    image[height // 2 :, : width // 2] = opencv.rotate(smaller_frame, opencv.ROTATE_180)
    image[: height // 2, width // 2 :] = opencv.rotate(smaller_frame, opencv.ROTATE_180)
    image[height // 2 :, width // 2 :] = smaller_frame

    opencv.imshow("frame!", image)
    if opencv.waitKey(1) == ord("q"):
        break

capture.release()
opencv.destroyAllWindows()
