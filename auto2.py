'''简化了时间选择操作'''
import datetime

import pyautogui
import time


def perform_task():
    start = time.time()
    # 继续执行剩余的代码
    pyautogui.click(386, 939)  # 点击5号场地
    time.sleep(1.5)  # 等待一下
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    pyautogui.click(309, 302)  # 点击1号场地
    time.sleep(2)  # 等待一下,这里必须考虑来自服务器的延迟，保险起见设置>3秒
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

    '''下面这部分就是抢实际的场了，此处可以参考position.txt里的坐标进行修改'''
    # TODO: 根据position.txt里的坐标进行修改
    time.sleep(0.15)  # 等待一下
    # pyautogui.click(133, 624)  # 8-8:30
    # pyautogui.click(900, 622)  # 9:30-10
    # pyautogui.click(1155, 624)  # 10-10:30
    # pyautogui.click(1925, 624)  # 11:30-12
    pyautogui.click(1424, 715)  # 15-15:30
    pyautogui.click(2174, 720)  # 16:30-17

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
