import multiprocessing
import threading
import time

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import keyboard

# 用于阻塞的事件标志
start_event = multiprocessing.Event()
blocks = multiprocessing.Manager().dict()
results = multiprocessing.Manager().dict()

def screen_capture():
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    return screen_bgr

def split_image(image):
    # 定义感兴趣区域的坐标
    roi_coords = [
        (597, 652, 40, 254), (597, 652, 305, 519), (597, 652, 563, 778),
        (597, 652, 798, 1017), (597, 652, 1059, 1278), (597, 652, 1320, 1539),
        (597, 652, 1555, 1773), (597, 652, 1817, 2031), (597, 652, 2079, 2291),
        (694, 749, 40, 254), (694, 749, 305, 519), (694, 749, 563, 778),
        (694, 749, 798, 1017), (694, 749, 1059, 1278), (694, 749, 1320, 1539),
        (694, 749, 1555, 1773), (694, 749, 1817, 2031), (694, 749, 2079, 2291),
        (791, 846, 40, 254), (791, 846, 305, 519), (791, 846, 563, 778),
        (791, 846, 798, 1017), (791, 846, 1059, 1278), (791, 846, 1320, 1539),
        (791, 846, 1555, 1773), (791, 846, 1817, 2031), (791, 846, 2079, 2291),
        (888, 943, 40, 254)
    ]

    for i, (y1, y2, x1, x2) in enumerate(roi_coords):
        blocks[i] = image[y1:y2, x1:x2]
    return blocks

def detect_color(block, target_color, threshold=10):
    target_color_bgr = np.uint8(target_color[::-1])
    for row in block:
        for pixel in row:
            if np.all(np.abs(pixel - target_color_bgr) < threshold):
                return True
    return False

def worker(block_id, blocks, results, target_color, threshold):
    results[block_id] = detect_color(blocks[block_id], target_color, threshold)

def auto_scan():
    screen = screen_capture()
    global blocks
    blocks.update(split_image(screen))

    processes = []
    for block_id in range(28):
        p = multiprocessing.Process(target=worker, args=(block_id, blocks, results, (191, 187, 187), 10))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return results

def listen_for_key():
    while True:
        if keyboard.is_pressed('c'):
            start_event.set()
            print("按下 'c' 键，解除阻塞！")
            time.sleep(0.5)
            continue

def perform_task():
    global blocks
    global results
    processes = []
    for block_id in range(28):
        p = multiprocessing.Process(target=worker, args=(block_id, blocks, results, (191, 187, 187), 10))
        p.start()
        processes.append(p)
    print("任务开始，等待解除阻塞...")
    start_event.wait()  # 等待按下 'c' 键解除阻塞
    print("阻塞解除，任务继续执行...")
    start = time.time()
    pyautogui.click(386, 939)
    point1 = time.time()
    start_event.clear()
    start_event.wait()
    point2 = time.time()
    pyautogui.click(29, 83)
    pyautogui.click(343, 512)
    point3 = time.time()
    start_event.clear()
    start_event.wait()
    point4 = time.time()
    pyautogui.click(2239, 518)
    pyautogui.click(1284, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2515, 1095)

    time.sleep(0.1)
    detection_results = auto_scan()  # 自动触发分析
    end = time.time()
    print(f"Time elapsed: {end - start}")
    if detection_results[14] and detection_results[17]:
        pyautogui.click(1424, 715)
        pyautogui.click(2174, 720)
    elif detection_results[15] and detection_results[18]:
        pyautogui.click(1667, 724)
        pyautogui.click(147, 816)
    pyautogui.click(133, 624)
    pyautogui.click(900, 622)

    pyautogui.click(215, 1192)
    time.sleep(0.15)
    pyautogui.write("1")
    pyautogui.click(714, 1245)
    end = time.time()
    print("任务执行完毕，耗时：", end - start)
    print("加载5号场地耗时：", point2 - point1)
    print("点击要抢的场并等待加载完毕耗时：", point4 - point3)

if __name__ == "__main__":
    # 启动监听线程
    listener_thread = threading.Thread(target=listen_for_key, name="ListenerThread", daemon=True)
    listener_thread.start()
    # 启动任务线程
    perform_task()