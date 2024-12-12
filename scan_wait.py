"""检测在点下预约键之后是否处于加载状态"""
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


def detect_color(block, target_color, threshold=10):
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


def run2():
    # start = time.time()
    screen = screen_capture()
    # 找出屏幕截图“加载中”显示的块
    blocks = screen[882:901, 1269:1293]  # 这个laptop也适用
    # cv2.imshow("block", blocks)
    # cv2.imwrite("block.jpg", blocks) 测试用
    #
    # cv2.waitKey(0)
    # 指定要检测的颜色 (B, G, R)
    # target_color = (84,84,88)  # 深灰色，connect显示器完美匹配
    target_color = (76, 76, 80)  # 灰色，laptop识别完全准确
    detection_results = detect_color(blocks, target_color)
    print("wait detect:",detection_results)
    # end = time.time()
    # print(f"Time elapsed: {end - start}")
    return detection_results

# 测试用
# time.sleep(5)
# run2()
