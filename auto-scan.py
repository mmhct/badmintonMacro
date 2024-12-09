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
    # 获取图像的高度和宽度
    h, w, _ = image.shape
    print(image.shape)
    # 计算每个块的高度和宽度
    blocks = {}
    blocks[0] = image[597:652, 40:254]  # 8:00-8:30
    blocks[1] = image[597:652, 305:519]  # 8:30-9:00
    blocks[2] = image[597:652, 563:778]  # 9:00-9:30
    blocks[3] = image[597:652, 798:1017]  # 9:30-10:00
    blocks[4] = image[597:652, 1059:1278]  # 10:00-10:30
    blocks[5] = image[597:652, 1320:1539]  # 10:30-11:00
    blocks[6] = image[597:652, 1555:1773]  # 11:00-11:30
    blocks[7] = image[597:652, 1817:2031]  # 11:30-12:00
    blocks[8] = image[597:652, 2079:2291]  # 12:00-12:30
    blocks[9] = image[694:749, 40:254]  # 12:30-13:00
    blocks[10] = image[694:749, 305:519]  # 13:00-13:30
    blocks[11] = image[694:749, 563:778]  # 13:30-14:00
    blocks[12] = image[694:749, 798:1017]  # 14:00-14:30
    blocks[13] = image[694:749, 1059:1278]  # 14:30-15:00
    blocks[14] = image[694:749, 1320:1539]  # 15:00-15:30
    blocks[15] = image[694:749, 1555:1773]  # 15:30-16:00
    blocks[16] = image[694:749, 1817:2031]  # 16:00-16:30
    blocks[17] = image[694:749, 2079:2291]  # 16:30-17:00
    blocks[18] = image[791:846, 40:254]  # 17:00-17:30
    blocks[19] = image[791:846, 305:519]  # 17:30-18:00
    blocks[20] = image[791:846, 563:778]  # 18:00-18:30
    blocks[21] = image[791:846, 798:1017]  # 18:30-19:00
    blocks[22] = image[791:846, 1059:1278]  # 19:00-19:30
    blocks[23] = image[791:846, 1320:1539]  # 19:30-20:00
    blocks[24] = image[791:846, 1555:1773]  # 20:00-20:30
    blocks[25] = image[791:846, 1817:2031]  # 20:30-21:00
    blocks[26] = image[791:846, 2079:2291]  # 21:00-21:30
    blocks[27] = image[888:943, 40:254]  # 21:30-22:00
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


if __name__ == "__main__":
    # 截取屏幕
    start = time.time()
    screen = screen_capture()
    # 将屏幕截图分成4行4列的块
    blocks = split_image(screen)
    # 指定要检测的颜色 (B, G, R)
    target_color = (191, 187, 187)  # 灰色
    detection_results = {}
    for block_id, block in blocks.items():
        detection_results[block_id] = detect_color(block, target_color)
    end = time.time()
    print(f"Time elapsed: {end - start}")
    print(detection_results)
