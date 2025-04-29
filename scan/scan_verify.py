import time
import cv2
import numpy as np
from PIL import ImageGrab


def screen_capture():
    # 使用PIL库进行屏幕截屏
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    # 转换颜色通道从RGB到BGR，因为cv2使用BGR格式
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    return screen_bgr


def run_verify():
    # start = time.time()
    screen = screen_capture()
    # 获取屏幕截图中的验证码区域 (这里的坐标是示例，需根据实际情况调整)
    blocks = screen[708:943, 1033:1529]  # 这个laptop也适用
    # cv2.imshow("block", blocks)  # 可用来查看验证码区域
    cv2.imwrite("../res/verify.jpg", blocks)

    image = cv2.imread("../res/verify.jpg")
    # 高斯模糊，去除噪声
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    cv2.imshow("blurred", blurred)  # 显示模糊处理后的图像
    cv2.waitKey(0)

    # 边缘检测
    canny = cv2.Canny(blurred, 200, 400)
    cv2.imshow("canny", canny)  # 显示边缘检测结果
    cv2.waitKey(0)

    # 寻找边缘轮廓
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    rectangels = []

    # 逐个轮廓处理，绘制外接矩形
    for i, contour in enumerate(contours):  # 遍历所有轮廓
        # 外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        # 排除面积较小的轮廓（可以根据实际情况调整面积阈值）
        if w > 50 and h > 50:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            rectangels.append((x+w//2, y+h//2))

    # 显示带有矩形框的图像
    cv2.imshow('image', image)
    cv2.waitKey(0)



# 测试用，暂停5秒后执行
time.sleep(5)
run_verify()
