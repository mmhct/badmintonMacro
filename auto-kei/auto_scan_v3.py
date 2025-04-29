'''可以自动识别可抢的时间，并根据自定义优先顺序抢场'''
import datetime

import pyautogui
import time
from auto_scan import run


def perform_task():
    start = time.time()
    # 继续执行剩余的代码
    pyautogui.click(386, 939)  # 点击5号场地
    #time.sleep(1.5)  # 等待一下，这里必须考虑来自服务器的延迟
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    pyautogui.click(309, 302)  # 点击1号场地
    time.sleep(1.5)  # 等待一下,这里必须考虑来自服务器的延迟，保险起见设置>3秒
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
    time.sleep(0.15)  # 等待一下
    pyautogui.click(2515, 1095)  # 点击确认键

    '''下面这部分就是抢实际的场了，程序会自动识别可抢的场地，并按照自定义优先规则进行选择'''
    # TODO: 根据position.txt里的坐标进行修改
    time.sleep(0.18)  # 等待一下,如果这里还要强行优化，那就识别蒙上一层黑雾的图片
    detection_results = run()
    detection_results = {key: not value for key, value in detection_results.items()}
    if detection_results[14] and detection_results[17]:
        pyautogui.click(1424, 715)  # 15-15:30
        pyautogui.click(2174, 720)  # 16:30-17
    elif detection_results[15] and detection_results[18]:
        pyautogui.click(1667, 724)  # 15:30-16
        pyautogui.click(147, 816)  # 17-17:30
    elif detection_results[16] and detection_results[19]:
        pyautogui.click(1926, 722)  # 16-16:30
        pyautogui.click(408, 815)  # 17:30-18
    elif detection_results[12] and detection_results[15]:
        pyautogui.click(905, 722)  # 14-14:30
        pyautogui.click(1667, 724)  # 15:30-16
    elif detection_results[13] and detection_results[16]:
        pyautogui.click(1164, 721)  # 14:30-15
        pyautogui.click(1926, 722)  # 16-16:30
    elif detection_results[3] and detection_results[6]:
        pyautogui.click(900, 622)  # 9:30-10
        pyautogui.click(1657, 627)  # 11-11:30
    # 更多自定义规则可以在这里添加
    # pyautogui.click(133, 624)  # 8-8:30
    # pyautogui.click(900, 622)  # 9:30-10
    # pyautogui.click(1155, 624)  # 10-10:30
    # pyautogui.click(1925, 624)  # 11:30-12
    else:  # 啥也没剩，我打早八
        pyautogui.click(133, 624)  # 8-8:30
        pyautogui.click(900, 622)  # 9:30-10

    # 下面的固定不改
    pyautogui.click(215, 1192)  # 点击使用人数框
    # pyautogui.click(240, 1252)  # 篮球场测试用
    time.sleep(0.15)  # 等待一下
    pyautogui.write("1")  # 输入文本
    pyautogui.click(714, 1245)  # 点击预约
    end = time.time()
    print("任务执行完毕，耗时：", end - start)
    # pyautogui.click(629, 1301) # 篮球场测试用


if __name__ == "__main__":
    set_time = datetime.datetime.strptime("2024-12-06 21:45:00", "%Y-%m-%d %H:%M:%S")
    time_difference = (set_time - datetime.datetime.now()).total_seconds()
    while time_difference > 0:
        if time_difference > 10:
            time.sleep(5)
        else:
            time.sleep(0.1)
        time_difference = (set_time - datetime.datetime.now()).total_seconds()
    perform_task()  # 执行任务
