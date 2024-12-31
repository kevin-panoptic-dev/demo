import cv2 as opencv
import random
import numpy as np

logo = opencv.imread("assets/logo1.png", -1)
# print(img)
# print(img.shape) height, width, color space
# print(img[0][400])  first row, middle pixel

# randomness
# for i in range(100):
#     for j in range(img.shape[1]):
#         img[i][j] = [
#             random.randint(0, 255),
#             random.randint(0, 255),
#             random.randint(0, 255),
#         ]

# graft
# tag = img[500:700, 600:900]  # row, column
# img[100:300, 650:950] = tag

# generator

height = random.randrange(200, 2000, 100)
width = random.randrange(200, 2000, 100)
channels = 3
img = np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)
print(img.shape)
img = (
    opencv.resize(img, None, fx=1.5, fy=0.8)
    if img.shape[0] > img.shape[1]
    else opencv.resize(img, None, fx=0.8, fy=1.5)
)
print(img.shape)

graft = logo[200:600, 300:400]
graft2 = logo[500:650, 300:700]
try:
    img[100:500, 100:200] = graft
    img[500:650, 400:800] = graft2
except IndexError:
    pass

opencv.imshow("Image", img)
opencv.waitKey(0)
opencv.destroyAllWindows()
