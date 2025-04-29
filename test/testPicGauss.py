import cv2 as cv
image = cv.imread("../res/QQ20241230204144.png")
blurred = cv.GaussianBlur(image, (5, 5), 0)
cv.imshow("blurred", blurred)
cv.waitKey(0)
canny = cv.Canny(blurred, 200, 400)
cv.imshow("canny", canny)
cv.waitKey(0)