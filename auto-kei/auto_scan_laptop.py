"""基础方法汇总文件，所有auto_scan系列的文件都会用到的方法都在这里"""
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


def split_image(image):
    # 获取图像的高度和宽度(测试用)
    # h, w, _ = image.shape
    # print(image.shape)

    blocks = {}
    blocks[0] = image[604:640, 76:218]  # 8:00-8:30
    blocks[1] = image[604:640, 336:476]  # 8:30-9:00
    blocks[2] = image[604:640, 602:738]  # 9:00-9:30
    blocks[3] = image[604:640, 830:982]  # 9:30-10:00
    blocks[4] = image[604:640, 1084:1249]  # 10:00-10:30
    blocks[5] = image[604:640, 1347:1511]  # 10:30-11:00
    blocks[6] = image[604:640, 1579:1745]  # 11:00-11:30
    blocks[7] = image[604:640, 1840:2007]  # 11:30-12:00
    blocks[8] = image[604:640, 2101:2269]  # 12:00-12:30
    blocks[9] = image[604:640, 2333:2504]  # 12:30-13:00
    blocks[10] = image[700:736, 64:231]  # 13:00-13:30
    blocks[11] = image[700:736, 325:492]  # 13:30-14:00
    blocks[12] = image[700:736, 560:730]  # 14:00-14:30
    blocks[13] = image[700:736, 822:991]  # 14:30-15:00
    blocks[14] = image[700:736, 1083:1252]  # 15:00-15:30
    blocks[15] = image[700:736, 1316:1487]  # 15:30-16:00
    blocks[16] = image[700:736, 1580:1749]  # 16:00-16:30
    blocks[17] = image[700:736, 1838:2008]  # 16:30-17:00
    blocks[18] = image[700:736, 2074:2244]  # 17:00-17:30
    blocks[19] = image[700:736, 2337:2504]  # 17:30-18:00
    blocks[20] = image[796:831, 65:232]  # 18:00-18:30
    blocks[21] = image[796:831, 300:468]  # 18:30-19:00
    blocks[22] = image[796:831, 560:730]  # 19:00-19:30
    blocks[23] = image[796:831, 820:989]  # 19:30-20:00
    blocks[24] = image[796:831, 1055:1227]  # 20:00-20:30
    blocks[25] = image[796:831, 1316:1488]  # 20:30-21:00
    blocks[26] = image[796:831, 1575:1748]  # 21:00-21:30
    blocks[27] = image[796:831, 1812:1981]  # 21:30-22:00
    # for i in range(28):
    #     cv2.imshow(f"block{i}", blocks[i])
    #     cv2.waitKey(0)
    return blocks


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


def run_lap():
    # start = time.time()
    screen = screen_capture()
    # 将屏幕截图分成约场时间的块
    blocks = split_image(screen)
    # 指定要检测的颜色 (B, G, R)
    target_color = (191, 187, 187)  # 灰色，识别完全准确
    # target_color = (179, 179, 45)  # 浅蓝色,这个好像不对，用不起
    detection_results = {}
    for block_id, block in blocks.items():
        detection_results[block_id] = detect_color(block, target_color)
    # print(detection_results)
    # end = time.time()
    # print(f"Time elapsed: {end - start}")
    return detection_results

