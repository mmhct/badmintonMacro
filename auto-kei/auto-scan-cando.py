import time

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import keyboard
import threading
import time


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
    # blocks[0] = image[614:645, 83:108]  # 8:00-8:30
    # blocks[1] = image[614:645, 346:365]  # 8:30-9:00
    # blocks[2] = image[614:645, 606:625]  # 9:00-9:30
    # blocks[3] = image[614:645, 834:851]  # 9:30-10:00
    blocks[4] = image[614:645, 1088:1102]  # 10:00-10:30
    blocks[5] = image[614:645, 1352:1364]  # 10:30-11:00
    blocks[6] = image[614:645, 1587:1601]  # 11:00-11:30
    blocks[7] = image[614:645, 1846:1862]  # 11:30-12:00
    # blocks[8] = image[614:645, 2079:2291]  # 12:00-12:30
    # blocks[9] = image[694:749, 40:254]  # 12:30-13:00
    # blocks[10] = image[694:749, 305:519]  # 13:00-13:30
    # blocks[11] = image[694:749, 563:778]  # 13:30-14:00
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
    # blocks[22] = image[791:846, 1059:1278]  # 19:00-19:30
    # blocks[23] = image[791:846, 1320:1539]  # 19:30-20:00
    # blocks[24] = image[791:846, 1555:1773]  # 20:00-20:30
    # blocks[25] = image[791:846, 1817:2031]  # 20:30-21:00
    # blocks[26] = image[791:846, 2079:2291]  # 21:00-21:30
    # blocks[27] = image[888:943, 40:254]  # 21:30-22:00
    for i in range(28):
        if i not in blocks:
            continue
        cv2.imshow(f"block{i}", blocks[i])
        cv2.waitKey(0)
    return blocks


def detect_color(block, target_color, threshold=10):
    # 转换目标颜色从RGB到BGR
    start=time.time()
    target_color_bgr = np.uint8(target_color[::-1])
    # 创建一个与block尺寸相同的数组，并填充目标颜色
    target_color_block = np.full(block.shape, target_color_bgr, dtype=np.uint8)
    # 计算每个像素与目标颜色的差异
    diff = cv2.absdiff(block, target_color_block)
    # 计算差异的总和
    diff_sum = np.sum(diff, axis=-1)
    end=time.time()
    print(f"Time elapsed2222: {end - start}")
    # 判断是否存在颜色差异小于阈值的像素
    return np.any(diff_sum < threshold)


def auto_scan():
    # 截取屏幕
    start = time.time()
    screen = screen_capture()
    # 将屏幕截图分成约场时间的块
    blocks = split_image(screen)
    # 指定要检测的颜色 (B, G, R)
    target_color = (191, 187, 187)  # 灰色，识别完全准确
    # target_color = (179, 179, 45)  # 浅蓝色,这个好像不对，用不起
    detection_results = {}
    for block_id, block in blocks.items():
        detection_results[block_id] = detect_color(block, target_color)
    end = time.time()
    print(f"Time elapsed: {end - start}")
    return detection_results


# 用于阻塞的事件标志
block_event = threading.Event()


# 监听键盘事件解除阻塞
def listen_for_key():
    while True:
        if keyboard.is_pressed('c'):  # 监听按键事件（这里是 'c' 键）
            block_event.set()  # 按键时解除阻塞
            print("按下 'c' 键，解除阻塞！")
            time.sleep(0.5)  # 防止按键事件被触发多次，这里延迟
            continue


# 模拟程序运行中的阻塞
def perform_task():
    print("任务开始，等待解除阻塞...")
    block_event.wait()  # 阻塞，等待解除
    print("阻塞解除，任务继续执行...")
    start = time.time()
    # 继续执行剩余的代码
    pyautogui.click(386, 939)  # 点击5号场地
    point1 = time.time()
    block_event.clear()  # 重置阻塞事件
    block_event.wait()  # 阻塞，等待解除
    point2 = time.time()
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    '''这里就需要手动操作一下，选择需要抢的场，然后等圈转完（也就是加载完，再按c键）'''
    pyautogui.click(343, 512)  # 点击2号场地,如果要抢其他场地，可以注释掉这行，自己选择c
    point3 = time.time()
    block_event.clear()  # 重置阻塞事件
    block_event.wait()  # 阻塞，等待解除
    point4 = time.time()
    pyautogui.click(2239, 518)  # 点击日期框
    pyautogui.click(1284, 1409)  # 这个是选择下一个月份，如果遇到月份更替就要做这个操作，如果没有更替做这个也没事
    # 这个月份功能还没测试，不知道是否能用，因为选择月份之后可能会有些系统延迟，需要等待一下，等月份更替的时候进行测试
    pyautogui.click(2141, 1409)  # 点击日期栏，其实执行的是选择之后的日期，一般手抢是下滑选择日期
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)  # 连续点击以选到最后的日期，这里多点几次也没事，建议先打开一个然后拖到最底
    pyautogui.click(2515, 1095)  # 点击确认键

    '''下面这部分就是抢实际的场了，程序会自动识别可抢的场地，并按照自定义优先规则进行选择'''
    # TODO: 根据position.txt里的坐标进行修改
    time.sleep(0.1) # 等待一下
    start = time.time()
    detection_results = auto_scan()
    end = time.time()
    print(f"Time elapsed: {end - start}")
    if detection_results[14] and detection_results[17]:
      pyautogui.click(1424, 715)  # 15-15:30
      pyautogui.click(2174, 720)  # 16:30-17
    elif detection_results[15] and detection_results[18]:
      pyautogui.click(1667, 724) # 15:30-16
      pyautogui.click(147, 816) # 17-17:30
    pyautogui.click(133, 624)  # 8-8:30
    pyautogui.click(900, 622)  # 9:30-10
    # pyautogui.click(1155, 624)  # 10-10:30
    # pyautogui.click(1925, 624)  # 11:30-12
    # pyautogui.click(1424, 715)  # 15-15:30
    # pyautogui.click(2174, 720)  # 16:30-17

    # 下面的固定不改
    pyautogui.click(215, 1192)  # 点击使用人数框
    # pyautogui.click(240, 1252)  # 篮球场测试用
    time.sleep(0.15)  # 等待一下
    pyautogui.write("1")  # 输入文本
    pyautogui.click(714, 1245)  # 点击预约
    end = time.time()
    # pyautogui.click(629, 1301) # 篮球场测试用
    print("任务执行完毕，耗时：", end - start)
    print("加载5号场地耗时：", point2 - point1)
    print("点击要抢的场并等待加载完毕耗时：", point4 - point3)


if __name__ == "__main__":
    threading.Thread(target=listen_for_key, daemon=True).start()  # 监听键盘按键
    perform_task()  # 执行任务
