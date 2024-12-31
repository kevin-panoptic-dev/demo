import cv2 as opencv
import numpy as np

capture = opencv.VideoCapture(0)
face_cascade = opencv.CascadeClassifier(opencv.data.haarcascades + "haarcascades_frontalface_default.xml")  # type: ignore
eye_cascade = opencv.CascadeClassifier(opencv.data.haarcascades + "haarcascadees_eye.xml")  # type: ignore


while True:
    ret, frame = capture.read()
    gray = opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        opencv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        roi_gray = gray[y : y + h + 1, x : x + w + 1]
        roi_color = frame[y : y + h + 1, x : x + w + 1]  # shallow reference
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for ex, ey, ew, eh in eyes:
            opencv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 4)

    opencv.imshow("frame", frame)

    if opencv.waitKey(1) == ord("q"):
        break

capture.release()
opencv.destroyAllWindows()
