import cv2 as opencv

# -1 => normal image, 0 => grayscale, 1 => include transparent portion
logo1 = opencv.imread("assets/logo1.png", 0)
logo2 = opencv.imread("assets/logo2.png", 1)
logo2_resized = opencv.resize(logo2, (400, 400))
logo2_relative = opencv.resize(logo2, (0, 0), fx=0.5, fy=0.5)  # shirk
logo2_rotated = opencv.rotate(logo2, opencv.ROTATE_90_COUNTERCLOCKWISE)


# display => (window label, image)
opencv.imshow("image", logo1)
# handle termination, infinite second and wait for any key pressed
opencv.waitKey(0)
opencv.destroyAllWindows()

# write an image
opencv.imwrite("new_image.png", logo2)
