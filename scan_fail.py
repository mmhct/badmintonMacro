"""检测是否预约失败"""
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


def detect_color(block, target_color, threshold=40):
    # 转换目标颜色从RGB到BGR
    target_color_bgr = np.uint8(target_color[::-1])
    # 创建一个与block尺寸相同的数组，并填充目标颜色
    target_color_block = np.full(block.shape, target_color_bgr, dtype=np.uint8)
    # 计算每个像素与目标颜色的差异
    diff = cv2.absdiff(block, target_color_block)
    # 计算差异的总和
    diff_sum = np.sum(diff, axis=-1)
    # 判断是否存在颜色差异小于阈值的像素
    return np.any(diff_sum < threshold)


def run_scan_fail():
    # start = time.time()
    screen = screen_capture()
    # 找出屏幕截图“预约失败”红叉的块
    blocks = screen[306:390, 1229:1347]  # 红叉的位置
    cv2.imshow("block", blocks)
    cv2.imwrite("block.jpg", blocks)  # 测试用
    #
    cv2.waitKey(0)
    # 指定要检测的颜色 (R, G, B)
    target_color = (236, 13, 39)  # 红色，还未调整测试
    detection_results = detect_color(blocks, target_color)
    print("fail detect:", detection_results)
    # end = time.time()
    # print(f"Time elapsed: {end - start}")
    return detection_results

# 测试用
time.sleep(5)
run_scan_fail()
